import subprocess

job = 'pcc_job_file.csv'

with open(job) as job:
    for line in job:
        line = line.strip().split(',')
        i = line[0]
        j = line[1] 

        cmd1 = [
            'python', 'util_pcc.py',
            f'{i}_apo_cs_strength.csv', f'{i}_holo_cs_strength.csv', f'{i}_bs_res.csv', f'{j}', f'{i}'
        ]

        subprocess.run(cmd1, check=True)
