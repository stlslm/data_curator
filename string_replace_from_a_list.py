''' The huge text file (~1.3GB) to be read as one string
'''
string_file = "docs/trainval.json"

''' List contains all the sub-string to be found in the huge string_file
'''
list_file = "docs/png_renamed_images.txt"
with open(list_file, 'r') as f:
    lines = f.readlines()
    lines = [l.strip() for l in lines]

with open(string_file, 'r') as f:
    data = f.read()

cnt=0
for f_jpg in lines:
    f_png = f_jpg.replace('.jpg','.png')
    data = data.replace(f_jpg, f_png)
    cnt+=1

print('There are total {} replacements.'.format(cnt))
print('Done.')