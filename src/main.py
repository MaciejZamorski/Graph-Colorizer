from graph_colorizer import GraphColorizer

if __name__ == '__main__':
    path = 'files/GEOM30b.col'
    params = {
        'N': 10,
        'T': 100,
        'population_size': 100,
        'mutation_probability': 0.05,
        'crossover_probability': 0.8,
        'max_no_improvements': 100,
    }

    gc = GraphColorizer(path, params)
    results = gc.run()
    colors = [result[1] for result in results]

    print('Min: {}, max: {}, średnia: {}'.format(min(colors), max(colors),
                                                 sum(colors) / len(colors)))
