#!/usr/bin/env python

import argparse
import subprocess
import string
import time,sys
import random
#import ssh
#from ssh import Connection
from operator import attrgetter
from collections import namedtuple

def main():
    
    parser = argparse.ArgumentParser()

    #Read the arguments
    parser.add_argument('-d','--destination', required=True, help="IP address of the destination physical machine")
    
    VMS_to_migrate = parser.add_mutually_exclusive_group(required=True)
    VMS_to_migrate.add_argument("-id", help="Migrate only one vm with the <id>")
    VMS_to_migrate.add_argument("-all", action='store_true', help="Migrate all VMs")
    
    #the policy used - random vs smart
    parser.add_argument("-p","--policy",choices=['random','smart'],default='random',help="Policy of VM Migration")
    parser.add_argument("-ttl", help="The TTL input for migration", default=0.0, type=float)
    
    args = parser.parse_args()

    if(args.all):
        #read the list of VMs
        VM_list = read_VM_list()
        migrate_all(VM_list,args.destination,args.policy,args.ttl)
    else:
        migrate_one(args.id,args.destination)
        
    return    

#Method VM list    
def read_VM_list():
    
    #outputs the list of VMs in the stdout
    command_output = subprocess.Popen(["xm","list"],stdout=subprocess.PIPE)
    
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
    
    
def read_VM_tuple():
    #outputs the list of VMs in the stdout
    command_output = subprocess.Popen(["xl","list"],stdout=subprocess.PIPE)
     
    VM_Tuple = namedtuple("VM_Tuple","VM_name RAM")
    VM_Tuple_list = []
        
    #read line by line with the "xm list" command, and create a list of VMs
    while True:
        line = command_output.stdout.readline()
        if line != '':
            #line = line.rstrip()
            tokens = line.split()
#            print("TOKENS0 "+tokens[0])
#            print("TOKENS1 "+tokens[2])
#            print("TOKENS2 "+tokens[2])
            
            #filtering out
            if((tokens[0] != "Domain-0") & (tokens[0] != "Name") & (tokens[0] != "total")):
                VM = VM_Tuple(tokens[0],float(tokens[2]))
                #VM_Tuple_list.append([token[0],token[2])
                VM_Tuple_list.append(VM)
        else:
            break
    
    return VM_Tuple_list
    
    
#Function to migrate all the VMs
def migrate_all(VM_list,destination,policy,ttl):
    
    #print the policy
    if(policy == 'random'):
        migrate_random(VM_list,destination,ttl)
    else:
        migrate_smart(VM_list,destination,ttl)
        
    return
    
#Random Migration
def migrate_random(VM_list,destination,ttl):

    print("Migrating all VMs - The policy is Random")
    
    #randomizing
    random.shuffle(VM_list)
    
    if(ttl == 0.0):
        migrate_no_ttl(VM_list,destination)
    else:
        migrate_ttl(VM_list,destination,ttl)
        
    return

#Migrate without the TTL defined
def migrate_no_ttl(VM_list,destination):        
    #start the time
    start_time = time.time()
    
    for VM in VM_list:
        subprocess.call(["xm","migrate",VM,destination,"-l"])        
        
    elapsed_time = time.time() - start_time

    print("The Elapsed time is "+str(elapsed_time))
    return


#Migrate the VMs with the TTL defined
def migrate_ttl(VM_list,destination,ttl):    
    print("Starting migration within a TTL of "+str(ttl))
    elapsed_time = 0.0
    count_vm_migrated = 0
    
    for VM in VM_list:
        start_time = time.time()
        subprocess.call(["xm","migrate",VM,destination,"-l"])        
        elapsed_time_process = time.time() - start_time
            
        if(elapsed_time + elapsed_time_process <= ttl):
            elapsed_time += elapsed_time_process
            count_vm_migrated += 1
            print("Migrated "+VM+" within the TTL of "+str(ttl))                
        else:
            break
            
    
    print("VMs Migrated within TTL = "+str(count_vm_migrated))
    print("The Elapsed time to migrate within this TTL is "+str(elapsed_time))
    return
    
#Smart Algorithm Migration    
def migrate_smart(VM_list, destination,ttl):
    
    #VM Tuple list
    VM_Tuple_List = read_VM_tuple()
    
    #sort the tuple list
    VM_Tuple_List = sorted(VM_Tuple_List, key=attrgetter('RAM'))

    #VM tuple list
    VM_list = []
    
    for VM_Tuple in VM_Tuple_List:
        VM_list.append(VM_Tuple.VM_name)

    print VM_list
    
    if(ttl == 0.0):
        migrate_no_ttl(VM_list,destination)
    else:
        migrate_ttl(VM_list,destination,ttl)
        
            
    return 0
    
def migrate_one(VM,destination):
    subprocess.call(["xm","migrate",VM,destination,"-l"])
    return


if __name__ == "__main__":
        main()
        
        
        
#TTL - optional parameter - 
