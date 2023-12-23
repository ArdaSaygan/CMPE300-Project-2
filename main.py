from mpi4py import MPI
import numpy
import sys
from time import sleep
N = 5
comm_world = MPI.COMM_WORLD
rank = comm_world.Get_rank()
comm = MPI.COMM_SELF.Spawn(sys.executable,
                           args=['machine.py'],
                           maxprocs=N)


parent_rank = numpy.array(rank, 'i')
comm.Bcast([parent_rank, MPI.INT], root=MPI.ROOT)

data = [12,23,24,25,26]

for p in range(0,N):
    comm.send(obj= data[p] , dest=p, tag=1)


sleep(2)