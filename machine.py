from mpi4py import MPI
from pathlib import Path
from sys import argv


parent = MPI.Comm.Get_parent()
rank = parent.Get_rank()


print('hello from rank: ', rank)
