import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import sys
import os

sns.set_theme()
sns.set(rc={'figure.figsize': (21, 14)}) # 15, 10

n = 10
N = 20
FOLDER = 'Graphs'


def render_data(domain, n, N, data, savefile, title, formula):
    xlabs = list(range(n, N + 1))
    ylabs = list(range(n, N + 1))

    t_array = np.zeros((N-n+1, N-n+1))
    for i in range(len(t_array)):
        for j in range(len(t_array[i])):
            t_array[i][j] = None
    for i in range(n, N + 1):
        for j in range(i, N + 1):
            try:
                t_array[i-n][j-n] = formula(data[i-n][j-n])
            except Exception:
                t_array[i-n][j-n] = None

    t_ax = sns.heatmap(t_array, xticklabels=xlabs, yticklabels=ylabs, annot=True)
    t_ax.legend(title=title)

    fig = t_ax.get_figure()
    fig.savefig(f'{domain}/{FOLDER}/{savefile}.png')
    plt.clf()


def plot_data(domain, n, N, data, savefile, title, formula, xlabel, ylabel, order):
    points = []
    for i in range(n, N + 1):
        for j in range(i, N + 1):
            try:
                points.append(formula(data[i-n][j-n]))
            except Exception:
                pass

    l_ax = sns.regplot(x=list(map(lambda x: x[0], points)), y=list(map(lambda x: x[1], points)), order=order)
    l_ax.legend(title=title)

    fig = l_ax.get_figure()
    l_ax.set_xlabel(xlabel)
    l_ax.set_ylabel(ylabel)
    fig.savefig(f'{domain}/{FOLDER}/{savefile}.png')
    plt.clf()
 

def plot_points_data(domain, n, N, data, savefile, title, formula, xlabel, ylabel):
    points = []
    for i in range(n, N + 1):
        for j in range(i, N + 1):
            try:
                points.append(formula(data[i-n][j-n]))
            except Exception:
                pass

    l_ax = sns.scatterplot(x=list(map(lambda x: x[0], points)), y=list(map(lambda x: x[1], points)))
    l_ax.legend(title=title)

    fig = l_ax.get_figure()
    l_ax.set_xlabel(xlabel)
    l_ax.set_ylabel(ylabel)
    fig.savefig(f'{domain}/{FOLDER}/{savefile}.png')
    plt.clf()


def plot_box(domain, n, N, data, savefile, title, ylabel, fields, formulas):
    x_data = []
    y_data = []
    dics = {field: [] for field in fields}
    dics_squished = {'Field': [], 'Time': []}
    for i in range(n, N+1):
        for j in range(i, N+1):
            for fid, field in enumerate(fields):
                try:
                    dics[field] = [formulas[fid](data[i-n][j-n])]
                    dics_squished['Field'].append(field)
                    dics_squished['Time'].append(formulas[fid](data[i-n][j-n]))
                    y_data.append(formulas[fid](data[i-n][j-n]))
                    x_data.append(field)
                except:
                    pass

    dataf = pd.DataFrame(dics)
    dataf_squished = pd.DataFrame(dics_squished)

    # Box plots
    b_ax = sns.boxplot(x=x_data, y=y_data)
    b_ax.legend(title=title)
    b_ax.set_xticklabels(b_ax.get_xticklabels(),rotation=30)

    fig = b_ax.get_figure()
    b_ax.set_ylabel(ylabel)
    fig.savefig(f"{domain}/{FOLDER}/{savefile}.png")
    plt.clf()

    # Violin plots
    # v_ax = sns.violinplot(x='Field', y='Time', data=dataf_squished, scale="count", cut=0)
    # v_ax.legend(title=title)
    # v_ax.set_xticklabels(v_ax.get_xticklabels(),rotation=30)

    # fig = v_ax.get_figure()
    # v_ax.set_ylabel(ylabel)
    # fig.savefig(f"{domain}/{FOLDER}/{savefile}_violin.png")
    # plt.clf()

    # Box plots without outliers
    b_ax = sns.boxplot(x=x_data, y=y_data, showfliers=False)
    b_ax.legend(title=title)
    b_ax.set_xticklabels(b_ax.get_xticklabels(),rotation=30)

    fig = b_ax.get_figure()
    b_ax.set_ylabel(ylabel)
    fig.savefig(f"{domain}/{FOLDER}/{savefile}_nof.png")
    plt.clf()

    # Box plots with swarm
    b_ax = sns.boxplot(x=x_data, y=y_data)
    b_ax.legend(title=title)
    b_ax.set_xticklabels(b_ax.get_xticklabels(),rotation=30)
    b_ax = sns.swarmplot(x=x_data, y=y_data, color=".25")

    fig = b_ax.get_figure()
    b_ax.set_ylabel(ylabel)
    fig.savefig(f"{domain}/{FOLDER}/{savefile}_swarm.png")
    plt.clf()


def plot_violin(domain, n, N, data, data_nocp, savefile, title, ylabel, fields, formulas):
    dics = {field: [] for field in fields} | {'CP': []}
    dics_squished = {'Field': [], 'Time': [], 'CP': []}
    for d, c in [(data, True), (data_nocp, False)]:
        for i in range(n, N+1):
            for j in range(i, N+1):
                for fid, field in enumerate(fields):
                    try:
                        value = formulas[fid](d[i-n][j-n])
                    except:
                        value = 600
                    dics[field].append(value)
                    if value != -1:
                        dics_squished['Field'].append(field)
                        dics_squished['Time'].append(value)
                        dics_squished['CP'].append(c)
                dics['CP'].append(c)

    dataf = pd.DataFrame(dics)
    dataf_squished = pd.DataFrame(dics_squished)

    # Violin plots
    v_ax = sns.violinplot(x='Field', y='Time', hue='CP', split=True, data=dataf_squished, scale="count", cut=0, inner='quartile')
    v_ax.legend(title=title)
    v_ax.set_xticklabels(v_ax.get_xticklabels(),rotation=30)

    fig = v_ax.get_figure()
    v_ax.set_ylabel(ylabel)
    fig.savefig(f"{domain}/{FOLDER}/{savefile}_violin.png")
    plt.clf()

    # Box plots without outliers with CP/NO-CP
    b_ax = sns.boxplot(x='Field', y='Time', hue='CP', data=dataf_squished, showfliers=False)
    b_ax.legend(title=title)
    b_ax.set_xticklabels(b_ax.get_xticklabels(),rotation=30)

    fig = b_ax.get_figure()
    b_ax.set_ylabel(ylabel)
    fig.savefig(f"{domain}/{FOLDER}/{savefile}_nocp_nof.png")
    plt.clf()


def main(argv):
    if len(argv) != 2:
        print("Usage: python3 make_graph.py [domain]")
        return

    # Set up the domain and domain-related data
    domain = str(argv[1])
    if not domain.startswith('./'):
        if domain.startswith('/'):
            domain = '.' + domain
        else:
            domain = './' + domain
    if domain.endswith('/'):
        domain = domain[:-1]
    
    if not os.path.isdir(domain):
        print(f"{domain}: directory not found")
        return

    try:
        with open(f"{domain}/graph_data") as data_file:
            n, N = list(map(int, data_file.readline().split(',')))
    except:
        print(f"Problem reading file graph_data for domain {domain}")
        return

    # Extract the dataset
    data = [[None] * (N - n + 1) for _ in range(N + 1)]
    data_nocp = [[None] * (N - n + 1) for _ in range(N + 1)]

    for i in range(n, N + 1):
        for j in range(i, N + 1):

            try:
                with open(f'{domain}/Stats/pfile{j:0>2}--pfile{i:0>2}.csv') as file:
                    keys = file.readline().split(',')
                    values = list(map(float, file.readline().split(',')))
                    data[i-n][j-n] = {keys[k]: values[k] for k in range(len(keys))}
            except Exception:
                data[i-n][j-n] = {}

            try:
                with open(f'{domain}-nocp/Stats/pfile{j:0>2}--pfile{i:0>2}.csv') as file:
                    keys = file.readline().split(',')
                    values = list(map(float, file.readline().split(',')))
                    data_nocp[i-n][j-n] = {keys[k]: values[k] for k in range(len(keys))}
            except Exception:
                data_nocp[i-n][j-n] = {}

    # Heatmaps
    def pc_simplified_clauses(x):
        return float(x['simplified_clauses']) / (float(x['clauses']) + float(x['simplified_clauses']))

    def percentage_search_phase(x):
        return float(x['sat_solving']) /(float(x['sat_constraint_propagation_time']) + float(x['sat_solving']))

    tests_sets = [('total_time', 'Total time', lambda x: x['total_time\n']),
                  ('variables', 'Variables', lambda x: x['variables']),
                  ('clauses', 'Clauses', lambda x: x['clauses']),
                  ('outcome', 'Outcome', lambda x: x['outcome']),
                  ('p1size', 'P1 Size', lambda x: x['p1fluents'] + x['p1operators']),
                  ('p2size', 'P2 Size', lambda x: x['p2fluents'] + x['p2operators']),
                  ('p1xp2size', 'P1xP2 Size', lambda x: x['p1fluents'] * x['p1operators'] + x['p2fluents'] * x['p2operators']),

                  ('p1pp2size', 'P1+P2 Size', lambda x: x['p1fluents'] + x['p1operators'] + x['p2fluents'] + x['p2operators']),
                  ('simp_clauses', '% Simplified clauses', pc_simplified_clauses),
                  ('solving_vs_cp', 'sat_solving_time / (cp_time + sat_solving_time)', percentage_search_phase),
                  ]

    for savefile, title, formula in tests_sets:
        render_data(domain, n, N, data, savefile, title, formula)

    # Lines plots
    def time_by_size(x):
        return int(((x['p1fluents'] + x['p1operators']) * (x['p2fluents'] + x['p2operators']))), x['total_time\n']
    def time_by_size_add(x):
        return int(((x['p1fluents'] + x['p1operators']) + (x['p2fluents'] + x['p2operators']))), x['total_time\n']

    line_sets = [('time_progression_quad_mul', 'Time', time_by_size, "|P|·|P'|", "Total time (s)", 2),
                 ('time_progression_lin_mul', 'Time', time_by_size, "|P|·|P'|", "Total time (s)", 1),
                 ('time_progression_cube_mul', 'Time', time_by_size, "|P|·|P'|", "Total time (s)", 3),
                 ('time_progression_lin_add', 'Time', time_by_size_add, "|P| + |P'|", "Total time (s)", 1),
                 ('time_progression_quad_add', 'Time', time_by_size_add, "|P| + |P'|", "Total time (s)", 2),
                 ('time_progression_cube_add', 'Time', time_by_size_add, "|P| + |P'|", "Total time (s)", 3),
                 ]

    for savefile, title, formula, xlabel, ylabel, order in line_sets:
        plot_data(domain, n, N, data, savefile, title, formula, xlabel, ylabel, order)

    # Points clouds
    points_sets = [('time_progression_mul', 'Time', time_by_size, "|P|·|P'|", "Total time (s)"),
                   ('time_progression_add', 'Time', time_by_size_add, "|P| + |P'|", "Total time (s)")]

    for savefile, title, formula, xlabel, ylabel in points_sets:
        plot_points_data(domain, n, N, data, savefile, title, formula, xlabel, ylabel)


    # Box plots
    time_fields_names = ['CP - Operator Profiling', 'CP - Constraint Propagation', 'COMP - Fluent image', 'COMP - Operators image', 'COMP - Morphism property', 'COMP - Bijection property', 'COMP - Fluent injectivity', 'COMP - Operator injectivity', 'SAT - Solving' ,'Total time']
    #time_formulas = [(lambda x: x[field]) for field in time_fields]
    time_formulas = [lambda x: x['sat_operator_profiling_time'],
                     lambda x: x['sat_constraint_propagation_time'], 
                     lambda x: x['sat_fluents_images_time'], 
                     lambda x: x['sat_operators_images_time'], 
                     lambda x: x['sat_morphism_property_time'],
                     lambda x: x['sat_bijection_property_time'],
                     lambda x: x['sat_fluents_injectivity_time'], 
                     lambda x: x['sat_operators_injectivity_time'],
                     lambda x: x['sat_solving'],
                     lambda x: x['total_time\n']]

    time_sum_fields = ['Constraint propagation', 'SAT Compilation', 'SAT Solving', 'Total time']
    time_sum_formulas = [lambda x: x['sat_operator_profiling_time'] + x['sat_constraint_propagation_time'],
                         lambda x: x['sat_translation'],
                         lambda x: x['sat_solving'],
                         lambda x: x['total_time\n']]

    box_sets = [('time_distribution', 'Time by step', 'Time (s)', time_fields_names, time_formulas),
                ('time_distribution_summary', 'Time by step', 'Time (s)', time_sum_fields, time_sum_formulas)]
    
    for savefile, title, ylabel, fields, formulas in box_sets:
        plot_violin(domain, n, N, data, data_nocp, savefile, title, ylabel, fields, formulas)
        plot_box(domain, n, N, data, savefile, title, ylabel, fields, formulas)


if __name__ == "__main__":
    main(sys.argv)
