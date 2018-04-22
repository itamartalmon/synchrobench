#!/usr/bin/python
import os, re, subprocess, pickle, time
from math import ceil
ITER_NUM = 10
SKIP_LISTS_PATH = os.sep.join(['bin'])
RESULTS_PATH = os.sep.join(['results.pkl'])
NUM_OF_THREADS = [2,4,8,16,32,64]
INIT_SIZE = [524288]
UPDATE_RATIO = [20,50]
DURATION = 10000

TXS_REGEX = "#txs\s+:\s+(\d+)"
NODES_REGEX = "inodes at level (\d+)\s+=\s+(\d+)"

def main():

    skip_lists_bins = [f for f in os.listdir(SKIP_LISTS_PATH) if os.path.isfile(os.path.join(SKIP_LISTS_PATH, f))]
    try:
        with open(RESULTS_PATH, 'rb') as f:
            results_dict = pickle.load(f)
    except BaseException:
        results_dict = {}

    print("\nRotating Skip List Evaluation Script Started\n")
    print('\n'.join([
        "Binary Path: " + SKIP_LISTS_PATH + os.sep,
        "Skip Lists: " + str(skip_lists_bins),
        "Num of Threads: " + str(NUM_OF_THREADS),
        "Initial Set Size: " + str(INIT_SIZE),
        "Update Ratio: " + str(UPDATE_RATIO),
        "Test Duration: " + str(DURATION),
        "Iteration Number: " + str(ITER_NUM)
    ]))
    x_time = ceil(len(skip_lists_bins)*len(NUM_OF_THREADS)*len(INIT_SIZE)*len(UPDATE_RATIO)*ITER_NUM*DURATION / 1000 / 60)
    print("\nApprox. time to finish: ~{0} minutes (lists X thread-nums X sizes X u-ratios X iteration X duration)".format(x_time))
    start_t = time.time()

    for l in skip_lists_bins:
        full_path = os.sep.join([SKIP_LISTS_PATH, l])
        print('\nEvaluating {name}...'.format(name=l))
        if l not in results_dict:
            results_dict[l] = {}
        for i in INIT_SIZE:
            if i not in results_dict[l]:
                results_dict[l][i] = {}
            for u in UPDATE_RATIO:
                if u not in results_dict[l][i]:
                    results_dict[l][i][u] = {}
                for t in NUM_OF_THREADS:
                    cmd = [full_path, '-t '+str(t), '-i '+str(i),
                           '-r '+str(2*i), '-u '+str(u), '-d '+str(DURATION)]
                    print("Running command {0} for {1} iterations".format(' '.join(cmd), ITER_NUM))
                    total_txs = 0
                    nodes = {}
                    for _ in range(ITER_NUM):
                        p = subprocess.Popen(['timeout', str(2*(DURATION/1000))] + cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                        out, err = p.communicate()
                        if p.returncode:
                            print("FAILED TO RUN: {0} will skip to the next list".format(cmd))
                            break
                        out = out.decode('utf-8').strip()
                        total_txs += int(re.findall(TXS_REGEX, out)[0])
                        for level, node_num in re.findall(NODES_REGEX, out):
                            nodes[level] = int(node_num)

                    total_txs = int(total_txs / ITER_NUM)
                    for n in nodes.keys():
                        nodes[n] = int(nodes[n] / ITER_NUM)

                    results_dict[l][i][u][t] = {'txs': total_txs, 'nodes': nodes}

        print("\nSaving {0} results to {1} (as a pickle file)".format(l, RESULTS_PATH))
        with open(RESULTS_PATH, 'wb') as _f:
            pickle.dump(results_dict, _f)

    print("\nTesting done after {0} minutes.".format(ceil((time.time() - start_t) / 60)))

    print("\nRotating Skip List Evaluation Script Finished Successfully\n")

if __name__ == '__main__':
    main()
