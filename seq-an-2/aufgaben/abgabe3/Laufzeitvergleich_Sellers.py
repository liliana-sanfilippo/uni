import matplotlib.pyplot as plt
runtime_sellers = [0.12, 0.11, 0.15]
runtime_ukkonen = [0.05, 0.04, 0.06]

plt.boxplot([runtime_sellers, runtime_ukkonen],
            tick_labels=["Sellers", "Ukkonen"])
plt.ylabel("Laufzeit (s)")
plt.title("Laufzeitvergleich")
plt.show()