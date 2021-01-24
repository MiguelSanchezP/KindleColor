import os
import qrcode

ncx_file = ''

for root, dirs, files in os.walk('.'):
	for file in files:
		if file.endswith('.ncx'):
			ncx_file = os.path.join(root, file)

print (ncx_file)

f = open(ncx_file, 'r')

lines = []

for line in f:
	if line.strip().startswith('<content'):
		lines.append(line.strip())

print (lines[0])
