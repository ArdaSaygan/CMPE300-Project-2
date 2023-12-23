from mpi4py import MPI
from pathlib import Path
from sys import argv


input_file = open(Path(argv[1]), "r")   
output_file = open(Path(argv[2]), "w")

num_machines = int(input_file.readline())
prod_cycles = int(input_file.readline())

wf = [int(i) for i in input_file.readline.split()]

input_file.close()
output_file.close()