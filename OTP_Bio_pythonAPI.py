# This script use the opentargets API to get Target and disease association information.

# ---- Importing required library------------- 
# argparse: makes it easy to write user friendly command line interface. More info (https://docs.python.org/3/library/argparse.html)
# opentarget: an official python client for the Open Targets REST API. More inf (https://opentargets.readthedocs.io/en/stable/)
# pandas: data wrangle and analysis. More info (https://pypi.org/project/pandas/)

import argparse 
from opentargets import OpenTargetsClient
import pandas as pd
ot = OpenTargetsClient()


# function to find the association for target id or disease id.  
def association(self):
    count = 0
    for asso in self:
        print("Target ID:", asso['target']['id'],"\t", "Disease ID:", asso['disease']['id'],"\t", "Association_score Overall:", asso['association_score']['overall'])
        count = count+1
    print("\nTotal Number of Associaton: ", count)


# function to compute related statistics using "association_score.overall".         
def stat_ana(self):
    print("\tMAXIMUM association_score.overall is : ", self['association_score.overall'].max())
    print("\tMINIMUM association_score.overall is : ", self['association_score.overall'].min())
    print("\tAVERAGE association_score.overall is : ", self['association_score.overall'].mean())
    print("\tSTANDARD DEVIATION association_score.overall is : ", self['association_score.overall'].std(), "\n\n")


# First create the parser and then add the required argument. Here argument --target and --disease were used.
parser = argparse.ArgumentParser(description='This script use opentarget python client to compute the association of target and drug based on target id (for example: ENSG00000197386) and disease id (for example: Orphanet_399) and output the result on the terminal window. To use the script it is required to provide -t/--target target_id or -d/--disease disease id. It can be possible to save the result on the file using python3 script.py -t/-d target_id/disease_id > filename.dat.')

parser.add_argument("-t", "--target", help="Type your target ID after -t or --target. For example python3 test.py -t target_id")
parser.add_argument("-d", "--disease", help="Type your disease ID after -d or --disease. For example python3 test.py -d disease_id")


# Parse, Validate and Print the result on the terminal
args = parser.parse_args()

if not (args.target or args.disease):
   parser.error('Please provide input for target id (-t) or disease id (-d)')  


# Check input and parse accordingly. 
# if input is -t/--target then ot(OpenTargetsClient) is called and find the association for target with the input id for example: ENSG00000197386. After this the function "association(self)" is called to output Target association information.
if args.target:
   asso_target = ot.get_associations_for_target(args.target)
   print("\n Association for Target, Query With Target ID:", args.target,"\n")
   association(asso_target)


# Create the pandas dataframe which make it easier to compute statistics.
# Once pandas dataframe for Target is created, the function stat_ana(self) is called to output various statistics.
   response = ot.get_associations_for_target(args.target, fields=['association_score.overall'])
   target_df = response.to_dataframe()
   print("\nStatistic Based on \"association_score.overall\" for Target Query With Target ID:", args.target,"\n")
   stat_ana(target_df)


# else input is -d/--disease then ot(OpenTargetsClient) is called and find the association for disease with the input id for example: Orphanet_399. After this the function "association(self)" is called to output Disease association information.
else:
   asso_disease = ot.get_associations_for_disease(args.disease)
   print("\n Association for Disease, Query With Disease ID:", args.disease,"\n")
   association(asso_disease)


# Once pandas dataframe for Disease is created, the function stat_ana(self) is called to output various statistics.
   response = ot.get_associations_for_disease(args.disease, fields=['association_score.overall'])
   disease_df = response.to_dataframe()
   print("\nStatistic Based on \"association_score.overall\" for Disease Query With Disease ID:", args.disease,"\n")
   stat_ana(disease_df)
