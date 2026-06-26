#install.packages("tidyverse")
#install.packages("ggplot2")
#install.packages("dplyr")
library(tidyverse)
library(ggplot2)
library(dplyr)
#install.packages("BiocManager")
BiocManager::install("edgeR", force=TRUE)

library(edgeR) 

# Dateien einlesen (tidyverse)
transkriptom <- read_delim("TrockenstresstabellevUebung2.txt")

# Dataframe erzwingen
as.data.frame(transkriptom)

tpm_cols <- colnames(transkriptom)
print(tpm_cols)

# Probennamen heraussuchen, damit man später darüber iterieren kann zur benennung
probennamen <- unique(sub("_[^_]+$", "",  tpm_cols[3:8]))
print(probennamen)

# tpm aus count 
## Siehe Folie 13 Vorlesung 2
## rpk spalten erstellen
transkriptom <- transkriptom %>%
  mutate(across(ends_with("count"), ~.x / length , .names = "{.col}_rpk"
                ))
## summieren 
transkriptom <- transkriptom %>%
  mutate(rpk_sum = rowSums(across(matches("_rpk"))))

## und skalieren
transkriptom <- transkriptom %>%
  mutate(scaling_factor = rpk_sum / 1000000 )

## manuell berechnen 
transkriptom <- transkriptom %>%
  mutate(across(ends_with("rpk"), ~.x / scaling_factor , .names = "{.col}_tpm_manuell"))

## Für die übersichtlichkeit: 

vergleichstabelle <- transkriptom %>% select(matches("(_tpm|_manuell)$"))

### 15:22

# Nur tpms
tpms <- transkriptom %>% select(matches("(_tpm)$"))

# nullreihen entfernen 
tpms <- tpms %>%
  mutate(tpm_sum = rowSums(across(matches("_tpm"))))
 
tpms <- tpms |>
   filter(tpm_sum > 0)

new_tpms <- tpms %>% 
  select(ends_with("_tpm"))

# logfold2 auf alle tpm werte
new_tpms <- new_tpms %>%
  mutate(across(matches("_tpm"), ~ log2(.x +1)))
  
# transponieren 
new_tpms <- t(new_tpms)

# pca 
pca <- prcomp(new_tpms)

# klasse und attribute 
class(pca)
names(pca)

# scores extrahieren 
 scores <- as.data.frame(pca$x)

# plotten 
 ##  erstmal condintions erzeugen, damit man es visuell darstellen kann
scores$sample = rownames(scores)
scores$sample = paste(str_extract(rownames(scores), "[^_]+"), str_extract(rownames(scores), "_[^_]+"), "")
 
 
ggplot(scores, aes(PC1, PC2, color = sample)) +
  #geom_line()
  geom_point()

# clustert es sich wie erwartet?  
## Es ist deutlich gestreuter, als ich es erwartet hätte, aber man sieht trotzdem,
## dass es sich je nach Bedingung entlag einer der Achsen clustert und mit fortschreitendem Zeitverlauf weiter vom ursprünglichen Cluster (oben links) entfernt. 
##Mit etwas Wohlwollen kann man das als das erwartete Clustering bezeichnen

# dgel 

counts <- transkriptom %>% 
  select(ends_with("count")) %>%
  as.matrix()

rownames(counts) <- transkriptom$target_id

proben = colnames(counts)
gruppen <- str_extract(proben, "_[^_]+")
group <- factor(gruppen)


dgel <- DGEList(counts= counts, group=group)

# normalisieren 
dgel <- normLibSizes(dgel)

# dispersion 
dgel <- estimateDisp(dgel)

#classic test  (exakt)
classic_test <- exactTest(dgel)

# ergebnisse
ergebnis <- as.data.frame(topTags(classic_test, n = Inf))
print(ergebnis)

# nein, ist korrigiert, denn die FDR Spalte ist nicht drin 

# joinen 

## gennamen wieder rein 
ergebnis_als_tabelle <- 
  tibble::rownames_to_column(ergebnis, "target_id")

#erweitern
joined <- transkriptom %>% 
  left_join(ergebnis_als_tabelle, by = "target_id")

# wie viele diff. abundant
sum(ergebnis_als_tabelle$FDR < 0.05)
## Ergebnis: 10282

# Nein es wurde keine Annahme verletzt 
