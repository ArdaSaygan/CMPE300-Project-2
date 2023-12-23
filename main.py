from mpi4py import MPI
from time import sleep

comm = MPI.COMM_SELF.Spawn(command="python3",
                           args=['machine.py', "id", 'parent_id', "opeartion", "initial_source"],
                           maxprocs=5)
sleep(1)
