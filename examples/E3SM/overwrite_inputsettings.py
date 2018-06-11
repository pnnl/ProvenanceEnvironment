

import os, glob, shutil, subprocess

cime_output_root = subprocess.Popen("./xmlquery --value CIME_OUTPUT_ROOT", shell=True, stdout=subprocess.PIPE)
cime_output_root = cime_output_root.communicate()[0]
exeroot = subprocess.Popen("./xmlquery --value EXEROOT", shell=True, stdout=subprocess.PIPE)
exeroot = exeroot.communicate()[0]
caseroot = subprocess.Popen("./xmlquery --value CASEROOT", shell=True, stdout=subprocess.PIPE)
caseroot = caseroot.communicate()[0]
cimeroot = subprocess.Popen("./xmlquery --value CIMEROOT", shell=True, stdout=subprocess.PIPE)
cimeroot = cimeroot.communicate()[0]
srcroot = subprocess.Popen("./xmlquery --value SRCROOT", shell=True, stdout=subprocess.PIPE)
srcroot = srcroot.communicate()[0]
case = subprocess.Popen("./xmlquery --value CASE", shell=True, stdout=subprocess.PIPE)
case = case.communicate()[0]
machdir = subprocess.Popen("./xmlquery --value MACHDIR", shell=True, stdout=subprocess.PIPE)
machdir = machdir.communicate()[0]
rundir = subprocess.Popen("./xmlquery --value RUNDIR", shell=True, stdout=subprocess.PIPE)
rundir = rundir.communicate()[0]
dout_l_msroot = subprocess.Popen("./xmlquery --value DOUT_L_MSROOT", shell=True, stdout=subprocess.PIPE)
dout_l_msroot = dout_l_msroot.communicate()[0]

print(cime_output_root)
print(exeroot)
print(caseroot)
print(cimeroot)
print(srcroot)
print(case)
print(machdir)
print(rundir)
print(dout_l_msroot)


def copy_replace_files(path, file, destination):
   count = 0
   file_names = os.path.join(path, file)
   for filename in glob.glob(file_names):
       print(filename)
       shutil.copy2(filename, destination)
       count = count + 1
   print count, 'files copied'



#Copy files
copy_replace_files('/global/u2/b/bibiraju/Edison_reconstruct/case_scripts/', 'env_*.xml', caseroot)
copy_replace_files('/global/u2/b/bibiraju/Edison_reconstruct/case_scripts/', 'user_nl_*', caseroot)
copy_replace_files('/global/u2/b/bibiraju/Edison_reconstruct/run/', '*_in', rundir)



os.system("./xmlchange --id CIME_OUTPUT_ROOT --val " + cime_output_root)

os.system("./xmlchange --id EXEROOT --val " + exeroot)

os.system("./xmlchange --id CASEROOT --val " + caseroot)

os.system("./xmlchange --id CIMEROOT --val " + cimeroot)

os.system("./xmlchange --id SRCROOT --val " + srcroot)

os.system("./xmlchange --id CASE --val " + case)

os.system("./xmlchange --id MACHDIR --val " + machdir)

os.system("./xmlchange --id RUNDIR --val " + rundir)

os.system("./xmlchange --id DOUT_L_MSROOT --val " + dout_l_msroot)

