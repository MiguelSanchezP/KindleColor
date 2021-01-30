import os
import qrcode

ncx_file = ''

for root, dirs, files in os.walk('.'):
	for file in files:
		if file.endswith('.ncx'):
			ncx_file = os.path.join(root, file)

#print (ncx_file)

f = open(ncx_file, 'r')

lines = []
for line in f:
	if line.strip().startswith('<content'):
		lines.append(line.strip())
f.close()

#print (lines[0])

paths = []

for line in lines:
	paths.append(line.split('"')[1])

#print (paths)

paths_def = []

for path in paths:
	for root, dirs, files in os.walk('.'):
		for file in files:
			if file.endswith(path.split('/')[len(path.split('/'))-1]):
				paths_def.append(os.path.join(root, file))

image_entries = []
for p in paths_def:
#	print ('-------------------------------------------------------------------')
#	print (p)
#	print ('-------------------------------------------------------------------')
	f = open(p, 'r')
	lines= f.readlines()
	for line in lines: #f:
#		print (line)
		if '<img' in line:
#			print ('here')
			image_entries.append([p, line])
#			print (line)
	f.close()

image_paths = []
for i in image_entries:
	image_paths.append(i[1].split('src="')[1].split('"')[0])
#	print (i[1].split('src="')[1].split('"')[0])

final_image_paths = []
for i in range(len(image_paths)):
	if (i+1) < len (image_paths):
		if image_paths[i] == image_paths[i+1]:
			continue
		else:
			final_image_paths.append(image_entries[i][0])
	else:
		final_image_paths.append(image_entries[i][0])

final_image_entries = []
for i in range(len(image_entries)):
	if (i+1) < len(image_entries):
		if image_entries[i][1].split('src="')[1].split('"')[0] == image_entries[i+1][1].split('src="')[1].split('"')[0]:
			continue
		else:
			final_image_entries.append(image_entries[i][1])
	else:
		final_image_entries.append(image_entries[i][1])

j=0
#print (final_image_entries)
#print ('----------------------------------------------')

for i in range(len(final_image_paths)):
#	print ('Path to open: ' + final_image_paths[i])
	f = open(final_image_paths[i], 'r')
#	file_lines = []
	file_lines = f.readlines()
	f.close()
	f = open(final_image_paths[i], 'w')
#	j = 0
#	print (file_lines)
#	print ('EEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE')
	for line in file_lines:
		f.write(line)
		if j < len(final_image_entries):
			if line == final_image_entries[j]:
				f.write('ATTENTION. HERE GOES A CAPTION :)\n')
				j = j+1
	f.close()

