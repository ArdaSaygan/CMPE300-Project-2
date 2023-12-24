
from mpi4py import MPI
import numpy as np
from time import sleep
from operations import produce
comm = MPI.Comm.Get_parent()
comm_world = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()



if rank == 0: # kill this child, for convenience 
    pass
    #exit()

# get main processes id
main_rank = np.array(0, dtype='i')
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
    cycle = np.array(0, dtype='i')
    comm.Bcast([cycle, MPI.INT], root=0)

    # wait for children machines to complete their work
    print(f"{rank} -- {pid} -- {children_list} - p - {parent_pid - 1} - source {source == None}")

    while True: 
        all_children_done = True
        for child in children_list:
            child_rank = child-1
            if not comm_world.Iprobe(source=child_rank, tag=3):
                # print(rank, " gonna probn't ", child)
                all_children_done = False
        if all_children_done:
            break

    received_products = list() # this will be a list of tuples, 
                               # where first element is the pid of the child
                               # and second element is the product recieved 

    for child in children_list:
        child_rank = child-1
        prod = bytearray(1024)
        req = comm_world.irecv(buf= prod, source=child_rank, tag=3)
        prod = prod.decode("utf-8").strip('\x00')
        # may be problematic, check this design later /^|^\
        received_products.append((child, prod))

    print(f" rank {rank} cycle {cycle}")

    # produce product
    print(f" {rank} takes {received_products} to do {operation_list[op_index]}")
    product = produce(received_products, operation_list[op_index])
    op_index = (op_index+1)%op_len
    print(f" {rank} produced {product}")
    # calculate maintenance cost


    # send product to parent machine
    req = comm_world.Isend([product.encode('utf-8'), MPI.CHAR], dest=parent_pid-1, tag=3)
    req.Wait()
    # signal main that the work is done
    comm.send(product, dest=main_rank, tag=2)



sleep(2)


