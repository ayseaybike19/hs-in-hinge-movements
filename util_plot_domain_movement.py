import matplotlib.pyplot as plt

# Data
conserved = [19]   # two segments
migrated = [5]  # two segments

# Colors
colors_conserved = ["#7D8BE0", "#ABCDDE"]
colors_migrated = ["#7D8BE0", "#EA7D70"]

# Plot conserved bar (stacked segments)
plt.bar("conserved", conserved[0], color=colors_conserved[0], width=0.6)
#plt.bar("conserved", conserved[1], bottom=conserved[0], color=colors_conserved[1], width=0.6)

# Plot migrated bar (stacked segments)
plt.bar("migrated", migrated[0], color=colors_migrated[0],width=0.6)
#plt.bar("migrated", migrated[1], bottom=migrated[0], color=colors_migrated[1],width=0.6)

plt.ylim(0,20)
plt.yticks(range(0,21,2))

# Customize
plt.ylabel("Count")
plt.title("Conservation of HS Location Relative to Domains", pad=20)

# Show plot
plt.show()

