#!/usr/bin/env python

import math
import sys
from heapq import nlargest


def emit(key, value):
    sys.stdout.write(str(key) + '\t' + str(value) + '\n')


EPSILON = 0.001


first_iter = True
last_iter = False
num_nodes = 0
iter_num = 0
squared_difference = 0

# Copy of stdin
lst_outputs = []

# List of tuples (rank, node_id)
ranks = []

for line in sys.stdin:
    if 'Iter:' in line:
        first_iter = False
        iter_num = int(line.split('\t')[1]) + 1
        if iter_num == 50:
            # Only print top 20 (should we do it in process_map?)
            last_iter = True
    else:
        # For iterations < 50
        lst_outputs.append(line)

        # For iteration 50
        node_id, info = line.strip('\n').split('\t')
        node_id = node_id[len('NodeId:'):]
        info = info.split(',')
        rank, prev_rank  = info[0:2]
        ranks.append((rank, node_id))

        num_nodes += 1
        squared_difference += (float(rank) - float(prev_rank)) ** 2

if last_iter or math.sqrt(squared_difference / num_nodes) < EPSILON:
    top_ranks = nlargest(20, ranks)
    top_ranks.sort(reverse=True)
    # top_ranks = sorted(ranks, reverse=True)[:20]

    for rank, node_id in top_ranks:
        emit('FinalRank:' + rank, node_id)
else:
    if first_iter:
        emit('Iter:', 1)
    else:
        emit('Iter:', iter_num)

    for output in lst_outputs:
        sys.stdout.write(output)
