import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.lines import Line2D

# ---------------- data ----------------
data = {
    "Protein": [
        "Adenosine kinase", "Adenylate kinase", "Allose-binding protein", "Angiotensin-converting enzyme 2","b-Phosphoglucomutase", "bis-Phosphoglycerate mutase", 
        "Dihydrodipicolinate reductase", "f1ATPase", "Glucokinase", "Glucosamine phosphate synthase", "Glucose/galactose-binding protein", "Guanylate kinase", 
        "Isocitrate dehydrogenase", "Long chain fatty acid COA ligase", "Lysine-sensitive aspartokinase 3", "Nickel-binding periplasmic protein",
        "Nicotinate nucleotide periplasmic protein", "Pyruvate kinase", "Ribose-binding protein", "RNA uridylyl transferase",
        "Sarcoplasmic/endoplasmic reticulum Ca ATPase 1", "Sucrose phosphatase", "Triose phosphate isomerase",
        "UTP glucose 1 phosphate uridylyl transferase"
    ],
    "p-value": [0.27114988, 0.0143274, 0.86524926, 0.00000893, 0.0019961, 0.00175,
                0.2661939, 0.00073636, 0.33310116, 0.34066359, 0.16990109, 0.93477669, 
                0.03891645, 0.50869496, 0.19668779, 0.0430106, 0.91095586, 0.01914924,
                0.00000912, 0.41462379, 0.97310556, 0.94463006, 0.01413064, 0.59814365
    ],
    "recall difference (abs)": [0.0625, 0.205882353, 0.153846154, 0.8125, 0, 0.133333333,
                                0.416666667, 0.1875, 0.285714286, 0.615384615, 0.076923077, 
                                0, 0.222222222, 0.105263158, 0.111111111, 0.125, 0.181818182,
                                0.235294118, 0.307692308, 0.066666667, 0.25, 0, 0.363636364, 0.045454545
    ],
    "Category": ["IF", "CS-IF", "CS", "CS", "IF", "IF", "IF", "IF", "CS-IF",
                 "IF", "CS", "IF", "CS", "IF", "IF", "IF", "CS", "IF", "CS", "IF",
                 "CS-IF", "IF", "IF", "IF"
    ]
}
df = pd.DataFrame(data)

# ---------------- styling ----------------
color_map = {"CS": "#e41a1c", "IF": "#377eb8", "CS-IF": "#4daf4a"}
markers = ['.','o','v','^','<','>','8','s','p','P','*','h','H','X','D','d','1','2','3','4','+','x','|',"_"]
protein_to_marker = {prot: markers[i % len(markers)] for i, prot in enumerate(df["Protein"])}

# ---------------- plot ----------------
fig, ax = plt.subplots(figsize=(9,6))

for _, row in df.iterrows():
    ax.scatter(row["p-value"], row["recall difference (abs)"],
               marker=protein_to_marker[row["Protein"]],
               s=100,
               facecolor=color_map[row["Category"]],
               edgecolor="black", linewidth=0.6)

# Add threshold lines
ax.axvline(x=0.05, color='black', linestyle='--', linewidth=1)
ax.axhline(y=0.5, color='black', linestyle='--', linewidth=1)

# Axes & title
ax.set_xscale("log")
ax.set_xlabel("Paired T-test p-value, apo-holo binding fingerprints")
ax.set_ylabel("Recall difference (absolute val.)")
ax.set_title("Conservation of binding site properties: HS strength vs contacts", pad=20)

# ---------------- legends ----------------
# Category legend
cat_handles = [
    Line2D([], [], marker='o', linestyle='', markersize=8, markerfacecolor=color_map['CS'],
           markeredgecolor='black', label='Conformational selection'),
    Line2D([], [], marker='o', linestyle='', markersize=8, markerfacecolor=color_map['IF'],
           markeredgecolor='black', label='Induced fit'),
    Line2D([], [], marker='o', linestyle='', markersize=8, markerfacecolor=color_map['CS-IF'],
           markeredgecolor='black', label='Mix'),
]

# Protein legend (shape + color)
prot_handles = [
    Line2D([], [], linestyle='', marker=protein_to_marker[prot], markersize=7,
           markerfacecolor=color_map[df.loc[df['Protein']==prot, 'Category'].values[0]],
           markeredgecolor='black', label=prot)
    for prot in df["Protein"]
]

# Adjust layout to make room for legends
plt.subplots_adjust(right=0.72)

# Add both legends at the figure level
fig.legend(handles=cat_handles, title="Mechanism",
           loc='upper left', bbox_to_anchor=(0.73, 0.89), borderaxespad=0.5)
fig.legend(handles=prot_handles, title="Enzyme",
           loc='lower left', bbox_to_anchor=(0.73, 0.1), borderaxespad=0.5,
           fontsize=7, ncol=1, frameon=True)

plt.show()
