To run the program do the following.
Python version must be 3.12. 

virtualenv venv --python=<path_to_python3.12>
source venv/bin/activate
pip install -r requirements.txt

mpiexec -n 1 --oversubscribe python3 ioctl.py <path_to_input.txt> <path_to_output.txt>