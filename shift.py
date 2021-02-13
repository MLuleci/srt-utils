#!/usr/bin/python
# Reference: https://docs.fileformat.com/video/srt/

import sys
import re
import os

def fit(x):
	return map(lambda x: int(x), re.split(':|,',x))

def tif(x):
	return '{0:02d}:{1:02d}:{2:02d},{3:02d}'.format(*x)

def add(x,y):
	N = len(x)
	M = (100,100,100,1000)
	k = [0,0,0,0]
	carry = 0
	for i in range(N-1,-1,-1):
		z = x[i] + y[i]
		if carry != 0:
			z = z + carry
			carry = 0
		if z < 0:
			z = M[i] + z
			carry = -1
		if z >= M[i]:
			z = z % M[i]
			carry = 1
		k[i] = z
	if carry != 0:
		print 'Warning: overflow'
	return k

if len(sys.argv) < 4:
	print 'Usage: {} <input> <output> [+|-]<offset>'.format(sys.argv[0])
	print 'NOTE: Offset must have format \'hh:mm:ss,uuu\''
	print 'Optional +/- prefix changes offset direction'
	sys.exit(0)

inp = None
out = None
try:
	inp = open(sys.argv[1])
	out = open(sys.argv[2],'w')
	pfx = sys.argv[3][0]
	if pfx == '-':
		off = map(lambda x: -x, fit(sys.argv[3][1:]))
	elif pfx == '+':
		off = fit(sys.argv[3][1:])
	else:
		off = fit(sys.argv[3])
	

	for line in inp:
		sep = line.split(' --> ')
		if len(sep) > 1:
			beg = tif(add(fit(sep[0]), off))
			end = tif(add(fit(sep[1]), off))
			out.write(beg + ' --> ' + end + os.linesep)
		else:
			out.write(line)
except IOError, ex:
	print ex
finally:
	if inp:
		inp.close()
	if out:
		out.close()
