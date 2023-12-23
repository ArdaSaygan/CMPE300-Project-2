
from mpi4py import MPI
import numpy
from time import sleep

comm = MPI.Comm.Get_parent()
size = comm.Get_size()
rank = comm.Get_rank()



if rank == 0: # kill this child, for convenience 
    pass
    #exit()
print("rank 2 ", rank)
# get main processes id
main_rank = numpy.array(0, dtype='i')
comm.Bcast([main_rank, MPI.INT], root=0)

print("rank 3", rank)
# get machine parameters
machine_init = comm.recv(source=main_rank, tag=1)
print("rank 4", rank, machine_init)
pid, parent_pid, first_operation, feed = machine_init


# initialize operation list, operation index
# pid 1 is a special case
operation_list = []
op_len = 0
if (pid == 1):
    pass
elif (pid % 2 == 1):
    operation_list = ["reverse", "trim"]
    op_len = 2
else:
    operation_list = ["enhance", "split", "chop"]
    op_len = 3
op_index = 0
while (pid != 1) and (operation_list[op_index] != first_operation):
    op_index = (op_index + 1)%op_len



sleep(2)


