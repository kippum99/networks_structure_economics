import os

# test_file = '../local_test_data/EmailEnron.txt'
# test_file = '../local_test_data/GNPn100p05.txt'
test_file = '../local_test_data/Gnutella.txt'

os.system('python2 pagerank_map.py < ' + test_file + ' | sort | \
            python2 pagerank_reduce.py | python2 process_map.py | sort | \
            python2 process_reduce.py > outputs/output1.txt')

for i in range(2, 51):
    os.system('python2 pagerank_map.py < outputs/output' + str(i - 1)
                + '.txt | sort | \
                python2 pagerank_reduce.py | python2 process_map.py | sort | \
                python2 process_reduce.py > outputs/output' + str(i) + '.txt')
