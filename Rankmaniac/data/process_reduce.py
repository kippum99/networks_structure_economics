#!/usr/bin/env python

import math
import sys
from heapq import heappush, heapreplace


def emit(key, value):
    sys.stdout.write(str(key) + '\t' + str(value) + '\n')


# Copy of stdin
lst_outputs = []

# Min-heaps of prev and current ranks
prev_ranks_heap = []
ranks_heap = []

count = 0

for line in sys.stdin:
    # To pass to next iteration of pagerank_map
    lst_outputs.append(line)

    # Build min-heap of prev and current ranks
    node_id, info = line.strip('\n').split('\t')
    node_id = node_id[7:]   # 7 = len('NodeId:')
    info = info.split(',')
    rank, prev_rank  = info[0], info[1]

    if count < 20:
        count += 1
        heappush(prev_ranks_heap, (prev_rank, node_id))
        heappush(ranks_heap, (rank, node_id))
    else:
        if prev_rank > prev_ranks_heap[0][0]:
            heapreplace(prev_ranks_heap, (prev_rank, node_id))
        if rank > ranks_heap[0][0]:
            heapreplace(ranks_heap, (rank, node_id))

# Check convergence (relative ordering of top 20 are the same)
converged = True

prev_ranks_heap.sort(reverse=True)
ranks_heap.sort(reverse=True)

for i in range(20):
    if prev_ranks_heap[i][1] != ranks_heap[i][1]:
        converged = False
        break

# Produce outputs
if converged:
    for rank, node_id in ranks_heap:
        emit('FinalRank:' + rank, node_id)
else:
    for output in lst_outputs:
        sys.stdout.write(output)
