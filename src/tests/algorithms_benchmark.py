from os import listdir
from os.path import isfile, join
from time import perf_counter

import matplotlib.pyplot as plt

from src.main.grammar import GrammarUtils
from src.main.graph import Graph

labels = ['CFPQ', 'CFPQTP', 'CFPQTP*', 'Hellings']
colors = ['blue', 'orange', 'green', 'cyan']
graphs = [f for f in listdir('/mnt/x/DataForFLCourse/graphs') if isfile(join('/mnt/x/DataForFLCourse/graphs', f))]
grammars = [f for f in listdir('/mnt/x/DataForFLCourse/grammars') if isfile(join('/mnt/x/DataForFLCourse/grammars', f))]

for grammar_name in grammars:
    for g in graphs:
        (graph_name, separator, extension) = g.partition('.')
        print(grammar_name)
        print(graph_name)
        benchmark_data = [[] for i in range(1, 5)]
        cfg = GrammarUtils.from_file(f'/mnt/x/DataForFLCourse/grammars/{grammar_name}')
        cnf = GrammarUtils.to_cnf(cfg)
        graph = Graph.from_file(f'/mnt/x/DataForFLCourse/graphs/{g}')

        for tests_count in range(5):
            time_start = perf_counter()
            GrammarUtils.cfpq_matrix(graph, cnf)
            time_end = perf_counter()
            benchmark_data[0].append(time_end - time_start)
            print(time_end - time_start)

            time_start = perf_counter()
            GrammarUtils.cfpq_tensor(graph, cfg)
            time_end = perf_counter()
            benchmark_data[1].append(time_end - time_start)
            print(time_end - time_start)

            time_start = perf_counter()
            GrammarUtils.cfpq_tensor(graph, cnf)
            time_end = perf_counter()
            benchmark_data[2].append(time_end - time_start)
            print(time_end - time_start)

            time_start = perf_counter()
            GrammarUtils.cfpq_hellings(cfg, graph)
            time_end = perf_counter()
            benchmark_data[3].append(time_end - time_start)
            print(time_end - time_start)

        figure, axes = plt.subplots()
        benchmark_boxplot = axes.boxplot(benchmark_data, vert=True, patch_artist=True, labels=labels)
        axes.set_title(f'Grammar \"{grammar_name}\" & Graph \"{graph_name}\"')

        for patch, color in zip(benchmark_boxplot['boxes'], colors):
            patch.set_facecolor(color)

        axes.yaxis.grid(True)
        axes.set_ylabel('Time spent, seconds')
        axes.set_xlabel(f'Graph size: {graph.size} nodes')

        plt.savefig(f'images/{graph_name}_{grammar_name}.png')
