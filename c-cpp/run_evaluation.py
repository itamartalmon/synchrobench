#!/usr/bin/python
import os, re, subprocess, pickle

ITER_NUM = 10
SKIP_LISTS_PATH = os.sep.join(['bin'])
RESULTS_PATH = os.sep.join(['results.pkl'])
NUM_OF_THREADS = [2, 4, 8, 16, 32, 64]
INIT_SIZE = [1024, 2048]
UPDATE_RATIO = [20, 50]
DURATION = 5000

TXS_REGEX = "#txs\s+:\s+(\d+)"
NODES_REGEX = "inodes at level (\d+)\s+=\s+(\d+)"

def main():

    skip_lists_bins = [f for f in os.listdir(SKIP_LISTS_PATH) if os.path.isfile(os.path.join(SKIP_LISTS_PATH, f))]
    results_dict = {}

    for l in skip_lists_bins:
        full_path = os.sep.join([SKIP_LISTS_PATH, l])
        print('Evaluating {name}...'.format(name=l))
        results_dict[l] = {}
        for i in INIT_SIZE:
            results_dict[l][i] = {}
            for u in UPDATE_RATIO:
                results_dict[l][i][u] = {}
                for t in NUM_OF_THREADS:
                    cmd = [full_path, '-t '+str(t), '-i '+str(i), '-r '+str(2*i), '-u '+str(u), '-d '+str(DURATION)]
                    print("Running command {0} for {1} iterations".format(' '.join(cmd), ITER_NUM))
                    total_txs = 0
                    nodes = {}
                    for _ in range(ITER_NUM):
                        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                        out, err = p.communicate()
                        out = out.decode('utf-8').strip()
                        total_txs += int(re.findall(TXS_REGEX, out)[0])
                        for level, node_num in re.findall(NODES_REGEX, out):
                            nodes[level] = int(node_num)

                    total_txs = int(total_txs / ITER_NUM)
                    for n in nodes.keys():
                        nodes[n] = int(nodes[n] / ITER_NUM)

                    results_dict[l][i][u][t] = {'txs': total_txs, 'nodes': nodes}

    with open(RESULTS_PATH, 'wb') as _f:
        pickle.dump(results_dict, _f)


if __name__ == '__main__':
    main()
