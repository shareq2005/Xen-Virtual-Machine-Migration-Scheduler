#!/usr/bin/env python

import argparse
import subprocess
import string
import time,sys


def main():
    
    parser = argparse.ArgumentParser()

    #Read the arguments
    parser.add_argument("-d", help="IP address of the destination physical machine")
    parser.add_argument("-id", help="ID of the VM you want to migrate")

    args = parser.parse_args()

    print args.d
    print args.id

    #read the list of VMs
    VM_list = read_VM_list()
    
    #migrate all the VMs
    migrate_all(VM_list,args.d)
    
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
def migrate_all(VM_list,destination):
    
    for VM in VM_list:
        subprocess.call(["echo","xm","migrate",VM,destination,"-l"])
        
    return

if __name__ == "__main__":
        main()
        
        
#TTL - optional parameter - 
