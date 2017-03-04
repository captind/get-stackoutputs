#CloudFormation Outputs Collector. An alternative to static release notes.
#Retrieves outputs for a set of environment stacks and writes them to a csv file.
#Usage example get-stackouts.py -environment "dev01" -outputpath c:/
#Author: Jonathan Rudge

import boto.cloudformation
import re
import csv
import time
import argparse

parser = argparse.ArgumentParser(description='Clouformation Outputs Exporter.')
parser.add_argument('-e','--environment', help='Target Environment Name e.g. dev01',required=True)
parser.add_argument('-o','--output_path',help='Path to write output to, must use forward slashed for paths', required=True)
args = parser.parse_args()

env = args.environment
output_path = args.output_path

regex = r"^(?i)st.*\w(?i)" + re.escape(env) + r"\b(?!\w)"
generationtime = time.strftime("%Y%m%d-%H%M%S")
filename = output_path + 'test' + env + generationtime + '.csv'

with open( filename , 'wb') as csvfile:
    fieldnames = ['stack_name', 'ouptut_name', 'output_value']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    conn = boto.cloudformation.connect_to_region('eu-west-1')  # or your favorite region
    stacks = conn.describe_stacks()
    for stack in stacks:
        if re.match(regex, stack.stack_name): 
            print('=================================================')
            print('Stack Name: %s' % (stack.stack_name))
            print('=================================================')
            print('Outputs:')
            print('==========')      
            for output in stack.outputs:           
                print('%s: %s' % (output.key, output.value))             
                writer.writerow({'stack_name': 'stack.stack_name', 'ouptut_name': output.key, 'output_value': output.value })
            print('=================================================')
            print('')
    print('Outputs written to file:' + filename)
