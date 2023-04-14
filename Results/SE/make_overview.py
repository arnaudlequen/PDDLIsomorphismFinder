import argparse
import itertools as it
import matplotlib.pyplot as plt
import numpy as np
import os
import seaborn as sns
import sys

sns.set_theme()
sns.set('paper', font_scale=3.5, rc={'figure.figsize': (12,9), 'lines.linewidth': 3})
sns.set_style('whitegrid')
# sns.set(font='Verdana')

def instance_id_generator(min_n, max_n):
    for i in range(min_n, max_n+1):
        for j in range(i, max_n+1):
            yield (i, j)


def fetch_data(mode):
    # Max time vs Problems solved
    solved_times = []
    unsat_times = []
    solved_times_size_points = []
    unsat_times_size_points = []

    mode_condition = {'CP': (lambda d: not d.endswith('-nocp')),
                      'NOCP': (lambda d: d.endswith('-nocp'))}

    for domain in [d for d in os.listdir('.') if not os.path.isfile(d) and mode_condition[mode](d)]:
        min_n, max_n = 0, 0
        graph_data_path = f"./{domain}/graph_data"
        if mode == 'NOCP':
            graph_data_path = f"./{domain[:-5]}/graph_data"

        try:
            with open(graph_data_path, 'r') as graph_data_file:
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
                solved_times_size_points.append([instance_stats['total_time\n'], instance_stats['p1fluents'] + instance_stats['p1operators'] + instance_stats['p2fluents'] + instance_stats['p2operators']])
            elif None:
                # Some tests might not follow this convention
                pass
            elif instance_stats['outcome'] >= 0:
                if 'total_time\n' in instance_stats:
                    unsat_times.append(instance_stats['total_time\n'])
                    unsat_times_size_points.append([instance_stats['total_time\n'], instance_stats['p1fluents'] + instance_stats['p1operators'] + instance_stats['p2fluents'] + instance_stats['p2operators']])

    # Transform the data
    solved_times_points = [(time, i) for i, time in enumerate(sorted(solved_times))]
    unsat_times_points =  [(time, i) for i, time in enumerate(sorted(unsat_times))]
    solved_times_size_points.sort()
    unsat_times_size_points.sort()

    for i in range(1, len(solved_times_size_points)):
        if solved_times_size_points[i][1] < solved_times_size_points[i-1][1]:
            solved_times_size_points[i][1] = solved_times_size_points[i-1][1]
    for i in range(1, len(unsat_times_size_points)):
        if unsat_times_size_points[i][1] < unsat_times_size_points[i-1][1]:
            unsat_times_size_points[i][1] = unsat_times_size_points[i-1][1]

    return solved_times_points, unsat_times_points, solved_times_size_points, unsat_times_size_points


def main(argv):
    parser = argparse.ArgumentParser(description="Make the overview of all results")
    parser.add_argument('--table', type=bool, help="Draw a table of all the results")

    solved_times_points, unsat_times_points, solved_times_size_points, unsat_times_size_points = fetch_data('CP')
    solved_times_points_nocp, unsat_times_points_nocp, solved_times_size_points_nocp, unsat_times_size_points_nocp = fetch_data('NOCP')

    graphs_data = [(solved_times_points, solved_times_points_nocp, 'solved_by_time', 'Number of Isomorphisms found within the Time Limit', 'Time cutoff (s)', '# of instances solved'),
                   (unsat_times_points, unsat_times_points_nocp, 'unsat_by_time', 'Number of Negative Instances solved within the Time Limit', 'Time cutoff (s)', '# of instances solved'),
                   (solved_times_size_points, solved_times_size_points_nocp, 'solved_maxsize_by_time', 'Size of the Biggest Positive Instance solved within the Time Limit', 'Time cutoff (s)', '|P| + |P\'|'),
                   (unsat_times_size_points, unsat_times_size_points_nocp, 'unsat_maxsize_by_time', 'Size of the Biggest Negative Instance solved within the Time Limit', 'Time cutoff (s)', '|P| + |P\'|')]

    for data, data_nocp, file_name, title, xlabel, ylabel in graphs_data:
        ax = sns.lineplot(x=list(map(lambda x: x[0], data)), y=list(map(lambda x: x[1], data))) # marker='o'
        ax = sns.lineplot(x=list(map(lambda x: x[0], data_nocp)), y=list(map(lambda x: x[1], data_nocp)))
        ax.set_xticks(range(0, 301, 50), labels=[x if x % 100 == 0 else None for x in range(0, 301, 50) ])
        #ax.legend(title=title)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        fig = ax.get_figure()
        fig.savefig(f"{file_name}_init.svg", bbox_inches='tight')
        fig.savefig(f"{file_name}_init.eps", bbox_inches='tight')
        fig.savefig(f"{file_name}_init.png", bbox_inches='tight')
        plt.clf()


    # Table
    biggest_stats = {}
    maxmin_stats = {}
    terminated_stats = {}
    averages = {}
    for domain in [d for d in os.listdir('.') if not os.path.isfile(d)]:
        min_n, max_n = 0, 0
        real_domain = domain

        if domain.endswith('-nocp'):
            short_domain = domain[:-5]
            real_domain = domain[:-5]  # CLEAN THIS
            if short_domain not in terminated_stats:
                terminated_stats[short_domain] = {'CP': 0, 'NOCP': 0, 'Total': 0}
            graph_data_path = f"./{domain[:-5]}/graph_data"
        else:
            if domain not in terminated_stats:
                terminated_stats[domain] = {'CP': 0, 'NOCP': 0, 'Total': 0}
            graph_data_path = f"./{domain}/graph_data"
        try:
            with open(graph_data_path, 'r') as graph_data_file:
                min_n, max_n = list(map(int, graph_data_file.readline().split(',')))
            terminated_stats[real_domain]['Total'] = (max_n - min_n + 1) ** 2
        except FileNotFoundError:
            continue

        mx = 0 
        instance_stats = None
        mxmin = (0, 0)
        instance_stats_mxmin = None
        domain_sums = {'CP': 0, 'Compilation': 0, 'Solving': 0, 'Total': 0, 'SimpClausesPerc': 0, 'Count': 0}
        for instance_name in [f for f in os.listdir(f"./{domain}/Stats")]:
            names = None
            values = None
            # Parse the .csv file
            with open(f"./{domain}/Stats/{instance_name}", 'r') as instance_file:
                for line in instance_file.readlines():
                    if names is None:
                        names = line.split(',')
                        continue
                    values = list(map(float, line.split(',')))
            
            # Add to the count if the instance terminated
            #  CLEAN THIS (real_domain)
                if not domain.endswith('-nocp'):
                    # terminated_stats[domain]['Total'] = terminated_stats[domain]['Total'] + 1
                    if 'total_time\n' in names:
                        terminated_stats[domain]['CP'] = terminated_stats[domain]['CP'] + 1
                else:
                    # terminated_stats[short_domain]['Total'] = terminated_stats[short_domain]['Total'] + 1
                    if 'total_time\n' in names:
                        terminated_stats[short_domain]['NOCP'] = terminated_stats[short_domain]['NOCP'] + 1

            # Update the biggest problem solved, if needed
            stats = {n: v for n, v in list(zip(names, values))}
            stats = stats | {'instance_name': instance_name}

            # Size of the problem according to two different metrics
            candidate_val = stats['p1fluents'] + stats['p1operators'] + stats['p2fluents'] + stats['p2operators']
            sp1 = stats['p1fluents'] + stats['p1operators']
            sp2 = stats['p2fluents'] + stats['p2operators']
            candidate_val_maxmin = (min(sp1, sp2), max(sp1, sp2))

            if 'sat_translation' in names and 'sat_solving' in names and 'total_time\n' in names:
                try:
                    domain_sums['CP'] += stats['sat_constraint_propagation_time']       
                    domain_sums['SimpClausesPerc'] += stats['simplified_clauses'] / (stats['clauses'] + stats['simplified_clauses']) * 100  # Might be /0
                except KeyError:
                    pass
                domain_sums['Compilation'] += stats['sat_translation'] 
                domain_sums['Solving'] += stats['sat_solving']
                domain_sums['Total'] += stats['total_time\n']
                domain_sums['Count'] += 1

            if 'total_time\n' in names and candidate_val > mx:
                instance_stats = stats
                mx = candidate_val
            if 'total_time\n' in names and candidate_val_maxmin > mxmin:
                instance_stats_mxmin = stats
                mxmin = candidate_val_maxmin


        if instance_stats != None:
            biggest_stats[domain] = instance_stats
        if instance_stats_mxmin != None:
            maxmin_stats[domain] = instance_stats_mxmin
        if domain_sums['Count'] > 0:
            averages[domain] = {'CP': domain_sums['CP']/domain_sums['Count'], 'Compilation': domain_sums['Compilation']/domain_sums['Count'], 'Solving': domain_sums['Solving']/domain_sums['Count'], 'Total': domain_sums['Total']/domain_sums['Count'], 'SimpClausesPerc': domain_sums['SimpClausesPerc']/domain_sums['Count']}

    # Size of the longest name among domains
    mxlen_domain = max(list(map(len, biggest_stats.keys()))) 
    with open('biggest.tex', 'w') as biggest_file, \
         open('count.tex', 'w') as count_file, \
         open('averages.tex', 'w') as average_file:
        print("Biggest problem for which the procedure ends in 600 seconds or less")
        print()
        print(f"{'Domain': <{mxlen_domain}} |   F1   |   O1   |   F2   |   O2   |   SUM  | Slvd-CP |Slvd-NOCP")
        print('-'*72)

        biggest_file.write("\\begin{tabular}{l|rrr|rrr}\n")
        biggest_file.write("\t\\toprule\n")
        biggest_file.write("\t& \multicolumn{3}{c|}{Maximum sum} & \multicolumn{3}{c}{Maximum size of P}\\\\\n")
        biggest_file.write("\tDomain & $\\vert P \\vert$ & $\\vert P' \\vert$ & $\\vert P \\vert$ + $\\vert P' \\vert$ & $\\vert P \\vert$  & $\\vert P' \\vert$ & $\\vert P \\vert$ + $\\vert P' \\vert$ \\\\\n")
        biggest_file.write("\t\\midrule\n")

        count_file.write("\\begin{tabular}{l|rr|rr|r}\n")
        count_file.write("\t\\toprule\n")
        count_file.write("\tDomain & CP & No CP & CP (\\%) & No CP (\\%) & Simp. (\%) \\\\ \n")
        count_file.write("\t\\midrule \n")

        average_file.write("\\begin{tabular}{l|rrr|r}\n")
        average_file.write("\t\\toprule\n")
        average_file.write("\tDomain & CP & Compilation & Solving & Total time \\\\ \n")
        average_file.write("\t\\midrule \n")

        for domain, stats in sorted(list(biggest_stats.items())):
            print(f"{domain: <{mxlen_domain}} |", end='')
            for s in ['p1fluents', 'p1operators', 'p2fluents', 'p2operators']:
                print(f"{int(stats[s]): >7} |", end='')

            sm = int(stats['p1fluents'] + stats['p1operators'] + stats['p2fluents'] + stats['p2operators'])
            print(f"{sm: >8}", end='')
            # Instances on which the algorithm terminated
            if not domain.endswith('-nocp'):
                print(f"{terminated_stats[domain]['CP']: >9}", end='')
                print(f"{terminated_stats[domain]['NOCP']: >9}", end='')
            else:
                print(' '*9)

    
            print(f"   ({stats['instance_name']})")

            sm1 = int(stats['p1fluents'] + stats['p1operators'])
            sm2 = int(stats['p2fluents'] + stats['p2operators'])
            smm1 = int(maxmin_stats[domain]['p1fluents'] + maxmin_stats[domain]['p1operators'])
            smm2 = int(maxmin_stats[domain]['p2fluents'] + maxmin_stats[domain]['p2operators'])

            # Conventions are reversed in the article: P is the smaller problem
            biggest_file.write(f"\t{domain} & {min(sm1, sm2)} & {max(sm1, sm2)} & {sm} & {min(smm1, smm2)} & {max(smm1, smm2)} & {smm1 + smm2} \\\\\n")

            if not domain.endswith('-nocp'):
                count_file.write(f"\t{domain} & {terminated_stats[domain]['CP']} & {terminated_stats[domain]['NOCP']} ")
                count_file.write(f"& {terminated_stats[domain]['CP']/terminated_stats[domain]['Total']*100:0.1f}\\% ")
                count_file.write(f"& {terminated_stats[domain]['NOCP']/terminated_stats[domain]['Total']*100:0.1f}\\% ")
                count_file.write(f"& {averages[domain]['SimpClausesPerc']:0.1f}\\% \\\\ \n")

                average_file.write(f"\t{domain} & {averages[domain]['CP']:0.1f} & {averages[domain]['Compilation']:0.1f} & {averages[domain]['Solving']:0.1f} & {averages[domain]['Total']:0.1f} \\\\ \n")


        average_file.write("\t\\bottomrule\n")
        average_file.write("\\end{tabular}")
        biggest_file.write("\t\\bottomrule\n")
        biggest_file.write("\\end{tabular}")
        count_file.write("\t\\bottomrule\n")
        count_file.write("\\end{tabular}")

if __name__ == "__main__":
    main(sys.argv)
