#!/usr/bin/env python

import sys

# Damping constant
alpha = 0.85

def emit(key, value):
    sys.stdout.write(str(key) + '\t' + str(value) + '\n')


# Dictionary mapping node_id to [rank, info_string] where info_string is
# a string format of prev rank + neighbors
node_map = {}

for line in sys.stdin:
    # Just repeat line if iter number
    if 'Iter:' in line:
        sys.stdout.write(line)
        continue

    node_id, info = line.strip('\n').split('\t')

    if node_id not in node_map:
        node_map[node_id] = [0, '']

    if info[0] == 'i':
        node_map[node_id][1] = info[1:]
    else:
        node_map[node_id][0] += float(info)

for node_id in node_map:
    rank, info = node_map[node_id]
    rank = (1 - alpha) + alpha * rank
    emit('NodeId:' + node_id, str(rank) + ',' + info)
