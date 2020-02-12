#!/usr/bin/env python

import sys

# lines = []
#
# for line in sys.stdin:
#     lines.append(line)
#
# for line in lines[:20]:
#     node_id = int(line.split('\t')[0][len('NodeId:'):])
#
#     sys.stdout.write('FinalRank:1.0\t' + str(node_id) + '\n')

def emit(key, value):
    sys.stdout.write(str(key) + '\t' + str(value) + '\n')


first_iter = True

for line in sys.stdin:
    if 'Iter:' in line:
        first_iter = False
        iter_num = int(line.split('\t')[1]) + 1
        if iter_num == 50:
            # Only print top 20 (should we do it in process_map?)
            pass
            break
        else:
            sys.stdout.write('Iter:', iter_num + 1)
    else:
        sys.stdout.write(line)

if first_iter:
    emit('Iter:', 1)
