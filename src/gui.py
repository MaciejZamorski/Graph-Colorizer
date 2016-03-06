import tkinter as tk
from tkinter import ttk

from graph_colorizer import GraphColorizer

win = tk.Tk()
win.title("Genetic algorithm for graph coloring - Maciej Zamorski")
win.resizable(0, 0)

filename_label = ttk.Label(win, text="Filepath")
filename_label.grid(column=0, row=0)

filename = tk.StringVar()
filename_entry = ttk.Entry(win, width=12, textvariable=filename)
filename_entry.grid(column=0, row=1)
filename_entry.focus()

times_run_label = ttk.Label(win, text="Number of runs")
times_run_label.grid(column=1, row=0)

times_run = tk.IntVar()
times_run_entry = ttk.Entry(win, width=12, textvariable=times_run)
times_run_entry.grid(column=1, row=1)

population_size_label = ttk.Label(win, text="Population size")
population_size_label.grid(column=0, row=2)

population_size = tk.IntVar()
population_size_entry = ttk.Entry(win, width=12, textvariable=population_size)
population_size_entry.grid(column=0, row=3)

max_time_label = ttk.Label(win, text="Generations")
max_time_label.grid(column=1, row=2)

max_time = tk.IntVar()
max_time_entry = ttk.Entry(win, width=12, textvariable=max_time)
max_time_entry.grid(column=1, row=3)

crossing_prob_label = ttk.Label(win, text="Crossover probability")
crossing_prob_label.grid(column=0, row=4)

crossing_prob = tk.IntVar()
crossing_prob_entry = ttk.Entry(win, width=12, textvariable=crossing_prob)
crossing_prob_entry.grid(column=0, row=5)

mutation_prob_label = ttk.Label(win, text="Mutation probability")
mutation_prob_label.grid(column=1, row=4)

mutation_prob = tk.IntVar()
mutation_prob_entry = ttk.Entry(win, width=12, textvariable=mutation_prob)
mutation_prob_entry.grid(column=1, row=5)


def run():
    path = filename.get()
    params = {
        'N': times_run.get(),
        'T': max_time.get(),
        'population_size': population_size.get(),
        'mutation_probability': mutation_prob.get() / 100,
        'crossover_probability': crossing_prob.get() / 100,
        'max_no_improvements': 100,
    }

    gc = GraphColorizer(path, params)
    results = gc.run()
    colors = [result[1] for result in results]

    result = 'Min: {}, max: {}, avg: {}'.format(min(colors), max(colors),
                                                    sum(colors) / len(colors))
    results_label = ttk.Label(win, text=result)
    results_label.grid(column=1, row=6)


# Adding a Button # 6
action = ttk.Button(win, text="Run", command=run)
action.grid(row=6)
win.mainloop()
