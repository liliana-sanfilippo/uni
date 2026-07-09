Hier die drei angeforderten Übersichten.

## 1. Existenz von Erwartungswert und Varianz

**Allgemeines Kriterium**

$E[X]$ existiert, wenn $E[|X|] < \infty$ (absolute Konvergenz des Integrals/der Summe). $\text{Var}(X)$ existiert, wenn zusätzlich $E[X^2] < \infty$.

**Faustregel für die Praxis:** Je "schwerer" der Tail (Rand) einer Verteilung, desto eher existieren höhere Momente nicht.

| Verteilung | $E[X]$ existiert? | $\text{Var}(X)$ existiert? | Grund |
|---|---|---|---|
| Alle Verteilungen mit **beschränktem Träger** (Bernoulli, Binomial, Hypergeometrisch, $U(a,b)$, Beta) | immer | immer | Endliches Integrationsgebiet, keine Tail-Probleme |
| Poisson, Geometrisch, Negativ-Binomial | immer | immer | Exponentiell fallende Wahrscheinlichkeiten dominieren jedes Polynom |
| Normal $N(\mu,\sigma^2)$ | immer | immer | Dichte fällt wie $e^{-x^2}$, extrem schneller Tail-Abfall |
| Exponential, Gamma, $\chi^2$ | immer | immer | Dichte fällt wie $e^{-\lambda x}$ |
| **Cauchy** | **existiert nicht** | **existiert nicht** | Tail fällt nur wie $\frac{1}{x^2}$ (Dichte), das Integral $\int x \cdot f(x)\,dx$ divergiert bereits |
| **Pareto** (falls im Kurs relevant) | existiert nur für $\alpha > 1$ | existiert nur für $\alpha > 2$ | Parametrisierter Potenz-Tail, Existenz hängt vom Parameter ab |
| **t-Verteilung** mit $k$ Freiheitsgraden | existiert für $k>1$ | existiert für $k>2$ | Tail-Gewicht hängt von Freiheitsgraden ab |

**Merksatz:** Bei Verteilungen mit **Potenz-Tail** (Cauchy, Pareto, t-Verteilung) musst du immer den Parameter prüfen, der die Tail-Dicke steuert. Bei Verteilungen mit **exponentiellem Tail** (Normal, Exponential, Gamma, Poisson) existieren automatisch alle Momente. Bei **beschränktem Träger** ist die Existenz trivial, weil nichts divergieren kann.

**Klausur-Trick:** Wird nach der Existenz von $E[X^k]$ für wachsendes $k$ gefragt, prüfe, ob das Integral $\int x^k f(x)\,dx$ (bzw. die Summe) für große $|x|$ konvergiert. Bei Cauchy z. B. divergiert schon $k=1$.

---

## 2. Formeln, die man auswendig können sollte

**Grundformeln (Erwartungswert/Varianz allgemein)**

$$E[X] = \sum_i x_i \cdot \mathbb{P}(X=x_i) \quad \text{bzw.} \quad E[X] = \int x f(x)\,dx$$
$$\text{Var}(X) = E[(X-E[X])^2] = E[X^2] - (E[X])^2$$
$$\text{Var}(aX+b) = a^2 \text{Var}(X), \qquad E[aX+b] = aE[X]+b$$

**Für Summen (Linearität, Unabhängigkeit)**

$$E\left[\sum_i X_i\right] = \sum_i E[X_i] \quad \text{(gilt IMMER, auch ohne Unabhängigkeit)}$$
$$\text{Var}\left(\sum_i X_i\right) = \sum_i \text{Var}(X_i) \quad \text{(NUR bei Unabhängigkeit / Unkorreliertheit)}$$
$$\text{Var}\left(\sum_i X_i\right) = \sum_i \text{Var}(X_i) + 2\sum_{i<j}\text{Cov}(X_i,X_j) \quad \text{(allgemein)}$$

**Kenndaten der wichtigsten Verteilungen (unbedingt auswendig)**

$$\text{Ber}(p):\ E=p,\ \text{Var}=pq \qquad \text{Bin}(n,p):\ E=np,\ \text{Var}=npq$$
$$\text{Poi}(\lambda):\ E=\text{Var}=\lambda \qquad N(\mu,\sigma^2):\ E=\mu,\ \text{Var}=\sigma^2$$
$$\text{Exp}(\lambda):\ E=\tfrac{1}{\lambda},\ \text{Var}=\tfrac{1}{\lambda^2}$$

**Standardisierung**

$$Z = \frac{X-\mu}{\sigma} \sim N(0,1) \quad \text{(approx. oder exakt)}$$

**Satz von de Moivre-Laplace / ZGWS**

$$\mathbb{P}(a < \tfrac{S_n-np}{\sqrt{npq}} \leq b) \to \Phi(b)-\Phi(a), \qquad 2\Phi(k)-1 = \mathbb{P}(|Z|\leq k)$$

**Symmetrie von $\Phi$**

$$\Phi(-x) = 1-\Phi(x), \qquad \Phi(0) = \tfrac12$$

**Wichtige $k$-Werte für $\Phi$ (für Konfidenzintervalle, immer wieder gebraucht)**

$$\Phi(1{,}96) = 0{,}975 \ (95\%\text{-Bereich beidseitig}), \quad \Phi(1{,}645)=0{,}95, \quad \Phi(2{,}576)=0{,}995$$

**Tschebyscheff- und Markov-Ungleichung**

$$\mathbb{P}(|X-\mu|\geq k\sigma) \leq \frac{1}{k^2} \qquad \mathbb{P}(X\geq a) \leq \frac{E[X]}{a} \ (X\geq 0)$$

**Poisson-Approximation**

$$\text{Bin}(n,p) \approx \text{Poi}(\lambda), \quad \lambda = np$$

---

## 3. "Tells" — Wie erkennt man in der Aufgabenstellung, was zu tun ist?

**Hinweise auf bestimmte Verteilungen**

| Formulierung im Aufgabentext | Verteilung |
|---|---|
| "genau $k$ von $n$", "wie oft tritt Ereignis auf bei $n$ Wiederholungen", fester $p$ | Binomial |
| "wie viele Versuche bis zum ersten Erfolg" | Geometrisch |
| "Anzahl seltener Ereignisse pro Zeiteinheit/Fläche", "Mutationen pro Genom", "Anrufe pro Stunde" | Poisson |
| "Ziehen ohne Zurücklegen", "aus einer Urne/Charge mit bekannter Fehlerzahl" | Hypergeometrisch |
| "Wartezeit bis zum nächsten Ereignis" (stetig, z. B. Zerfallszeit) | Exponential |
| "Summe von $k$ Wartezeiten", "Zeit bis zum $k$-ten Ereignis" | Gamma |
| "Messfehler", "Rauschen", "viele kleine, additive Einflüsse" | Normal |
| "Anteil / Prozentsatz auf $(0,1)$ als Zufallsgröße selbst" (nicht als Parameter) | Beta |

**Hinweise, dass eine Approximation gefragt ist (statt exakter Rechnung)**

- "$n$ ist groß" / "für große $n$" / "approximiere" / "näherungsweise" → sofortiges Signal für Normal- oder Poisson-Approximation, nicht exakte Binomialformel
- $p$ sehr klein (meist $\leq 0{,}05$ oder $0{,}1$) und $np$ moderat → **Poisson**-Approximation
- $p$ moderat (nicht nahe 0 oder 1) und $npq \geq 9$ → **Normal**-Approximation (de Moivre-Laplace)
- Zahlen so groß, dass Binomialkoeffizient $\binom{n}{k}$ praktisch nicht mehr von Hand berechenbar ist → klares Signal für Approximation

**Hinweise auf ZGWS vs. Gesetz der großen Zahlen**

- "Wie groß muss $n$ mindestens sein, damit..." / "gib ein Konfidenzintervall an" / "mit Wahrscheinlichkeit $95\%$..." → **ZGWS** (konkrete Zahl gefragt)
- "Zeige, dass $S_n/n$ konvergiert" / "zeige Konsistenz des Schätzers" ohne konkrete Fehlerschranke → **Gesetz der großen Zahlen** reicht

**Hinweise auf Chebyshev/Markov statt Normalapproximation**

- "ohne Kenntnis der genauen Verteilung", "nur mit bekanntem Erwartungswert (und ggf. Varianz)", "gib eine obere Schranke an" (nicht "berechne die Wahrscheinlichkeit") → **Markov/Chebyshev**, da diese verteilungsfrei (nicht-asymptotisch) gelten und nur eine Abschätzung liefern, keine exakte/asymptotische Wahrscheinlichkeit

**Hinweise auf Unabhängigkeit vs. Abhängigkeit**

- "unabhängig wiederholt", "i.i.d.", "zufällige Stichprobe mit Zurücklegen" → Unabhängigkeit gegeben, einfache Additionsformel für Varianz nutzbar
- "ohne Zurücklegen", "aus endlicher Population", "abhängige Messungen" → Kovarianzterme beachten, Hypergeometrisch statt Binomial, oder allgemeine Varianzformel mit Kovarianz

**Hinweise auf Schätztheorie (falls das gerade dein Thema ist)**

- "erwartungstreu" / "unbiased" → prüfe $E[\hat\theta] = \theta$
- "konsistent" → prüfe $\hat\theta_n \xrightarrow{P} \theta$ (meist über GGZ oder Chebyshev gezeigt)
- "effizient" / "minimale Varianz" → Vergleich von $\text{Var}(\hat\theta)$ mit Cramér-Rao-Schranke
- "MSE" (Mean Squared Error) gefragt → $\text{MSE}(\hat\theta) = \text{Var}(\hat\theta) + \text{Bias}(\hat\theta)^2$, Bias-Varianz-Zerlegung anwenden

**Genereller Fahrplan beim Lesen einer Aufgabe**

1. Was wird gezählt/gemessen? → bestimmt die Grundverteilung
2. Ist $n$ explizit groß oder wird "approximiere" verlangt? → Approximation nötig
3. Wird nach einer konkreten Zahl (Stichprobengröße, Grenze, Wahrscheinlichkeit) gefragt? → ZGWS mit $\Phi$-Tabelle
4. Wird nur nach einer Schranke/Abschätzung ohne Verteilungsannahme gefragt? → Chebyshev/Markov
5. Wird nur Konvergenz/Existenz gezeigt, keine Zahl berechnet? → GGZ oder Momentenkriterium reicht

Falls du magst, kann ich dir das auch noch als kompaktes LaTeX-Cheat-Sheet (eine Seite, für die Klausurvorbereitung zum Ausdrucken) aufbereiten.