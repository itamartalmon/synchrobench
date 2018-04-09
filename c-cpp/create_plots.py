import sys, os, pickle
from matplotlib import pyplot as plt
from run_evaluation import RESULTS_PATH, NUM_OF_THREADS, INIT_SIZE, UPDATE_RATIO


def create_plot(list_to_compare_file='compare.txt'):

    with open(RESULTS_PATH, 'rb') as f:
        results_dict = pickle.load(f)

    lists_names = list(results_dict.keys())

    compare_list = []
    with open(list_to_compare_file, 'r') as f:
        for line in f.readlines():
            if 'skiplist' in line:
                assert line.strip() in lists_names, "Could not find {0} results in th results pickle file".format(line)
                compare_list.append(line.strip())

    compare_lists(results_dict, compare_list)


def compare_lists(results_dict, lists):

    print("\nCreating comparison diagram between the following lists:\n{0}\n".format(lists))
    fig, axes = plt.subplots(nrows=len(INIT_SIZE), ncols=len(UPDATE_RATIO), figsize=(len(INIT_SIZE)*3, len(UPDATE_RATIO)*3))

    for i, size in enumerate(INIT_SIZE):
        for j, u_ratio in enumerate(UPDATE_RATIO):
            ax = axes[i, j]
            ax.set_title('size={s} / u_ratio={u}'.format(s=size, u=u_ratio), fontsize=10)
            args = []
            for l in lists:
                y = [results_dict[l][size][u_ratio][n]['txs'] for n in NUM_OF_THREADS]
                args += [NUM_OF_THREADS, y, '-o']
            lines = ax.plot(*args, linewidth=0.5, markersize=2)
            ax.set_xticks(NUM_OF_THREADS)

    fig.subplots_adjust(top=0.9 - 0.03*len(lists), bottom=0.1, left=0.1, right=0.95, hspace=0.5, wspace=0.3)
    fig.text(0.5, 0.02, 'Number of threads', ha='center')
    fig.text(0.02, 0.5, 'TXS/s', va='center', rotation='vertical')
    fig.legend(lines, lists, loc='upper center')
    plt.savefig('plot_{0}.png'.format('-'.join(lists)))
    plt.close()


if __name__ == '__main__':
    '''
    This script recives a path to a text file that contains the names of lists we want to compare. (default='./compare.txt')
    It will read the relevant information from the results pickle file created by run_evaluation.py and plot the comparison
    over all the relevant configurations
    '''
    if len(sys.argv) > 1:
        create_plot(sys.argv[1])
    else:
        create_plot()
