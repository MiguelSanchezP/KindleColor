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
f.close()

print (lines[0])

paths = []

for line in lines:
	paths.append(line.split('"')[1])

print (paths)

paths_def = []

for path in paths:
	for root, dirs, files in os.walk('.'):
		for file in files:
			if file.endswith(path.split('/')[len(path.split('/'))-1]):
				paths_def.append(os.path.join(root, file))

image_entries = []
for p in paths_def:
	print (p)
	f = open(p, 'r')
	for line in f:
		if line.strip().startswith('<img'):
			image_entries.append(line.strip())
			print (line.strip())

