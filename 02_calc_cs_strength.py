#!/usr/bin/env python3
import argparse
import pandas as pd
import ast

def parse_contacts(contacts_str):
    """
    Given a string like "('ALA', '10'),('GLU', '14'),…",
    wrap in [ ] and literal_eval to get a list of 2-tuples.
    If the field is missing or not a string, return an empty list.
    """
    if not isinstance(contacts_str, str) or contacts_str.strip() == '':
        return []

    try:
        return ast.literal_eval(f'[{contacts_str}]')
    except Exception:
        contacts = []
        for item in contacts_str.split("),("):
            item = item.strip().lstrip('(').rstrip(')')
            parts = [p.strip().strip("'").strip('"') for p in item.split(',')]
            if len(parts) == 2:
                contacts.append((parts[0], parts[1]))
        return contacts

def main():
    parser = argparse.ArgumentParser(
        description="Summarize CS 'strength' by contact per PDBID."
    )
    parser.add_argument('input_csv',  help='path to input CSV (with columns PDBID, CS, Contacts)')
    parser.add_argument('output_csv', help='path for output summary CSV')
    args = parser.parse_args()

    # --- Read and debug-print the input ---
    df = pd.read_csv(args.input_csv, usecols=['PDBID', 'CS', 'Contacts'])

    totals = {}

    # --- Aggregate strengths ---
    for _, row in df.iterrows():
        pdb = row['PDBID']
        raw_cs = row['CS']

        # strip a trailing ".pdb" if present
        if isinstance(raw_cs, str) and raw_cs.lower().endswith('.pdb'):
            cs_name = raw_cs[:-4]
        else:
            cs_name = raw_cs

        # now extract numeric part
        try:
            num_part = cs_name.split('.')[-1]
            strength = int(num_part[-2:])
        except Exception:
            # skip any malformed CS entries
            continue

        contacts = parse_contacts(row['Contacts'])
        for res_num in set(contacts):
            key = (pdb, res_num)
            totals[key] = totals.get(key, 0) + strength

    # --- Build output DataFrame ---
    out_rows = [
        {
            'PDBID': pdb,
            'Residue Number': res_num,
            'Total CS Strength': total
        }
        for (pdb, res_num), total in totals.items()
    ]
    out_df = pd.DataFrame(out_rows)

    # --- Guard and write ---
    if out_df.empty:
        print("⚠️  No data was aggregated—check that your Contacts/CS columns are present and non-empty.")
    else:
        required = ['PDBID', 'Residue Number']
        missing = [col for col in required if col not in out_df.columns]
        if missing:
            raise RuntimeError(f"Expected columns missing in output: {missing}")

        out_df = out_df.sort_values(required)
        out_df.to_csv(args.output_csv, index=False)
        print(f"✅  Wrote summary to {args.output_csv}")

if __name__ == '__main__':
    main()

