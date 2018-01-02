import argparse
import sys
import os
import subprocess
import glob


if (len(sys.argv) < 2):
    print "No arguments provided.  Usage:"
    print "cprn_test --run1=<path to run1>  --run2=<path to run2>"
    exit(0)
parser = argparse.ArgumentParser(description='Compare netcdf files from two runs')
parser.add_argument('--run1', help='path to case1/run')
parser.add_argument('--run2', help='path to case2/run')

args = parser.parse_args()
# print args.get

run1 = args.run1
run2 = args.run2

os.chdir('/global/project/projectdirs/acme/tools/cprnc.edison')

count = 0
identical = False
file_names = os.path.join(run1, '*.nc')
for filename in glob.glob(file_names):
   
   head, tail = os.path.split(filename)
   if(tail != 'SEMapping.nc'):  
      case1 = run1.split("/")
      case2 = run2.split("/")
      casename1 = case1[len(case1)-3]
      casename2 = case2[len(case2)-3]
      c2= casename1 + '.'
      ncfilename = tail.split(c2)
      ncfile2 = casename2 + '.' + ncfilename[1]
      file1 = os.path.join(run1,tail)
      file2 = os.path.join(run2,ncfile2)
      

   if(tail == 'SEMapping.nc'):
      file1 = os.path.join(run1,tail)
      file2 = os.path.join(run2,tail)

   case = subprocess.Popen("./cprnc -v -m "+ file1 + " " + file2, shell=True, stdout=subprocess.PIPE)
   case = case.communicate()[0]
   print case
   result = case.split("diff_test: the two files seem to be ")
   
   diffcount = 0
   count = count + 1
   if(result == 'IDENTICAL'):
      identical = False
   elif(result == 'DIFFERENT'):
      identical = True
      diffcount = diffcount + 1
   
print count, 'files were compared'
print diffcount, " files are different"
if(diffcount > 0):
   exit(1)
elif(diffcount == 0):
   exit(0)
