# 03_plot_fps_apo_and_holo.py
# Mirror plots with domain-colored x-axis; --fixed/--mobile REQUIRED

import csv
import matplotlib.pyplot as plt
import numpy as np
import argparse
import pandas as pd
import re
from matplotlib.patches import Patch

parser = argparse.ArgumentParser()
parser.add_argument('strength_file_apo', help="path to apo cs_strength csv file")
parser.add_argument('strength_file_holo', help="path to holo cs_strength csv file")
parser.add_argument('target', help="name of target protein (string)")
parser.add_argument('bs_csv', help="csv with binding-site residues")
parser.add_argument('no_res', help="sequence length of target protein (int)")

# Required domain ranges:
parser.add_argument('--fixed', required=True,
                    help='Fixed-domain residue ranges, e.g. "97,101-290,395–398,431,435-521,566-578,581-613"')
parser.add_argument('--mobile', required=True,
                    help='Mobile-domain residue ranges, e.g. "21-96,98-100,293-390,402,407-421,548,550-560"')

args = parser.parse_args()

def parse_ranges(range_str):
    """
    Parse a comma/space/semicolon-separated list of residues and ranges.
    Accepts:
      97
      101-290
      395–398 (en dash), 395—398 (em dash), 395−398 (minus sign)
    Returns inclusive (start, end) tuples with start <= end.
    """
    s = re.sub(r'[–—−]', '-', range_str.strip())  # normalize dash variants
    tokens = re.split(r'[,\s;]+', s)
    spans = []
    for tok in tokens:
        if not tok:
            continue
        if '-' in tok:
            a, b = tok.split('-', 1)
            a, b = int(a), int(b)
            lo, hi = (a, b) if a <= b else (b, a)
            spans.append((lo, hi))
        else:
            n = int(tok)
            spans.append((n, n))
    if not spans:
        raise ValueError("Empty domain ranges are not allowed when required.")
    return spans

def ranges_to_spans(ranges):
    """Convert inclusive (start, end) to broken_barh spans (start, width)."""
    return [(s, e - s + 1) for (s, e) in ranges]

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

# Parse domains (required)
fixed_ranges  = parse_ranges(args.fixed)
mobile_ranges = parse_ranges(args.mobile)

# Load data
x_min, x_max = 0, int(args.no_res)
x_values = list(range(x_min, x_max + 1))
apo_dict  = read_strength_csv(args.strength_file_apo)
holo_dict = read_strength_csv(args.strength_file_holo)
y_apo  = [apo_dict.get(x, 0.0)  for x in x_values]
y_holo = [holo_dict.get(x, 0.0) for x in x_values]

# Binding-site residues (assumes residue numbers in 2nd column)
bs_df = pd.read_csv(args.bs_csv)
bs_res = set(bs_df.iloc[:, 1].astype(int).tolist())

colors = ['tab:red' if res in bs_res else 'tab:gray' for res in x_values]

# Same y-limits for comparability
ymax = max(1.0, max(y_apo or [0]), max(y_holo or [0]))
top_ylim = (0, ymax)
bottom_ylim = (0, ymax)

# Domain ribbon height (thin band at baseline)
ribbon_h = max(0.02 * ymax, 0.5)
fixed_color = 'tab:blue'
mobile_color = 'tab:green'

# Plot
fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, figsize=(12, 7))

# APO (top)
ax1.bar(x_values, y_apo, color=colors, width=0.9, zorder=1)
ax1.set_xlim(x_min - 0.5, x_max + 0.5)
ax1.set_ylim(*top_ylim)
ax1.set_ylabel("Hot Spot Strength (APO)")
ax1.set_title(f"Binding fingerprints, {args.target}")
ax1.set_xticks(range(x_min, x_max + 1, 20))
ax1.broken_barh(ranges_to_spans(fixed_ranges),  (0, ribbon_h),
                facecolors=fixed_color, edgecolors='none', alpha=0.5, zorder=2)
ax1.broken_barh(ranges_to_spans(mobile_ranges), (0, ribbon_h),
                facecolors=mobile_color, edgecolors='none', alpha=0.5, zorder=2)
for res in x_values:
    if res in bs_res:
        ax1.plot(res, 1, marker='*', markerfacecolor='white',
                 markeredgecolor='black', markersize=10, linestyle='None', zorder=3)

# HOLO (bottom, flipped)
ax2.bar(x_values, y_holo, color=colors, width=0.9, zorder=1)
ax2.set_ylim(*bottom_ylim)
ax2.invert_yaxis()
ax2.set_ylabel("Hot Spot Strength (HOLO)")
ax2.set_xlabel("Residues")
ax2.broken_barh(ranges_to_spans(fixed_ranges),  (0, ribbon_h),
                facecolors=fixed_color, edgecolors='none', alpha=0.5, zorder=2)
ax2.broken_barh(ranges_to_spans(mobile_ranges), (0, ribbon_h),
                facecolors=mobile_color, edgecolors='none', alpha=0.5, zorder=2)
for res in x_values:
    if res in bs_res:
        ax2.plot(res, 1, marker='*', markerfacecolor='white',
                 markeredgecolor='black', markersize=10, linestyle='None', zorder=3)

# Baseline line (both)
for ax in (ax1, ax2):
    ax.axhline(0, color='black', linewidth=0.8, zorder=0)

# Domain legend
ax1.legend(handles=[
    Patch(facecolor=fixed_color, alpha=0.5, label='Fixed domain'),
    Patch(facecolor=mobile_color, alpha=0.5, label='Mobile domain'),
], loc='upper right', frameon=False)

plt.tight_layout()
plt.savefig(f"{args.target}_fps_complete.png", dpi=300)
#plt.show()
