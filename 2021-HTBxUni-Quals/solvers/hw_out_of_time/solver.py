import time
import string
import socket
import base64
import numpy as np
import matplotlib.pyplot as plt


HOST = '167.172.51.181' # This must be changed to the corresponding value of the live instance
PORT = 30937  # This must be changed to the corresponding value of the live instance

# This function is used to decode the base64 transmitted power trace (which is a NumPy array)
def b64_decode_trace(leakage):
	byte_data = base64.b64decode(leakage) # decode base64
	return np.frombuffer(byte_data) # convert binary data into a NumPy array


# This function is used to communicate with the remote interface via socket
# The socket connection is also accessible with the use of netcat (nc)
def connect_to_socket(option, data):
	data = data.encode()
	# Initialize a socket connection 
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		# Connect to the HOST machine on the provided PORT
		s.connect((HOST, PORT))
		
		# Receive initial message
		resp_1 = s.recv(1024)

		# Select one of the two available options of this interface
		s.sendall(option) 	

		# Receive response
		resp_2 = s.recv(1024)

		# Send the data 
		s.sendall(data) 

		# Receive response
		# receive base64 encoded binary data 
		# that represented the power traces as a Numpy array 
		# use loop to avoid missing packets due to high latency 
		resp_data = b''
		tmp = s.recv(8096)
		while tmp != b'':
			resp_data += tmp
			tmp = s.recv(8096)
		s.close()

		# The print commands can be used for debugging in order to observe the responses
		# The following print commands can be commented out.
		# print(resp_1.decode('ascii'))
		# print(option)
		# print(resp_2.decode('ascii'))
		# print(data)

		return resp_data


def get_power_trace(password):
    leakage = connect_to_socket(b'1', password)
    power_trace = b64_decode_trace(leakage)
    # print("Length of power trace: {}".format(power_trace.shape))
    # print(power_trace)
    return power_trace

# We know that the flag starts with H.
res = "H"
arr = []
# We can get the first power_trace to calculate the differences latter.
for _ in range(1):
    arr.append(get_power_trace(res))
base = np.mean(arr, axis=0)

ALPHABET = string.ascii_letters + string.digits + string.punctuation
while "}" not in res:
    letters = {}
    for l in ALPHABET:
        arr = []
        for _ in range(1):
            arr.append(get_power_trace(res + l))
            time.sleep(0.1)
        # Average of all the tries to get a more accurate trace. Note: In the
        # end we only did 1 because it worked.
        avg = np.mean(arr, axis=0)
        letters[l] = (avg, np.max(np.abs(avg - base)))
    # Letter with the highest power consumption.
    l = max(letters, key=lambda x: letters[x][1])
    res += l
    # Update the base power_trace.
    base = letters[l][0]
    print(res)
