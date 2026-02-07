#!/usr/bin/env python3
import argparse
import pandas as pd
import sys
from scipy.stats import pearsonr
from scipy import stats

def load_and_fill(path, L):
    """
    Load a CSV with columns Residue Number, Total CS Strength.
    Ensure residues 1..L are all present, filling missing with 0.
    Returns a pd.Series indexed by Residue.
    """
    df = pd.read_csv(path)
    if 'Residue Number' not in df.columns or 'Total CS Strength' not in df.columns:
        print(f"Error: {path} must have columns 'Residue Number' and 'Total CS Strength'", file=sys.stderr)
        sys.exit(1)
    # ensure integer index
    s = df.set_index('Residue Number')['Total CS Strength'].astype(float)
    # reindex to full range, fill missing with 0
    full_index = range(1, L+1)
    return s.reindex(full_index, fill_value=0.0)

def main():
    parser = argparse.ArgumentParser(
        description="Compare two residue-based profiles and plot their difference"
    )
    parser.add_argument('csv1', help="Apo Strength CSV (Residue Number,Total CS Strength)")
    parser.add_argument('csv2', help="Holo Strength CSV (Residue Number,Total CS Strength)")
    parser.add_argument('bs_csv', help="csv with bs res listed")
    parser.add_argument('length', type=int,
                        help="Total sequence length L (max residue index)")
    parser.add_argument('output', help="Target name")
    args = parser.parse_args()

    # Load and fill
    s1 = load_and_fill(args.csv1, args.length)
    s2 = load_and_fill(args.csv2, args.length)
    out_s1 = pd.DataFrame({
        'Residue':s1.index,
        'Total Strength Apo':s1.values
    })
    out_s2 = pd.DataFrame({
        'Residue':s2.index,
        'Total Strength Holo':s2.values
    })
    out_s1.to_csv(f"apo_filled_{args.output}.csv", index=False)
    out_s2.to_csv(f"holo_filled_{args.output}.csv", index=False)

    # merge dfs for pcc prep
    merged_df = pd.merge(out_s1, out_s2, on = 'Residue', how = 'inner')
    col_x = merged_df['Total Strength Apo']
    col_y = merged_df['Total Strength Holo']
    merged_df.to_csv(f"merged_strength_{args.output}.csv",index=False)
    #correlation, p_value = pearsonr(col_x,col_y)

    #print(f"{args.output} PCC,{correlation:.4f}")

    # --- get bs res (vectorized; no loop, no concat) ---
    # read the BS csv; assumes the residue numbers are in the 2nd column (index 1)
    bs_df = pd.read_csv(args.bs_csv)

    # make sure the comparison is on the same dtype/name as merged_df's 'Residue'
    bs_res = set(bs_df.iloc[:, 1].astype(int).tolist())

    # filter merged_df to only rows whose Residue is in bs_res
    out_bs_df = merged_df[merged_df['Residue'].isin(bs_res)][
        ['Residue', 'Total Strength Apo', 'Total Strength Holo']
    ].copy()

    out_bs_df.to_csv(f"merged_strength_bs_{args.output}.csv", index=False)
    
    col_xx = out_bs_df['Total Strength Apo']
    col_yy = out_bs_df['Total Strength Holo']

    #corr, pval = pearsonr(col_xx,col_yy)

    #print(f"{args.output} BS PCC,{corr:.4f}")

    t_statistic,p_value = stats.ttest_rel(col_xx,col_yy)

    print(f"{args.output} BS paired T-test,{p_value:.8f}")

if __name__ == '__main__':
    main()
