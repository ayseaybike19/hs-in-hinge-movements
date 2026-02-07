#05.16.25

import glob
import subprocess

job = 'job_file.csv'
ftmap_path = '/Users/aybikebekar/Desktop/hinge_sites/ftmap_results'
ftmap_files = glob.glob(f'{ftmap_path}/*')

with open(job) as job:
    for line in job:
        line = line.strip().split(',')
        i = line[0] #file name: target_apo etc
        j = line[1] #sequence length
        i_list = i.split('_')
        k = i_list[0]

        cmd1 = [
            'python', '01_get_fps.py',
            f'{i}'
        ]

        cmd2 = [
            'python', '02_calc_cs_strength.py',
            f'{i}_contacts.csv',
            f'{i}_cs_strength.csv'
        ]

        cmd3 = [
            'python', '03_plot_fps.py',
            f'{i}_cs_strength.csv',
            f'{i}',
            f'{j}',
            f'{k}_bs_res.csv'
        ]


        subprocess.run(cmd1, check=True)

        subprocess.run(cmd2, check=True)
        
        subprocess.run(cmd3, check=True)

