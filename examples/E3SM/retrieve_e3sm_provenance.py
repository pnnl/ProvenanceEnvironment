'''
Created on Jun 5, 2017

@author: Bibi Raju
'''
import argparse
import urllib
import urllib2
import json
import os,sys
import binascii
from os.path import join



def reconstruct_acme_files(results,targetdir):
#    with open(results) as json_data:
    d = json.load(results)
    results = d['results']
    bindings = results['bindings']   
    for binding in bindings :
        resultline = ""
        parentdirectory = binding['parentdirectory']
        parentdir = parentdirectory["value"]
        parentdirPath = join(targetdir,parentdir)
        if not os.path.exists(parentdirPath):
            os.makedirs(parentdirPath)
        filenamedict = binding['filename']
        fw = open (join(parentdirPath,filenamedict["value"]), 'w+')
        filename = filenamedict['value']
        contents = binding['filepath']
        fileContent = contents["value"]
        if (filename.find(".gz") != -1 ):
            bcontent = binascii.unhexlify(fileContent)
            fw.write(bcontent)
        else:
            strippedContent = fileContent.decode('hex')
            strippedContent = strippedContent.decode('string_escape')
            resultline = resultline + strippedContent + "\n"
            fw.write(resultline)
        fw.close()


def add_readme_file(results,targetdir):
#    with open(results) as json_data:
    d = json.load(results)
    print(d)
    results = d['results']
    bindings = results['bindings']
    for binding in bindings :
        rdict = binding['simname']
        simname = rdict["value"]
        rdict = binding['compset']
        compset = rdict["value"]
        rdict = binding['res']
        res = rdict["value"]
        rdict = binding['github_hashkey']
        github_hashkey = rdict["value"]
        rdict = binding['machine']
        machine = rdict["value"]
        rdict = binding['compiler']
        compiler = rdict["value"]
        rdict = binding['scriptname']
        scriptname = rdict["value"]
        readme = join(targetdir,"README")
        fw = open (readme, 'w+')
        fw.write("Metadata extracted from the original simulation input deck\n\n")
        fw.write("Simulation name: " + simname + "\n")
        fw.write("Compset and resolution: " + compset + "\n" + res + "\n")
        fw.write("ACME Github hashkey:  "  + github_hashkey + "\n")
        fw.write("Machine: " + machine + "\n")
        fw.write("Compiler: " + compiler + "\n")
        fw.write("ACME Script Name: " + scriptname + "\n\n")
        fw.write("Notes on reconstructed configuration files, settings, and namelists:\n")
        fw.write("*  a copy of all harvested namelists and xml files are restored in \n")
        fw.write("   appropriate directories.\n")
        fw.write("*  additional configuration information stored in the performance_archive\n")
        fw.write("   CaseDocs subdirectories has been retained in the performance_archive.\n")
        fw.write("   These are compressed gzip txt files extracted from the original simulation.\n")
        fw.close()


def retrieve_description(simulation_name,url):
    #url = 'http://localhost:28080/proven/rest/v1/repository/sparql'

    query = """ SELECT ?simname ?compset ?res ?github_hashkey ?machine ?compiler ?scriptname 
                WHERE { 
                      GRAPH <http://provenance.pnnl.gov/ns/proven#acme> 
                           { 
                            ?subject <http://provenance.pnnl.gov/ns/proven#name>  ?simname .
                            ?subject <http://provenance.pnnl.gov/ns/proven#compset>  ?compset .
                            ?subject <http://provenance.pnnl.gov/ns/proven#res>  ?res .
                            ?subject <http://provenance.pnnl.gov/ns/proven#github_hashkey>  ?github_hashkey .
                            ?subject <http://provenance.pnnl.gov/ns/proven#machine>  ?machine .
                            ?subject <http://provenance.pnnl.gov/ns/proven#compiler>  ?compiler .
                            ?subject <http://provenance.pnnl.gov/ns/proven#script_name>  ?scriptname .                    
                            ?subject rdf:type <http://www.pnnl.gov/wfpp#Simulation> .
            """
    query = query +  '?subject <http://provenance.pnnl.gov/ns/proven#name> \"' + simulation_name  +  '"^^<http://www.w3.org/2001/XMLSchema#string>  .\n}\n}'  
    
    req = urllib2.Request(url, query)
    req.add_header("Content-Type", "text/plain")
    req.add_header("Accept","application/json")
    print query
    response = urllib2.urlopen(req)
    return response



def query_proven(simulation_name,url):

    query = """ SELECT ?simname ?idname ?filename ?parentdirectory ?filepath 
                WHERE { 
                      GRAPH <http://provenance.pnnl.gov/ns/proven#acme> 
                           { 
                            ?subject <http://provenance.pnnl.gov/ns/proven#name>  ?simname .
                            ?subject <http://www.pnnl.gov/wfpp#used> ?used .                      
                            ?subject rdf:type <http://www.pnnl.gov/wfpp#Simulation> .
            """
    query = query +  '?subject <http://provenance.pnnl.gov/ns/proven#name> \"' + simulation_name  +  '"^^<http://www.w3.org/2001/XMLSchema#string>  .\n'

    query = query + """{ SELECT DISTINCT ?filename ?parentdirectory ?idname ?filepath
                             WHERE {
                                     ?used <http://provenance.pnnl.gov/ns/proven#name>  ?idname .                                 
                                     ?used <http://provenance.pnnl.gov/ns/proven#filename>  ?filename . 
                                     ?used <http://provenance.pnnl.gov/ns/proven#parentdirectory> ?parentdirectory .
                                     ?used <http://provenance.pnnl.gov/ns/proven#filepath>  ?filepath .   
                                     ?used rdf:type <http://www.pnnl.gov/wfpp#InputDeck> .                              
                                    }
                         }
                     } 
                 }
           
             """
  
    
    req = urllib2.Request(url, query)
    req.add_header("Content-Type", "text/plain")
    req.add_header("Accept","application/json")

    print query
    response = urllib2.urlopen(req)
    return response

if (len(sys.argv) < 3):
    print "No arguments provided.  Usage:"
    print "retrieve_e3sm_provenance --simname=<Simulation Name>   --targetdir=<Location for reconstructed files> --server=<http://<hostname>:<portnumber>"
    exit(0)
    
parser = argparse.ArgumentParser(description='Return E3SM provenance and required files for rerunning simulation')
parser.add_argument('--simname', help='simulation name')
parser.add_argument('--server', help='proven server url')
parser.add_argument('--targetdir', help='destination directory of reconstructed files')
args = parser.parse_args() 
# print args.get
targetdir = args.targetdir
simname = args.simname
url = args.server
url = url + "/proven/rest/v1/repository/sparql"

response = query_proven(simname,url)
reconstruct_acme_files(response,targetdir)
response = retrieve_description(simname,url)
add_readme_file(response,targetdir)


