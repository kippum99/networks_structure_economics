#!/usr/bin/env python

import sys
from heapq import nlargest


def emit(key, value):
    sys.stdout.write(str(key) + '\t' + str(value) + '\n')


first_iter = True
last_iter = False

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
            emit('Iter:', iter_num)
    else:
        # For iterations < 50
        lst_outputs.append(line)

        # For iteration 50
        node_id, info = line.strip('\n').split('\t')
        node_id = node_id[len('NodeId:'):]
        info = info.split(',')
        rank = info[0]
        ranks.append((rank, node_id))

if last_iter:
    top_ranks = nlargest(20, ranks)
    top_ranks.sort(reverse=True)
    # top_ranks = sorted(ranks, reverse=True)[:20]

    for rank, node_id in top_ranks:
        emit('FinalRank:' + rank, node_id)
else:
    if first_iter:
        emit('Iter:', 1)

    for output in lst_outputs:
        sys.stdout.write(output)
