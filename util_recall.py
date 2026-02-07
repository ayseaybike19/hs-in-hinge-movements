import csv
import argparse
import pandas as pd

parser = argparse.ArgumentParser()

parser.add_argument('strength_file', help="path to cs_strength csv file")
parser.add_argument('no_res', help="seq length of target protein")
parser.add_argument('bs_csv', help="csv with bs res listed")
args = parser.parse_args()

strength_file = f'{args.strength_file}'

# 1) Read CSV into a dict: residue_number → strength
data = {}
with open(strength_file, newline='') as st:
    reader = csv.DictReader(st)
    for row in reader:
        # convert your columns to numbers
        x = int(row['Residue Number'])
        y = float(row['Total CS Strength'])
        data[x] = y

x_min, x_max = 0, int(f'{args.no_res}')
x_values = list(range(x_min, x_max +1))

y_values = [data.get(x,0) for x in x_values]

bs_df = pd.read_csv(f'{args.bs_csv}')
bs_res = set(bs_df.iloc[:,1].astype(int).tolist())

recall = []

for res,val in zip(x_values,y_values):
    if res in bs_res:
        if val !=0:
            recall.append(val)
print(len(recall))