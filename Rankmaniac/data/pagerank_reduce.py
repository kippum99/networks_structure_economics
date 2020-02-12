#!/usr/bin/env python

import sys

def emit(key, value):
    sys.stdout.write(str(key) + '\t' + str(value) + '\n')


# Dictionary mapping node_id to [rank, neighbors] (in string format)
node_map = {}

for line in sys.stdin:
    # Just repeat line if iter number
    if 'Iter:' in line:
        sys.stdout.write(line)
        continue

    node_id, info = line.strip('\n').split('\t')

    if node_id not in node_map:
        node_map[node_id] = [0, None]

    if info[0] == 'n':
        node_map[node_id][1] = info[1:]
    else:
        node_map[node_id][0] += float(info)

for node_id in node_map:
    rank, neighbors = node_map[node_id]
    emit('NodeId:' + node_id, str(rank) + ',,' + neighbors)
