import csv
import os

jobfile = 'strength_and_bs.csv'
results = {}

with open(jobfile) as jf:
    for strength_path, bs_path in csv.reader(jf):
        prot = os.path.basename(strength_path).replace('_cs_strength.csv','')

        # build a residue→strength map
        strength_map = {}
        with open(strength_path) as stf:
            rdr = csv.reader(stf)
            next(rdr)  # skip header
            for row in rdr:
                res_num = int(row[1])
                strength_map[res_num] = float(row[2])

        # sum up BS strengths (missing → 0.0)
        total = 0.0
        count = 0
        with open(bs_path) as bsf:
            for row in csv.reader(bsf):
                bs_res = int(row[1])
                total += strength_map.get(bs_res, 0.0)
                count += 1

        if count:
            # here we choose to set directly; no accumulation needed
            results[prot] = [total, count]

# now build x, y and compute averages
x = []
y = []
for prot, (cum_strength, cnt) in results.items():
    x.append(prot)
    y.append(cum_strength / cnt)

print(x, y)

