#!/usr/bin/env python

import argparse
import subprocess
import string
import time,sys
import random

def main():
    
    parser = argparse.ArgumentParser()

    #Read the arguments
    parser.add_argument('-d','--destination', required=True, help="IP address of the destination physical machine")
    
    VMS_to_migrate = parser.add_mutually_exclusive_group(required=True)
    VMS_to_migrate.add_argument("-id", help="Migrate only one vm with the <id>")
    VMS_to_migrate.add_argument("-all", action='store_true', help="Migrate all VMs")
    
    #the policy used - random vs smart
    parser.add_argument("-p","--policy",choices=['random','smart'],default='random',help="Policy of VM Migration")

    args = parser.parse_args()
    
    if(args.all):
        #read the list of VMs
        VM_list = read_VM_list()
    
        #migrate all the VMs
        migrate_all(VM_list,args.destination,args.policy)
    else:
        migrate_one(args.id,args.destination)
        
    #start the timer
    start_time = time.time()
        
    #elapsed time
    elapsed_time = time.time() - start_time
    print ("The elapsed time is " + str(elapsed_time))    
    

#Method VM list    
def read_VM_list():
    
    #outputs the list of VMs in the stdout
    command_output = subprocess.Popen(["ls","-al"],stdout=subprocess.PIPE)
    
    #initialize VM list
    VM_list = []
    
    #read line by line with the "xm list" command, and create a list of VMs
    while True:
        line = command_output.stdout.readline()
        if line != '':
            line = line.rstrip()
            tokens = line.split(" ")
            
            #filtering out
            if((tokens[0] != "Domain-0") & (tokens[0] != "Name")):
                VM_list.append(tokens[0])
        else:
            break
    
    return VM_list
    
    
#Function to migrate all the VMs
def migrate_all(VM_list,destination,policy):
    
    #print the policy
    if(policy == 'random'):
        migrate_random(VM_list,destination)
    else:
        migrate_smart(VM_list,destination)

#Random Migration
def migrate_random(VM_list,destination):

    print("Migrating all VMs - The policy is Random")
    
    #randomizing
    random.shuffle(VM_list)
    
    for VM in VM_list:
        subprocess.call(["echo","xm","migrate",VM,destination,"-l"])
    return

#Smart Algorithm Migration    
def migrate_smart(VM_list, destination):
    
    print("SMART ALGORITHM - NOT YET DONE")
    return
    
def migrate_one(VM,destination):
    subprocess.call(["echo","xm","migrate",VM,destination,"-l"])
    return

if __name__ == "__main__":
        main()
        
        
#TTL - optional parameter - 
