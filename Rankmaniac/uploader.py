"""
Utility to execute map-reduce jobs on Amazon EMR.

Written for the Rankmaniac competition
for CMS/CS/EE 144: Networks: Structure & Economics
at the California Institute of Technology.

Authored by: Max Hirschhorn (maxh@caltech.edu)
Edited by: Fabian Boemer (fboemer@caltech.edu)
"""

from __future__ import with_statement # for Python 2.5

import sys, os
import ConfigParser
from time import sleep
import base64

from boto.exception import EmrResponseError
from rankmaniac import Rankmaniac

unbuff_stdout = os.fdopen(sys.stdout.fileno(), 'w', 0) # unbuffered

# Vigenere cipher encoding
# See https://stackoverflow.com/questions/2490334/simple-way-to-encode-a-string-according-to-a-password
def encode(key, clear):
	enc = []
	for i in range(len(clear)):
		key_c = key[i % len(key)]
		enc_c = chr((ord(clear[i]) + ord(key_c)) % 256)
		enc.append(enc_c)
	return base64.urlsafe_b64encode("".join(enc))

# Vigenere cipher decoding
# See https://stackoverflow.com/questions/2490334/simple-way-to-encode-a-string-according-to-a-password
def decode(key, enc):
	dec = []
	enc = base64.urlsafe_b64decode(enc)
	for i in range(len(enc)):
		key_c = key[i % len(key)]
		dec_c = chr((256 + ord(enc[i]) - ord(key_c)) % 256)
		dec.append(dec_c)
	return "".join(dec)


def do_main(team_id, access_key, secret_key,
			infile='input.txt', max_iter=50):
	"""
	Submits a new map-reduce job to Amazon EMR and waits for it to
	finish executing.
	"""

	# Ensure that the input file exists
	if not os.path.isfile(os.path.join('data', infile)):
		raise Exception('file %s not found' % (infile))

	# Default modules for where to expect the pagerank step
	# and process step code
	pagerank_map = 'pagerank_map.py'
	pagerank_reduce = 'pagerank_reduce.py'
	process_map = 'process_map.py'
	process_reduce = 'process_reduce.py'

	# Read the configuration and override defaults
	config = ConfigParser.SafeConfigParser()
	config.read('data/rankmaniac.cfg')

	section = 'Rankmaniac'
	if config.has_section(section):
		pagerank_map = config.get(section, 'pagerank_map')
		pagerank_reduce = config.get(section, 'pagerank_reduce')
		process_map = config.get(section, 'process_map')
		process_reduce = config.get(section, 'process_reduce')

	# Terminates the job and closes connections upon leaving this block
	with Rankmaniac(team_id, access_key, secret_key) as r:
		r.set_infile(infile)
		print('Uploading...')
		r.upload()
		print('Uploaded')

		print('Adding %d iterations...' % (max_iter))
		for i in range(max_iter):
			while True:
				try:
					unbuff_stdout.write('.')
					r.do_iter(pagerank_map, pagerank_reduce,
							  process_map, process_reduce)
					break
				except EmrResponseError:
					sleep(10) # call Amazon APIs infrequently
		print('')

		print('Waiting for map-reduce job to finish...')
		print('  Use Ctrl-C to interrupt')
		while True:
			try:
				unbuff_stdout.write('.')
				if r.is_done():
					break
				elif not r.is_alive():
					print('')
					print("Failed to output 'FinalRank'!")
					break
				sleep(20) # call Amazon APIs infrequently
			except EmrResponseError:
				sleep(60) # call Amazon APIs infrequently
			except KeyboardInterrupt:
				print('')
				break
		print('')

		print('Terminating...')
		print('  Downloading...')
		r.download()
		print('  Downloaded')

	print('Terminated')

if __name__ == '__main__':
	
	team_id        = sys.argv[1] # 'YOUR-TEAM-ID'
	decoding_key   = sys.argv[2] # DO NOT HARD-CODE!
	access_enc_key = sys.argv[3] # DO NOT HARD-CODE!
	secret_enc_key = sys.argv[4] # DO NOT HARD-CODE!
	
	access_key = decode(decoding_key, access_enc_key)
	secret_key = decode(decoding_key, secret_enc_key)

	do_main(team_id, access_key, secret_key)
