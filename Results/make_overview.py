import argparse
import itertools as it
import matplotlib.pyplot as plt
import numpy as np
import os
import seaborn as sns
import sys

sns.set_theme()
sns.set(rc={'figure.figsize': (15, 10)})
sns.set_style('whitegrid')

def instance_id_generator(min_n, max_n):
    for i in range(min_n, max_n+1):
        for j in range(i, max_n+1):
            yield (i, j)

def main(argv):
    parser = argparse.ArgumentParser(description="Make the overview of all results")
    parser.add_argument('--table', type=bool, help="Draw a table of all the results")

    # Max time vs Problems solved
    solved_times = []
    unsat_times = []

    for domain in [d for d in os.listdir('.') if not os.path.isfile(d)]:
        min_n, max_n = 0, 0
        try:
            with open(f"./{domain}/graph_data", 'r') as graph_data_file:
                min_n, max_n = list(map(int, graph_data_file.readline().split(',')))
        except FileNotFoundError:
            continue

        for instance_name in (f"./{domain}/Stats/pfile{i}--pfile{j}.csv" for (i, j) in it.product(range(min_n, max_n+1), range(min_n, max_n+1))): #instance_id_generator(min_n, max_n)):
            instance_stats = None
            try:
                with open(instance_name, 'r') as instance_file:
                    col_names = instance_file.readline().split(',')
                    col_values = list(map(float, instance_file.readline().split(',')))
                    instance_stats = {col_names[i]: col_values[i] for i in range(len(col_names))}
            except FileNotFoundError:
                continue

            if instance_stats['outcome'] == 100:
                solved_times.append(instance_stats['total_time\n'])
            else:
                unsat_times.append(instance_stats['total_time\n'])

    # Transform the data
    # solved_times = list(enumerate(solved_times.sorted()))
    # unsat_times = list(enumerate(unsat_times.sorted()))
    solved_times_points = [(time, i) for i, time in enumerate(sorted(solved_times))]
    unsat_times_points =  [(time, i) for i, time in enumerate(sorted(unsat_times))]

    graphs_data = [(solved_times_points, 'solved_by_time', 'Number of Isomorphisms found within the Time Limit', 'Time cutoff (s)', '# of instances solved'),
                   (unsat_times_points, 'unsat_by_time', 'Number of Negative Instances solved within the Time Limit', 'Time cutoff (s)', '# of instances solved')]

    for data, file_name, title, xlabel, ylabel in graphs_data:
        ax = sns.lineplot(x=list(map(lambda x: x[0], data)), y=list(map(lambda x: x[1], data))) # marker='o'
        ax.set_xticks(range(0, 601, 50), labels=range(0, 601, 50))
        ax.legend(title=title)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        fig = ax.get_figure()
        fig.savefig(f"{file_name}.png")
        plt.clf()


    # Table
    biggest_stats = {}
    for domain in [d for d in os.listdir('.') if not os.path.isfile(d)]:
        min_n, max_n = 0, 0
        try:
            with open(f"./{domain}/graph_data", 'r') as graph_data_file:
                min_n, max_n = list(map(int, graph_data_file.readline().split(',')))
        except FileNotFoundError:
            continue

        mx = 0 
        instance_stats = None
        for instance_name in [f for f in os.listdir(f"./{domain}/Stats")]:
            names = None
            values = None
            with open(f"./{domain}/Stats/{instance_name}", 'r') as instance_file:
                for line in instance_file.readlines():
                    if names is None:
                        names = line.split(',')
                        continue
                    values = list(map(float, line.split(',')))
            
            stats = {n: v for n, v in list(zip(names, values))}
            stats = stats | {'instance_name': instance_name}
            candidate_val = stats['p1fluents'] + stats['p1operators'] + stats['p2fluents'] + stats['p2operators']
            if candidate_val > mx:
                instance_stats = stats
                mx = candidate_val

        if instance_stats != None:
            biggest_stats[domain] = instance_stats


    mxlen_domain = max(list(map(len, biggest_stats.keys()))) 
    print("Biggest problem for which the procedure ends in 600 seconds or less")
    print()
    print(f"{'Domain': <{mxlen_domain}} |   F1   |   O1   |   F2   |   O2   |   SUM  ")
    print('-'*64)
    for domain, stats in biggest_stats.items():
        print(f"{domain: <{mxlen_domain}} |", end='')
        for s in ['p1fluents', 'p1operators', 'p2fluents', 'p2operators']:
            print(f"{stats[s]: >7} |", end='')

        sm = stats['p1fluents'] + stats['p1operators'] + stats['p2fluents'] + stats['p2operators']
        print(f"{sm: >8}", end='')
        print(f"   ({stats['instance_name']})")


if __name__ == "__main__":
    main(sys.argv)
