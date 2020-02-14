#!/usr/bin/env python

import math
import sys
from heapq import nlargest


def emit(key, value):
    sys.stdout.write(str(key) + '\t' + str(value) + '\n')


# EPSILON = 0.007


first_iter = True
last_iter = False
num_nodes = 0
iter_num = 0
# squared_difference = 0

# Copy of stdin
lst_outputs = []

# List of tuples (rank, node_id)
ranks = []

# Dictionary mapping node to prev_rank
prev_ranks = {}

for line in sys.stdin:
    if 'Iter:' in line:
        first_iter = False
        iter_num = int(line.split('\t')[1]) + 1
        if iter_num == 50:
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
        prev_ranks[node_id] = prev_rank
        # squared_difference += (float(rank) - float(prev_rank)) ** 2

# Check convergence (relative ordering of top 20)
top_ranks = nlargest(20, ranks)
top_ranks.sort(reverse=True)

converged = False
prev_rank_compare = sys.maxsize
node_id_compare = -1

# # Debugging
# f = open("debug/log" + str(iter_num) + ".txt", "w")

if not first_iter:
    converged = True
    for _, node_id in top_ranks:
        prev_rank = float(prev_ranks[node_id])
        if prev_rank > prev_rank_compare:
            # f.write(prev_rank + ' for node ' + node_id + ' > ' + prev_rank_compare + ' for node ' + node_id_compare + '\n')
            converged = False
            break
        prev_rank_compare = prev_rank
        node_id_compare = node_id


# for rank, node_id in top_ranks:
#     f.write(str(rank) + ' ' + str(node_id) + '\n')
# f.close()

if last_iter or converged:
    for rank, node_id in top_ranks:
        emit('FinalRank:' + rank, node_id)
else:
    if first_iter:
        emit('Iter:', 1)
    else:
        emit('Iter:', iter_num)

    for output in lst_outputs:
        sys.stdout.write(output)
