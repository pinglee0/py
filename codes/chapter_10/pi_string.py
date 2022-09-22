filename = 'pi_million_digits1.txt'

with open(filename,"r+") as file_object:
    data=file_object.read(100)
    lines = file_object.readlines()
    file_object.write("12333\n")
# file_object.write("\n\n\n\n\n")
pi_string = ''
for line in lines:
    pi_string += line.strip()
file2=open(filename,"r+")
for a in file2:
    print (a)
file2.close()
print(f"{pi_string[:152]}...")
print(len(pi_string))
aa="adasd\n"
print(aa)
print(data)

fname = input('Enter the file name:  ')
try:
   fhand = open(fname)
except:
   print ('File cannot be opened:', fname)
   exit()

count = 0
for line in fhand:
   if line.startswith('Subject:') :
      count = count + 1
print ('There were', count, 'subject lines in', fname)
