#!/usr/bin/env python

import sys


def emit(key, value):
    sys.stdout.write(str(key) + '\t' + str(value) + '\n')


for line in sys.stdin:
    # Just repeat line if iter number
    if 'Iter:' in line:
        sys.stdout.write(line)
        continue

    node_id, info = line.strip('\n').split('\t')
    node_id = node_id[len('NodeId:'):]
    info = info.split(',')
    rank = info[0]
    neighbors = info[2:]

    emit(node_id, 'n' + ','.join(neighbors))

    for neighbor in neighbors:
        emit(neighbor, float(rank) / len(neighbors))
