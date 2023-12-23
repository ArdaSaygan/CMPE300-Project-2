
from mpi4py import MPI
import numpy
from time import sleep

comm = MPI.Comm.Get_parent()
comm_world = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()



if rank == 0: # kill this child, for convenience 
    pass
    #exit()

# get main processes id
main_rank = numpy.array(0, dtype='i')
comm.Bcast([main_rank, MPI.INT], root=0)

# get machine parameters
machine_init = comm.recv(source=main_rank, tag=1)
pid, parent_pid, children_list, first_operation, source = machine_init

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


# work loop
while (True):
    # wait for the cycle signal
    cycle = numpy.array(0, dtype='i')
    comm.Bcast([cycle, MPI.INT], root=0)

    # wait for children machines to complete their work
    print(f"{rank} -- {children_list}")
    for child in children_list:
        comm_world.recv(source=child, tag=3)

    print(f" rank {rank} cycle {cycle}")

    # process and create product 
    product = "bahario"
    # send product to parent machine
    req = comm_world.Isend(product, dest=parent_pid, tag=3)
    # req.Wait()
    # signal main that the work is done
    comm.send(product, dest=main_rank, tag=2)



sleep(2)


