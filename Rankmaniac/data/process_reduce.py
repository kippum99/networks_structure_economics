#!/usr/bin/env python

import math
import sys
from heapq import nlargest


def emit(key, value):
    sys.stdout.write(str(key) + '\t' + str(value) + '\n')

# Threshold for max squared diff in ordering (convergence testing)
penalty_tolerance = 20

first_iter = True
last_iter = False
num_nodes = 0
iter_num = 0

# Copy of stdin
lst_outputs = []

# List of tuples (rank, node_id)
ranks = []
prev_ranks = []

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
        prev_ranks.append((prev_rank, node_id))

        num_nodes += 1

# Check convergence (relative ordering of top 20)
converged = False

if not first_iter:
    top_ranks = nlargest(25, ranks)
    top_ranks.sort(reverse=True)

    # Top 25 previous ranks
    top_prev_ranks = nlargest(25, prev_ranks)
    top_prev_nodes_set = set(pair[1] for pair in top_prev_ranks)

    converged = True

    # Check if top 20 of current ranks are within top 25 of prev ranks
    for _, node_id in top_ranks:
        if node_id not in top_prev_nodes_set:
            converged = False
            break

    # If all top 20 of current ranks are within top 25 of prev ranks,
    # compute squared difference in ordering
    if converged:
        top_prev_ranks.sort(reverse=True)

        # Dictionary mapping node_id to prev_ordering
        prev_ordering = {}

        for i, (_, node_id) in enumerate(top_prev_ranks):
            prev_ordering[node_id] = i

        # Compute squared difference in ordering
        sum_squared_diff = 0

        for i, (_, node_id) in enumerate(top_ranks):
            diff = i - prev_ordering[node_id]
            sum_squared_diff += diff ** 2

        converged = sum_squared_diff <= penalty_tolerance

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
