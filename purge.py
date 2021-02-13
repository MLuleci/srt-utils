#!/usr/bin/python
# [1]: https://en.wikipedia.org/wiki/Byte_order_mark#Byte_order_marks_by_encoding

import sys
import re
import os

if len(sys.argv) < 4:
	print 'Usage: {} <input> <output> [indices]'.format(sys.argv[0])
	print 'NOTE: Lowest index is 1, indices may be unordered'
	sys.exit(0)

inp = None
out = None
try:
	inp = open(sys.argv[1])
	out = open(sys.argv[2],'w')
	idx = list(map(lambda x: int(x), sys.argv[3:]))
	cur = 1

	inp.seek(3) # Skip BOM [1]
	while True:
		line = inp.readline()
		if not line:
			break
		if re.match('^\d+$',line.strip()):
			ind = int(line)
			if ind in idx:
				idx.remove(ind)
				while line.strip():
					line = inp.readline()
			else:
				out.write('{}{}'.format(cur,os.linesep))
				cur = cur + 1
		else:
			out.write(line)
except IOError, ex:
	print ex
finally:
	if inp:
		inp.close()
	if out:
		out.close()
