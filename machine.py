from mpi4py import MPI


parent = MPI.Comm.Get_parent()
rank = parent.Get_rank()

print('hello from rank: ', rank)
