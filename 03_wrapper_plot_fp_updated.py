# run_batch_fp.py  (wrapper)
import csv
import subprocess
import ast
import sys

JOB = "fp_sarc.csv"

def list_of_tuples_to_range_str(s):
    """
    '[(97, 97), (101, 290)]' -> '97,101-290'
    """
    spans = ast.literal_eval(s)  # expects a Python literal list of tuples
    parts = []
    for a, b in spans:
        a, b = int(a), int(b)
        if a == b:
            parts.append(f"{a}")
        else:
            lo, hi = (a, b) if a < b else (b, a)
            parts.append(f"{lo}-{hi}")
    return ",".join(parts)

with open(JOB, newline="") as fh:
    reader = csv.reader(fh)
    for line_no, row in enumerate(reader, start=1):
        # 0=id, 1=target name, 2=bs_csv base, 3=no_res, 4=fixed list, 5=mobile list
        if not row or all(not (c or "").strip() for c in row):
            continue

        if len(row) < 6:
            print(f"[ERROR] Line {line_no}: expected 6 columns, got {len(row)}. Row: {row}", file=sys.stderr)
            continue

        i = row[0].strip()
        target_name = row[1].strip()
        bs_base = row[2].strip()
        no_res = row[3].strip()
        fixed_literal = row[4].strip()
        mobile_literal = row[5].strip()

        # Enforce presence
        if not fixed_literal or not mobile_literal:
            print(f"[ERROR] Line {line_no} ({i}): fixed/mobile ranges are REQUIRED but missing.", file=sys.stderr)
            continue  # or: sys.exit(1)

        try:
            fixed_str = list_of_tuples_to_range_str(fixed_literal)
            mobile_str = list_of_tuples_to_range_str(mobile_literal)
        except Exception as e:
            print(f"[ERROR] Line {line_no} ({i}): could not parse fixed/mobile lists. {e}", file=sys.stderr)
            continue  # or: sys.exit(1)

        cmd = [
            "python", "03_plot_fps_apo_and_holo_upd.py",
            f"../{i}_apo_cs_strength.csv",
            f"../{i}_holo_cs_strength.csv",
            target_name,
            f"../{bs_base}.csv",
            no_res,
            "--fixed", fixed_str,
            "--mobile", mobile_str,
        ]

        #print("RUN:", " ".join(cmd))
        subprocess.run(cmd, check=True)
