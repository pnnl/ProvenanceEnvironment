'''
Created on Aug 24, 2017

@author: Eric G Stephan
'''
import argparse
import sys
from os import listdir
from os.path import isfile, join, isdir
import binascii


def get_sim_input_message_header():
    fosi.write("_BEGIN_MESSAGE\n")
    fosi.write("name=DescribeSimulationInputDeckMessage\n")
    fosi.write("domain=acme\n")
    fosi.write("_END\n")
    fosi.write("#\n")

def get_desc_sim_message_header():
    fosd.write("_BEGIN_MESSAGE\n")
    fosd.write("name=DescribeSimulationMessage\n")
    fosd.write("domain=acme\n")
    fosd.write("_END\n")
    fosd.write("#\n")

def get_desc_sim_schema():
            
    fosd.write("_BEGIN_SCHEMA\n")
    fosd.write("node=wfpp:Simulation\n")
    fosd.write("column,dataType,constraint\n")
    fosd.write("name,,primaryKey\n")
    fosd.write("compset,,\n")
    fosd.write("res,,\n")
    fosd.write("machine,,\n")
    fosd.write("compiler,,\n")
    fosd.write("script_name,,\n")
    fosd.write("_END\n")
    fosd.write("#\n")
     
def get_simulation_input_schema():
            
    fosi.write("_BEGIN_SCHEMA\n")
    fosi.write("node=wfpp:Simulation\n")
    fosi.write("format=_TABLE\n")
    fosi.write("column,dataType,constraint\n")
    fosi.write("name,,primaryKey\n")
    fosi.write("prov:used,,referenceNode\n")
    fosi.write("_END\n")
    fosi.write("#\n")


def get_inputdeck_schema():
    fosi.write("_BEGIN_SCHEMA\n")
    fosi.write("node=wfpp:InputDeck\n")
    fosi.write("format=_TABLE\n")
    fosi.write("column,dataType,constraint\n")
    fosi.write("name,,primaryKey\n")
    fosi.write("type,,\n")
    fosi.write("filename,,\n")
    fosi.write("parentdirectory,,\n")
    fosi.write("filepath,FILE,\n")
    fosi.write("_END\n")

def build_desc_sim_content():
    fosd.write("_BEGIN_CONTENT\n")
    fosd.write("node=wfpp:Simulation\n")
    fosd.write("name="  + find_simulation_name(rootdir) + "\n")
    fosd.write("compset=" + get_compset(rootdir) + "\n")
    fosd.write("res=" + get_res(rootdir) + "\n")
    fosd.write("github_hashkey="+ get_githubhash(rootdir) + "\n")
    fosd.write("machine="+ get_machine(rootdir) + "\n")
    fosd.write("compiler=" + get_compiler(rootdir) + "\n")
    fosd.write("script_name=" + find_run_acme_name(rootdir) + "\n")
    fosd.write("_END\n")
    fosd.write("#\n")

def build_simulation_input_content():
    fosi.write("_BEGIN_CONTENT\n")
    fosi.write("node=wfpp:Simulation\n")  
    simulation= find_simulation_name(rootdir)
    simroot =  rootdir + "/" +simulation + "/run"

    fosi.write("name" + "," + "prov:used\n")
    onlyfiles = [f for f in listdir(simroot) if isfile(join(simroot, f))]
    for element in onlyfiles:
        element = str(element)
        if (element.find("_in") != -1) :
            fosi.write(simulation + ",wfpp:InputDeck?name=" + simulation + element + "\n")

    simroot =  rootdir + "/" +simulation + "/case_scripts"
    onlyfiles = [f for f in listdir(simroot) if isfile(join(simroot, f))]
    for element in onlyfiles:
        element = str(element)
        if (element.find("user_nl") != -1) :
            fosi.write(simulation + ",wfpp:InputDeck?name=" + simulation + element + "\n")
                        
    simroot =  rootdir + "/" +simulation + "/case_scripts"
    onlyfiles = [f for f in listdir(simroot) if isfile(join(simroot, f))]
    for element in onlyfiles:
        element = str(element)
        if (element.find(".xml") != -1) :
            fosi.write(simulation + ",wfpp:InputDeck?name=" + simulation + element + "\n")

    #
    #  Find the settings directory
    #
    perfdir = find_performance_archive_vars_dir(rootdir)    
    onlyfiles = [f for f in listdir(perfdir) if isfile(join(perfdir, f))]
    for element in onlyfiles:
        element = str(element)
    
        if ((element.find(".gz") != -1) and ((element.find("env_build") != -1) or (element.find("env_run") != -1) or (element.find("software_env") != -1))):
            fosi.write(simulation + ",wfpp:InputDeck?name=" + simulation + element + "\n")

    fosi.write("_END\n")
    fosi.write("#\n")

def build_inputdeck_content():
    fosi.write("_BEGIN_CONTENT\n") 
    fosi.write("node=wfpp:InputDeck\n" )
    simulation= find_simulation_name(rootdir)
    parentdir = "run"
    simroot = join(simulation,parentdir)
    simroot = join(rootdir,simroot)
    fosi.write("name" + ","  + "type" + "," + "filename" +  "," + "parentdirectory" + "," + "filepath\n")
    onlyfiles = [f for f in listdir(simroot) if isfile(join(simroot, f))]
    for element in onlyfiles:
        element = str(element)
        if (element.find("_in") != -1) :
            type = "namelist"
            filecontents = get_filelob(join(simroot,element),False)
            fosi.write(simulation + element +  "," + type + ","  + element + "," + parentdir + "," + filecontents + "\n")

    parentdir = "case_scripts"
    simroot = join(rootdir,simulation)
    simroot = join(simroot,parentdir)
    onlyfiles = [f for f in listdir(simroot) if isfile(join(simroot, f))]
    for element in onlyfiles:       
        if (element.find("user_nl") != -1) :
            type = "namelist"
            filecontents = get_filelob(simroot + "/" + element, False)
            fosi.write(simulation + element  + ","  + type + "," + element + "," + parentdir + "," + filecontents + "\n")

    
    parentdir = "case_scripts"    
    type = "settings"
    simroot = join(rootdir,simulation)
    simroot = join(simroot,parentdir)
    onlyfiles = [f for f in listdir(simroot) if isfile(join(simroot, f))]
    for element in onlyfiles:
        element = str(element)
    
        if (element.find(".xml") != -1) :
            type = "settings"
            filecontents = get_filelob(join(simroot,element),False)
            fosi.write(simulation + element  + ","  + type + "," +element + "," + parentdir + "," + filecontents + "\n")

    #
    #  Find the settings directory
    #

    perfdir = find_performance_archive_vars_dir(rootdir)    
    onlyfiles = [f for f in listdir(perfdir) if isfile(join(perfdir, f))]
    for element in onlyfiles:
        element = str(element)
    
        if ((element.find(".gz") != -1) and ((element.find("env_build") != -1) or (element.find("env_run") != -1) or (element.find("software_env") != -1))):
            type = "compressed archive"
            filecontents = get_filelob(join(perfdir,element),True)
            fosi.write(simulation + element  + ","  + type + "," +element + "," + "performance_archive" + "," + filecontents + "\n")  
    fosi.write("_END\n")

#
# Methods for associating input files to simulation.
#    


def find_performance_archive_vars_dir(rootdir):
    perf_dir = join(rootdir,"performance_archive")

    perf_dir_lvl1 = ""
    onlydirs = [d for d in listdir(perf_dir) if isdir(join(perf_dir, d))]
    for element in onlydirs:
            perf_dir_lvl1 = join(perf_dir,element)
            break  
         
    perf_dir_lvl2 = join(perf_dir_lvl1, find_simulation_name(rootdir))
    perf_dir_lvl3 = ""
    onlydirs = [d for d in listdir(perf_dir_lvl2) if isdir(join(perf_dir_lvl2, d))]
    for element in onlydirs:
            perf_dir_lvl3 = join(perf_dir_lvl2,element)
            break
        
    perf_dir_lvl4 = ""
    onlydirs = [d for d in listdir(perf_dir_lvl3) if isdir(join(perf_dir_lvl3, d))]
    for element in onlydirs:
            perf_dir_lvl4 = join(perf_dir_lvl3,element)
            break
    
                                   
    return perf_dir_lvl4
#
# Methods for extracting simulation descriptive information
#
def get_githubhash (rootdir):
    acme_github_hash = join(rootdir,find_simulation_name(rootdir))
    acme_github_hash = join(acme_github_hash,"build")
    acme_github_hash = join(acme_github_hash,"GIT_DESCRIBE")
    f = open(acme_github_hash,'r')
    line = f.readline()
    hash = str(line)
    hash = hash.strip('\n')
    f.close()
    return hash


def get_compset(rootdir):
    case_scripts_readme = join(rootdir,find_simulation_name(rootdir))
    case_scripts_readme = join(case_scripts_readme,"case_scripts")
    case_scripts_readme = join(case_scripts_readme,"README.case")
    f = open(case_scripts_readme,'r')
    line = f.readline()
    ctokens = line.split("--compset ")
    compset_buff = ctokens[1]
    compset_tokens = compset_buff.split("--")
    compset = compset_tokens[0]
    f.close()
    return compset   

def get_res(rootdir):
    case_scripts_readme = join(rootdir,find_simulation_name(rootdir))
    case_scripts_readme = join(case_scripts_readme,"case_scripts")
    case_scripts_readme = join(case_scripts_readme,"README.case")
    f = open(case_scripts_readme,'r')
    line = f.readline()
    rtokens = line.split("--res ")
    res_buff = rtokens[1]
    res_tokens = res_buff.split(" --pecount")
    res = res_tokens[0]
    f.close()
    return res

def get_machine(rootdir):
    mach = ""
    envfile = join(rootdir,find_simulation_name(rootdir))
    envfile = join(envfile,"case_scripts")
    envfile = join(envfile,"env_case.xml")
    f = open(envfile, 'r')
    for line in f:
        if (line.find('<entry id="MACH" value=') != -1):
            tokens = line.split('<entry id=\"MACH\" value=\"')
            tokens2 = tokens[1].split('"')
            mach = tokens2[0]
            break
    f.close()
    return mach

def get_compiler(rootdir):
    mach = ""
    envfile = join(rootdir,find_simulation_name(rootdir))
    envfile = join(envfile,"case_scripts")
    envfile = join(envfile,"env_build.xml")
    f = open(envfile, 'r')
    for line in f:
        if (line.find('<entry id="COMPILER" value=') != -1):
            tokens = line.split('<entry id=\"COMPILER\" value=\"')
            tokens2 = tokens[1].split('"')
            mach = tokens2[0]
            break
    f.close()
    return mach

def find_run_acme_name(rootdir):
    result = ""
    parentdir = join(rootdir,find_simulation_name(rootdir))
    parentdir = join(parentdir,"case_scripts")
    parentdir = join(parentdir,"run_script_provenance")
    onlyfiles = [f for f in listdir(parentdir) if isfile(join(parentdir, f))]
    for element in onlyfiles:
        if (element.find("run_acme") != -1):
            return element
    return result

if (len(sys.argv) < 2):
    print "No arguments provided.  Usage:"
    print "collect_e3sm_provenance --e3smdir=<e3sm simulation top level directory>  --outputdir=<output target directory>"
    exit(0)

#
# General methods to build messages
#

def get_filelob(dirpath, isBinary):
    fbr = open(dirpath,'rb')
    results = binascii.hexlify(fbr.read())

    fbr.close()
    return results


    
def find_simulation_name(rootdir):
    result = ""
    onlydirs = [f for f in listdir(rootdir) if isdir(join(rootdir, f))]
    for element in onlydirs:
        if (element.find("performance_archive") == -1 ):
            return element
        else:
            pass
    return result

    

parser = argparse.ArgumentParser(description='Extract provenancefr om acme simulation and produce messages')
parser.add_argument('--acmedir', help='acme simulation top directory')
parser.add_argument('--outputdir', help='directory where messages are produced')

args = parser.parse_args()
# print args.get

rootdir = args.e3smdir
outdir = args.outputdir

fosd = open(join(outdir,"exported_e3sm_metadata_msg.proven.csv"),'w')
fosi = open(join(outdir,"exported_e3sm_input_files_msg.proven.csv"),'w')

##
## Build message that describes information about the simualtion
##
get_desc_sim_message_header()
get_desc_sim_schema()
build_desc_sim_content()
print "Writing..." + join(outdir,"exported_e3sm_metadata_msg.proven.csv")

##
## Build message that builds relationships between the simulation and file used by the simulation.
##
get_sim_input_message_header()
get_simulation_input_schema()
get_inputdeck_schema()
build_simulation_input_content()
build_inputdeck_content()
print "Writing..." + join(outdir,"exported_e3sm_input_files_msg.proven.csv")
fosi.close()
fosd.close()