"""
ioctl.py - I/O and program logic module
-------------------- 
Arda Saygan, 2021400063
Yigit Kagan Poyrazoglu, 2020400222
Group 14
"""

from mpi4py import MPI
from pathlib import Path
from sys import argv, executable
from time import sleep
import numpy as np
import pickle


def record_machine(machines, lineArray):
    parent = int(lineArray[1])
    child = int(lineArray[0])
    # record child machine as a child of parent
    parentData = machines.get(parent)
    parentData[0].append(child)
    # add initial operation to the data of child 
    childData = machines.get(child)
    childData.append(lineArray[2])

def add_source(machines, product):
    for machine in machines:
        machineData = machines.get(machine)
        children = machineData[0]
        if len(children) == 0 and len(machineData) == 2:
                machineData.append(product)
                break
        
def find_parent(machines, machine):
    for m in machines:
        children = machines.get(m)[0]
        if machine in children:
            return m
    
    return -1


input_file = open(Path(argv[1]), "r")   
output_file = open(Path(argv[2]), "w")
output_file.close()

num_machines = int(input_file.readline())
prod_cycles = int(input_file.readline())

wf = [int(i) for i in input_file.readline().split()]
wear_factors = {"enhance": wf[0], "reverse": wf[1], "chop": wf[2], "trim": wf[3], "split": wf[4]}

maintenance_threshold = int(input_file.readline())



"""
Initial information for each machine is stored in a dictionary while reading the input, 
until the threads are spawned. The dictionary is organized as:
MachineId:[[children], initial product, initial operation]
"""
machines = dict((i, [[]]) for i in range(1, num_machines+1))

# parse input data
for line in input_file:
    linev = line.split()
    # for lines with 3 tokens, record/update the machine data in the dictionary
    if len(linev) == 3:
            record_machine(machines, linev)
    # for lines with 1 token, update initial product for the machine in the dict
    elif len(linev) == 1:
            add_source(machines, linev[0])
    else:
        print("Unexpected error at line parsing")
        exit(1)

for machine in machines:
    data = machines.get(machine)
    while (len(data) < 3):
        data.append(None)

input_file.close()


# get the main rank
comm_world = MPI.COMM_WORLD
rank = comm_world.Get_rank()

comm = MPI.COMM_SELF.Spawn(executable,
                           args=['machine.py'],
                           maxprocs=num_machines)
# broadcast main rank to all children
parent_rank = np.array(rank, 'i')
comm.Bcast([parent_rank, MPI.INT], root=MPI.ROOT)
# broadcast other important info about the system configuration
system_info = np.array([prod_cycles, wear_factors, maintenance_threshold, Path(argv[2])], dtype=object)
system_info_pickled = pickle.dumps(system_info)
comm.Bcast(system_info_pickled, root=MPI.ROOT)

#print(machines)
# send initialization info to children
for machine in machines:
    machineInfo = machines.get(machine)
    # dataList = [machine id, parent id, list of children, first operation, source]
    dataList = [machine, find_parent(machines, machine), machineInfo[0], machineInfo[1], machineInfo[2]]
    comm.send(dataList, dest=machine-1, tag=1)


# initialization is done
    
# start the production cycles
for cycle in range(prod_cycles):
    # Broadcast the current production cycle
    cycle_arr = np.array(cycle, 'i')
    comm.Bcast([cycle_arr, MPI.INT], root=MPI.ROOT)

    # Wait for all machines to complete their work
    product = comm.recv(source=0, tag=2)
    for child in range(1, num_machines):
        comm.recv(source=child, tag=2)

    # perform the necessary operations on the product
    
    # print(f">>>{cycle}>>", product)
    output_file = open(Path(argv[2]), "a")
    output_file.write(product+"\n")
    output_file.close()


sleep(0.3)




