# This script use the opentargets RESTAPI to get Target and disease association information.
#

# ---- Importing required library------------- 
# request: allows to send HTTP requests easily and efficiently.
# argparse: makes it easy to write user friendly command line interface. More info (https://docs.python.org/3/library/argparse.html)
# pandas: data wrangle and analysis. More info (https://pypi.org/project/pandas/)


import requests
import argparse
import pandas as pd

# function to compute related statistics using "association_score.overall".  
def stat_ana(self):
    print("\tMAXIMUM association_score.overall is : ", self['Association_score_Overall'].max())
    print("\tMINIMUM association_score.overall is : ", self['Association_score_Overall'].min())
    print("\tAVERAGE association_score.overall is : ", self['Association_score_Overall'].mean())
    print("\tSTANDARD DEVIATION association_score.overall is : ", self['Association_score_Overall'].std(), "\n\n")

# function to get the target id as name and number of associated record in database to compute target id, disease id and association score overall.
# can be possible to add various fields based on the needs.
def asso_target(name, no_record):
    fields = ['target.id', 'disease.id','association_score.overall']
    payload = {'size': no_record, 'target':name, 'association_score':['overall'],'fields':fields}
    response = requests.post('https://platform-api.opentargets.io/v3/platform/public/association/filter?', json=payload)
    for result in response.json()['data']:
        yield (result['target']['id'], result['disease']['id'], result['association_score']['overall'])

# function to get the disease id as name and number of associated record in database to compute target id, disease id and association score overall.
# can be possible to add various fields based on the needs.
def asso_disease(name, no_record):
    fields = ['target.id', 'disease.id','association_score.overall']
    payload = {'size': no_record, 'disease':name, 'association_score':['overall'],'fields':fields}
    response = requests.post('https://platform-api.opentargets.io/v3/platform/public/association/filter?', json=payload)
    for result in response.json()['data']:
        yield (result['target']['id'], result['disease']['id'], result['association_score']['overall'])


# First create the parser and then add the required argument. Here argument --target and --disease were used.
parser = argparse.ArgumentParser(description='This script use open target RESTAPI to compute the association of target and drug based on target id (for example: ENSG00000197386) and disease id (for example: Orphanet_399) and output the result on the terminal window. To use the script it is required to provide -t/--target target_id or -d/--disease disease id. It can be possible to save the result on the file using python3 script.py -t/-d target_id/disease_id > filename.dat.')

parser.add_argument("-t", "--target", help="Type your target ID after -t or --target. For example python3 test.py -t target_id")
parser.add_argument("-d", "--disease", help="Type your disease ID after -d or --disease. For example python3 test.py -d disease_id")


# Parse, Validate and Print the result on the terminal
args = parser.parse_args()
if not (args.target or args.disease):
   parser.error('Please provide input for target id (-t) or disease id (-d)')


# Check input and parse accordingly. 
# if input is -t/--target then ot(OpenTargetsClient) is called and find the association for target with the input id for example: ENSG00000197386. After this the function "association(self)" is called to output Target association information.
if args.target:
  paylod= {'target':[args.target]}
  r = requests.post("https://platform-api.opentargets.io/v3/platform/public/association/filter", json=paylod)
  no_record = r.json()['total']
  #no_record = 10
  cols = ['Target_ID', 'Disease_ID', 'Association_score_Overall']
  target_asso = pd.DataFrame(asso_target([args.target], no_record), columns=cols)
  print("\n Association for Target, Query With Target ID:", args.target,"\n")

# To print the pd dataframe and make the format similar to the output while using python client for opentarget.
  for i in target_asso.index:
      print("Target ID:", target_asso['Target_ID'][i],"\t", "Disease ID:", target_asso['Disease_ID'][i],"\t", "Association_score Overall:", target_asso['Association_score_Overall'][i])
  print("\nTotal Number of Associaton: ", no_record)

  print("\nStatistic Based on \"association_score.overall\" for Target Query With Target ID:", args.target,"\n")
  stat_ana(target_asso)

# else input is -d/--disease then ot(OpenTargetsClient) is called and find the association for disease with the input id for example: Orphanet_399. After this the function "association(self)" is called to output Disease association information.
else:
  paylod= {'disease':[args.disease]}
  r = requests.post("https://platform-api.opentargets.io/v3/platform/public/association/filter", json=paylod)
  no_record = r.json()['total']
  cols = ['Target_ID', 'Disease_ID', 'Association_score_Overall']
  disease_asso = pd.DataFrame(asso_disease([args.disease], no_record), columns=cols)
  print("\n Association for Disease, Query With Disease ID:", args.disease,"\n")
  for i in disease_asso.index:
      print("Target ID:", disease_asso['Target_ID'][i],"\t", "Disease ID:", disease_asso['Disease_ID'][i],"\t", "Association_score Overall:", disease_asso['Association_score_Overall'][i])
  print("\nTotal Number of Associaton: ", no_record)
  print("\nStatistic Based on \"association_score.overall\" for Disease Query With Disease ID:", args.disease,"\n")
  stat_ana(disease_asso)
