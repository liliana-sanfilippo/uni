"""Robuste Helfer fuer die eKVV-API: Rate-Limiting, Backoff, leere Antworten, Cache."""
import hashlib
import json
import os
import re
import time
import requests

SESSION = requests.Session()
SESSION.headers.update({
    "User-Agent": "kr-studienplan-projekt/1.0 (Uni-Projekt)",
    "Accept": "application/json",
})

PAUSE = 0.5                 # hoefliche Grundpause zwischen zwei Requests (Sekunden)
CACHE_DIR = "cache"         # hier landen die gecachten Antworten


# ---------- Wartezeiten ----------
def _wartezeit(resp, versuch, basis=1.0):
    ra = resp.headers.get("Retry-After")
    if ra:
        try:
            return float(ra)
        except ValueError:
            pass
    return basis * (2 ** versuch)          # 1s, 2s, 4s, 8s, ...


def _wartezeit_fallback(versuch, basis=1.0):
    return basis * (2 ** versuch)


# ---------- Kern: ein Abruf mit klarem Ergebnis ----------
def _fetch_json(url, *, max_versuche=5, timeout=20, verbose=True):
    """Liefert (ausgang, daten) mit ausgang in {'data','empty','failed'}.

    'data'   -> daten = geparstes JSON
    'empty'  -> leerer Body (z.B. Veranstaltung im Semester nicht angeboten)
    'failed' -> nach Wiederholungen aufgegeben oder 200-ohne-JSON
    echte 4xx (z.B. 404) -> Exception
    """
    for versuch in range(max_versuche):
        try:
            resp = SESSION.get(url, timeout=timeout)
        except requests.RequestException as e:
            wz = _wartezeit_fallback(versuch)
            if verbose:
                print(f"  Netzwerkfehler bei {url}: {e} -> warte {wz:.1f}s")
            time.sleep(wz)
            continue

        if resp.status_code == 429 or 500 <= resp.status_code < 600:
            wz = _wartezeit(resp, versuch)
            if verbose:
                print(f"  HTTP {resp.status_code} bei {url} -> warte {wz:.1f}s "
                      f"(Versuch {versuch + 1}/{max_versuche})")
            time.sleep(wz)
            continue

        resp.raise_for_status()

        if not resp.text.strip():
            return ("empty", None)

        try:
            return ("data", resp.json())
        except ValueError:
            if verbose:
                print(f"  Kein JSON von {url}: {resp.text[:120]!r}")
            return ("failed", None)

    if verbose:
        print(f"  Nach {max_versuche} Versuchen aufgegeben: {url}")
    return ("failed", None)


# ---------- Oeffentliche API (unveraendert kompatibel) ----------
def get_json(url, **kw):
    """Wie bisher: JSON zurueck, oder None bei leerem Body / Fehlschlag."""
    _ausgang, daten = _fetch_json(url, **kw)
    return daten


# ---------- Cache-Variante ----------
def _cache_pfad(url):
    h = hashlib.sha256(url.encode("utf-8")).hexdigest()[:12]
    tail = re.sub(r"[^A-Za-z0-9._-]", "_", url.rstrip("/").split("/")[-1])[:40] or "root"
    return os.path.join(CACHE_DIR, f"{tail}_{h}.json")


def get_json_cached(url, *, erneuern=False, verbose=True, **kw):
    """Wie get_json, aber mit lokalem Datei-Cache.

    - Cache-Treffer      -> kein API-Aufruf
    - erneuern=True      -> Cache umgehen und neu holen
    - 'data'/'empty'     -> wird gecacht
    - 'failed'           -> NICHT gecacht (Fehler nicht einfrieren)
    """
    pfad = _cache_pfad(url)

    if not erneuern and os.path.exists(pfad):
        try:
            with open(pfad, encoding="utf-8") as f:
                if verbose:
                    print(f"  Cache-Treffer: {url}")
                return json.load(f)
        except (ValueError, OSError):
            pass                            # kaputte Cache-Datei -> neu holen

    ausgang, daten = _fetch_json(url, verbose=verbose, **kw)

    if ausgang in ("data", "empty"):
        os.makedirs(CACHE_DIR, exist_ok=True)
        with open(pfad, "w", encoding="utf-8") as f:
            json.dump(daten, f, ensure_ascii=False, indent=2)

    return daten