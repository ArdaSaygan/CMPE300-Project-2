"""
machine.py - slave logic module
--------------------
Arda Saygan, 2021400063
Yigit Kagan Poyrazoglu, 2020400222
Group 14
"""

from mpi4py import MPI
import numpy as np
from time import sleep
from operations import produce
import pickle

comm = MPI.Comm.Get_parent()
comm_world = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()


# get main processes id
main_rank = np.array(0, dtype='i')
comm.Bcast([main_rank, MPI.INT], root=0)
# get system configuration
sys_config_pickled = bytearray(1024)
comm.Bcast(sys_config_pickled, root=0)
sys_config = pickle.loads(sys_config_pickled)
prod_cycles, wear_factors, maintenance_threshold, output_file_path = sys_config

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

# create list for keeping maintenance logs
# a list of 3 tuple
maintenance_logs = []
accumulated_wear = 0

# work loop
while (True):
    # wait for the cycle signal
    cycle = np.array(0, dtype='i')
    comm.Bcast([cycle, MPI.INT], root=0)

    # wait for children machines to complete their work
    # print(f"{rank} -- {pid} -- {children_list} - p - {parent_pid - 1} - source {source}")

    while True: 
        all_children_done = True
        for child in children_list:
            child_rank = child-1
            if not comm_world.Iprobe(source=child_rank, tag=3):
                # print(rank, " gonna probn't ", child)
                all_children_done = False
        if all_children_done:
            break

    # this will be a list of tuples, 
    # where first element is the pid of the child
    # and second element is the product recieved 
    # add the sources already if machine is a leaf node indeed
    received_products = [(-1, source)] if source != None else list()

    for child in children_list:
        child_rank = child-1
        prod = bytearray(1024)
        req = comm_world.irecv(buf= prod, source=child_rank, tag=3)
        prod = prod.decode("utf-8").strip('\x00')
        # may be problematic, check this design later /^|^\
        received_products.append((child, prod))

    # print(f" rank {rank} cycle {cycle}")

    # produce product
    if pid != 1:
        operation = operation_list[op_index] 
        product = produce(received_products, operation)
        op_index = (op_index+1)%op_len 
        accumulated_wear += wear_factors[operation] 
    else:
        operation = ""
        product = produce(received_products, operation)
    

    # print(f" {rank} produced {product}")
    # calculate maintenance cost
    if pid != 1:
        if (accumulated_wear>=maintenance_threshold):
            C = (accumulated_wear - maintenance_threshold + 1)*wear_factors[operation]
            maintenance_logs.append( f"{pid}-{C}-{cycle+1}" )
            accumulated_wear = 0

    # send product to parent machine
    req = comm_world.Isend([product.encode('utf-8'), MPI.CHAR], dest=parent_pid-1, tag=3)
    req.Wait()
    # signal main that the work is done
    comm.send(product, dest=main_rank, tag=2)

    # end of the simulation, write the maintenance costs
    if cycle == prod_cycles - 1:
        output_file = open(output_file_path,"+a")
        for log in maintenance_logs:
            output_file.write(log+"\n")
        break


sleep(0.3)


