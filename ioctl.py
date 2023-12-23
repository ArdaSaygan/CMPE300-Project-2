from mpi4py import MPI
from pathlib import Path
from sys import argv


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




input_file = open(Path(argv[1]), "r")   
output_file = open(Path(argv[2]), "w")

num_machines = int(input_file.readline())
prod_cycles = int(input_file.readline())

wf = [int(i) for i in input_file.readline().split()]
wear_factors = {"enhance": wf[0], "reverse": wf[1], "chop": wf[2], "trim": wf[3], "split": wf[4]}

maintenance_threshold = int(input_file.readline())


# each id has a list containing: a list of children, initial source (null for non leaf machines)
# and the initial operation
machines = dict((i, [[]]) for i in range(1, 44))

# parse input data
for line in input_file:
    linev = line.split()
    if len(linev) == 3:
            record_machine(machines, linev)
    elif len(linev) == 1:
            add_source(machines, linev[0])
    else:
        print("Unexpected error at line parsing")
        exit(1)

for machine in machines:
    data = machines.get(machine)
    while (len(data) < 3):
        data.append(None)

print(machines)

input_file.close()
output_file.close()