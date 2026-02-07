# 05.16.25 (mirror plots with domain-colored x-axis)

import csv
import matplotlib.pyplot as plt
import numpy as np
import argparse
import pandas as pd

parser = argparse.ArgumentParser()
parser.add_argument('strength_file_apo', help="path to apo cs_strength csv file")
parser.add_argument('strength_file_holo', help='path to holo cs_strength csv file')
parser.add_argument('target', help="name of target protein")
parser.add_argument('bs_csv', help="csv with bs res listed")
parser.add_argument('no_res', help="seq length of target protein (int)")
parser.add_argument('fixed_ranges', help='residues in fixed domain')
parser.add_argument('mobile_ranges', help='residues in mobile domain')
args = parser.parse_args()

strength_file_apo = f'{args.strength_file_apo}'
strength_file_holo = f'{args.strength_file_holo}'

# --------- CONFIG: domain residue ranges (inclusive) ----------
# Example for one enzyme; replace with your ranges
fixed_ranges = [(97, 97), (101, 290), (395, 398), (431, 431),
                (435, 521), (566, 578), (581, 613)]  # blue
mobile_ranges = [(21, 96), (98, 100), (293, 390), (402, 402),
                 (407, 421), (548, 548), (550, 560)]  # green

# Colors for domains
fixed_color = 'tab:blue'
mobile_color = 'tab:green'

# --------- helpers ----------
def read_strength_csv(path):
    """Return dict: residue_number -> strength"""
    d = {}
    with open(path, newline='') as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            x = int(row['Residue Number'])
            y = float(row['Total CS Strength'])
            d[x] = y
    return d

def ranges_to_spans(ranges):
    """
    Convert inclusive (start, end) residue ranges to broken_barh spans:
    (start, width) where width counts residues -> end - start + 1
    """
    spans = []
    for s, e in ranges:
        if e < s:
            s, e = e, s
        spans.append((s, e - s + 1))
    return spans

# --------- load data ----------
apo_dict  = read_strength_csv(strength_file_apo)
holo_dict = read_strength_csv(strength_file_holo)

x_min, x_max = 0, int(f'{args.no_res}')
x_values = list(range(x_min, x_max + 1))

y_apo  = [apo_dict.get(x, 0.0)  for x in x_values]
y_holo = [holo_dict.get(x, 0.0) for x in x_values]

# Binding-site residues (assumes residue numbers in 2nd column)
bs_df = pd.read_csv(f'{args.bs_csv}')
bs_res = set(bs_df.iloc[:, 1].astype(int).tolist())

colors = ['tab:red' if res in bs_res else 'tab:gray' for res in x_values]

# Common y-limit so magnitudes are directly comparable
ymax = max(1.0, max(y_apo, default=0), max(y_holo, default=0))
top_ylim = (0, ymax)
bottom_ylim = (0, ymax)  # will be inverted on the second axis

# Ribbon height for the domain-colored baseline (in data y-units)
ribbon_h = max(0.02 * ymax, 0.5)  # thin but visible; tweak as desired

# --------- plotting (Option 2) ----------
fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, figsize=(12, 7))

# TOP: APO (normal)
ax1.bar(x_values, y_apo, color=colors, width=0.9, zorder=1)
ax1.set_xlim(x_min - 0.5, x_max + 0.5)
ax1.set_ylim(*top_ylim)
ax1.set_ylabel("Hot Spot Strength (APO)")
ax1.set_title(f"Binding fingerprints, {args.target}")
ax1.set_xticks(range(x_min, x_max + 1, 20))

# Domain-colored x-axis ribbon (top, just above y=0)
ax1.broken_barh(ranges_to_spans(fixed_ranges), (0, ribbon_h),
                facecolors=fixed_color, edgecolors='none', alpha=0.5, zorder=2)
ax1.broken_barh(ranges_to_spans(mobile_ranges), (0, ribbon_h),
                facecolors=mobile_color, edgecolors='none', alpha=0.5, zorder=2)

# Stars right on the x-axis at y=1 (top)
for res in x_values:
    if res in bs_res:
        ax1.plot(res, 1, marker='*', markerfacecolor='white',
                 markeredgecolor='black', markersize=10, linestyle='None', zorder=3)

# BOTTOM: HOLO (flipped vertically)
ax2.bar(x_values, y_holo, color=colors, width=0.9, zorder=1)
ax2.set_ylim(*bottom_ylim)
ax2.invert_yaxis()  # flip vertically
ax2.set_ylabel("Hot Spot Strength (HOLO)")
ax2.set_xlabel("Residues")

# Domain-colored x-axis ribbon (bottom, just below the shared baseline after inversion)
# Still draw from y=0 to +ribbon_h; inversion makes it appear below the baseline.
ax2.broken_barh(ranges_to_spans(fixed_ranges), (0, ribbon_h),
                facecolors=fixed_color, edgecolors='none', alpha=0.5, zorder=2)
ax2.broken_barh(ranges_to_spans(mobile_ranges), (0, ribbon_h),
                facecolors=mobile_color, edgecolors='none', alpha=0.5, zorder=2)

# Stars right on the shared baseline at y=1 (bottom)
for res in x_values:
    if res in bs_res:
        ax2.plot(res, 1, marker='*', markerfacecolor='white',
                 markeredgecolor='black', markersize=10, linestyle='None', zorder=3)

# Optional guide: thin baseline line to emphasize the shared axis
for ax in (ax1, ax2):
    ax.axhline(0, color='black', linewidth=0.8, zorder=0)

# Legend stub for domains (using proxy patches)
from matplotlib.patches import Patch
legend_handles = [
    Patch(facecolor=fixed_color, alpha=0.5, label='Fixed domain'),
    Patch(facecolor=mobile_color, alpha=0.5, label='Mobile domain'),
]
ax1.legend(handles=legend_handles, loc='upper right', frameon=False)

plt.tight_layout()
plt.savefig(f"{args.target}_fp_labeled.png", dpi=300)
# plt.show()
