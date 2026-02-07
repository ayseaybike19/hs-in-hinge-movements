import glob
import argparse
from pymol import cmd, stored

parser = argparse.ArgumentParser()

parser.add_argument('job', help='path to job file with inputs')
args = parser.parse_args()

ftmap_path = ('/Users/aybikebekar/Desktop/hinge_sites/ftmap_results')
ftmap_files = glob.glob('/Users/aybikebekar/Desktop/hinge_sites/ftmap_results' + '/*')

def cluster_finder(inp):
    cluster_info = []
    with open(inp) as res:
        for line in res:
             if line.startswith("HEADER cross"):
                header_line = line.split()
                cluster_info.append(header_line[1])
    return cluster_info

if __name__ == '__main__':
    with open(f"{args.job}_contacts.csv", "w") as fo:
        fo.write("PDBID,CS,Contacts\n")

        cluster_info = cluster_finder(f'{ftmap_path}/{args.job}_mapped.pdb')

        cmd.load(f"{ftmap_path}/{args.job}_mapped.pdb")

        for cluster in cluster_info:
            stored.contacts = []
            cmd.select("cont_cs",f"byres protein within 3 of {cluster}")
            cmd.iterate("cont_cs and name CA", "stored.contacts.append((resi))")    
            fo.write(f'{args.job},{cluster},"{",".join(map(str, stored.contacts))}"\n')    
