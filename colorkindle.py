import os
import qrcode
import subprocess
import shutil
from datetime import datetime

current_date = datetime.now().strftime('%S%M%H%d%m%Y')

path = input ('Add the relative path (from this location) to the book: ./')
print ('\nExtract the book contents')
subprocess.call('unzip -d tmp ./' + path, shell=True)

ncx_file = ''

for root, dirs, files in os.walk('./tmp'):
	for file in files:
		if file.endswith('.ncx'):
			ncx_file = os.path.join(root, file)

f = open(ncx_file, 'r')

lines = []
for line in f:
	if line.strip().startswith('<content'):
		lines.append(line.strip())
f.close()

paths = []

for line in lines:
	paths.append(line.split('"')[1])

paths_def = []

for path in paths:
	for root, dirs, files in os.walk('./tmp'):
		for file in files:
			if file.endswith(path.split('/')[len(path.split('/'))-1]):
				paths_def.append(os.path.join(root, file))

image_entries = []
for p in paths_def:
	f = open(p, 'r')
	lines= f.readlines()
	for line in lines:
		if '<img' in line:
			image_entries.append([p, line])
	f.close()

image_paths = []
for i in image_entries:
	image_paths.append(i[1].split('src="')[1].split('"')[0])

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
path = "/".join(final_image_paths[0].split('/')[0:(len(final_image_paths[0].split('/'))-1)])
print (path)
f = open (final_image_paths[0], 'r')
head = f.readlines()
f.close()
f2 = open (path + "/qrcodes.xhtml", 'w+')
i = 0
while not '</head>' in head[i]:
	f2.write(head[i])
	i = i+1
f2.write ('</head>\n\n')
f2.write ('<body>\n')
os.mkdir (path + "/qrcodes/")
for i in range(len(final_image_paths)):
	f = open(final_image_paths[i], 'r')
	file_lines = f.readlines()
	f.close()
	f = open(final_image_paths[i], 'w')
	for line in file_lines:
		f.write(line)
		if j < len(final_image_entries):
			if line == final_image_entries[j]:
				filename = final_image_paths[i].split('/')[len(final_image_paths[i].split('/'))-1]
				image = line.split('src="')[1].split('"')[0].split('/')[len(line.split('src="')[1].split('"')[0].split('/'))-1]
				f.write('<p><sup><a href="qrcodes.xhtml#' + image + '" id="' + image + '">qr</a></sup></p>\n')
				f2.write('<p><a href="' + filename + '#' + image + '" id="' + image + '">back</a><img src="qrcodes/' + image + '.png"/></p>\n')
				gqr = qrcode.make('domain/kindleimages/'+ current_date + '/' + image)
				gqr.save(path+'/qrcodes/'+image+'.png')
				j = j+1
	f.close()
f2.write ('</body>\n')
f2.write ('</html>')
f2.close()
new_book_name = input ('Write the name of the book to export: ')
print ('Zip back the contents')
subprocess.call('zip -X -r ' + new_book_name + ' ./tmp/mimetype ./tmp/*', shell=True)
print ('Upload the contents to the server')
subprocess.call('find . -name ' + image + ' > .output.txt', shell=True)
f = open('.output.txt', 'r')
image_directory = ''
for line in f:
	image_directory = '/'.join(line.split('/')[0:len(line.split('/'))-1])
f.close()
subprocess.call('ssh alias@server -t "mkdir /home/user/BookUploads/' + current_date + '/"', shell=True)
subprocess.call('scp -r ' + image_directory + '/* alias@server:/home/user/BookUploads/' + current_date + '/', shell=True)
shutil.rmtree('./tmp/')
