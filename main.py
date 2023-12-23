from mpi4py import MPI

comm = MPI.COMM_SELF.Spawn(command="python3",
                           args=['machine.py'],
                           maxprocs=5)
