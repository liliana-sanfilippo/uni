#install.packages("tidyverse")
#install.packages("ggplot2")
#install.packages("dplyr")
library(tidyverse)
library(ggplot2)
library(dplyr)
# Ausführen mit Strg + Enter 

# Dateien einlesen (tidyverse)
## https://readr.tidyverse.org/reference/read_delim.html
transkriptom <- read_delim("TrockenstressTag29.txt")

mapman <- read_delim("MapManTAIR10.txt")
descriptions <- read_delim("TAIR10_functional_descriptions_20150630.txt")

# REIHENWEISE Mittel berechnen (tidyverse)
## (Überprüfen sie die Überschriften mit colnames(), nutzen sie die Funktionen mutate(), rowMeans(),
## across(), und matches() um eine neue Spalte mit dem Namen mean_D zu erzeugen und
## eine Spalte mit dem Namen mean_WW zu erzeugen
tpm_cols <- colnames(transkriptom)

print(tpm_cols)

transkriptom <- transkriptom %>%
  mutate(mean_D = rowMeans(across(matches("_D_r"))))
transkriptom <- transkriptom %>%
  mutate(mean_WW = rowMeans(across(matches("_WW_"))))


#mutate(across(names(d_cols), rowMeans))

# log2-foldchange berechnen 
## Addieren sie jeweils 1 zu jedem mean, bilden sie den Quotienten mit Trockenstress im Zähler und
## transformieren sie den Wert mit log2 (D / WW)
logtwofc <- function(x,y) {
   log2( (x+1) / (y+1) )
}

transkriptom <- transkriptom %>%
  mutate(d29Wvs29_D_log2FC = log2((mean_D +1) / (mean_WW +1)))


# Frage: 
## Wie viele Transkripte haben in Kontrollbedingungen eine Abundanz grösser 1000, grösser 100, grösser 10?

# 10172
gr10 <- transkriptom |> filter(mean_WW > 10) |> tally()
# 1336
gr100 <- transkriptom |> filter(mean_WW > 100) |> tally()
#100
gr1000 <- transkriptom |> filter(mean_WW > 1000) |> tally()

# Abbildung (ausschliesslich für die Gene der Kategorie Photosynthese (PS))
## Gennamen anpassen 
transkriptom <- transkriptom %>%
  mutate(target_id_short = substr(target_id, 1, 9))
transkriptom <- transkriptom %>%
  mutate(neg_dek_p = -log10(d29Wvs29_D_q_value))
## Join 
joined <- transkriptom %>% left_join(mapman, by = join_by("target_id_short" == "IDENTIFIER"))
## Nur PS
#ps <- joined |> filter(str_detect(across(NAME), pattern="PS."))
#ps <- joined |> filter(across(NAME, str_detect(pattern="PS.")))
ps <- joined |> filter(str_detect(substr(NAME, 1, 2), "PS")) 
#ps <- transkriptom |> filter(starts_with("PS.")) 

j_cols <- colnames(joined)

print(j_cols)



## Vulcano Plot

zehn_top <- ps %>% 
  slice_max(neg_dek_p, n=10)

volcano_plot <- ggplot(ps, aes(x = d29Wvs29_D_log2FC, y = neg_dek_p, 
                                   color = ifelse(d29Wvs29_D_q_value < 0.01, "red", "black")
                                 )) +
  geom_point(size = 1) +
  labs(title = "Volcano Plot PS", x = "Log2FoldChange", y = "-log10(P-value)") +
  theme_minimal() +
  scale_color_manual(values = c("black", "red"), 
                     labels = c("Nicht signifikant", "Signifikant"), name="Legende") +
  geom_text(data=zehn_top, aes(label=target_id), vjust= -0.5, show.legend = FALSE)

print(volcano_plot)

zehn_top <- joined %>% 
  slice_max(neg_dek_p, n=10)

volcano_plot_all <- ggplot(joined, aes(x = d29Wvs29_D_log2FC, y = neg_dek_p, 
                                   color = ifelse(d29Wvs29_D_q_value < 0.01, "red", "black")
)) +
  geom_point(size = 1) +
  labs(title = "Volcano Plot Alle", x = "Log2FoldChange", y = "-log10(P-value)") +
  theme_minimal() +
  scale_color_manual(values = c("black", "red"), 
                     labels = c("Nicht signifikant", "Signifikant"), name="Legende") +
  geom_text(data=zehn_top, aes(label=target_id), vjust= -0.5, show.legend = FALSE)


print(volcano_plot_all)

## Histogramm der Transkriptabundanzen

histo_data_all <- joined  %>% pivot_longer(
  cols = c(mean_D, mean_WW), 
  names_to = "Bedingung",
  values_to = "Abundanzen"
)

histo_data_ps <- ps  %>% pivot_longer(
  cols = c(mean_D, mean_WW), 
  names_to = "Bedingung",
  values_to = "Abundanzen"
)

### 

histo_alle_einzeln <- ggplot(histo_data_all, aes(x = Abundanzen, fill= Bedingung)) +
  labs(title = "Histogramm Alle") + 
  geom_histogram() +
  facet_wrap(~Bedingung) +
  scale_x_log10()

print(histo_alle_einzeln)

ggplot(histo_data_ps, aes(x = Abundanzen, fill= Bedingung)) +
  labs(title = "Histogramm PS") + 
  geom_histogram() +
  facet_wrap(~Bedingung)
  scale_x_log10()
  
###
  
ggplot(histo_data_all, aes(x = Abundanzen, fill= Bedingung)) +
    labs(title = "Histogramm Alle") + 
    geom_histogram(position="dodge") +
    scale_x_log10()
  
ggplot(histo_data_ps, aes(x = Abundanzen, fill= Bedingung)) +
    labs(title = "Histogramm PS") + 
    geom_histogram(position="dodge") +
  scale_x_log10()


## Boxplot der fold-changes

ggplot(ps, aes(y = d29Wvs29_D_log2FC)) +
  labs(title = "Boxplot PS") +
  geom_boxplot()
  
ggplot(joined, aes(y = d29Wvs29_D_log2FC)) +
  labs(title = "Boxplot Alle") +
  geom_boxplot()

# Warum erwartet man es so oder auch nicht?



