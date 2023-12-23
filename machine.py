
from mpi4py import MPI
import numpy
from time import sleep

comm = MPI.Comm.Get_parent()
size = comm.Get_size()
rank = comm.Get_rank()

parent_rank = numpy.array(0, dtype='i')
comm.Bcast([parent_rank, MPI.INT], root=0)

print("my rank : ", rank, "parent rank", parent_rank)

data = comm.recv(source=parent_rank, tag=12)
print("rank ", rank, " received data ", data)

sleep(2)


