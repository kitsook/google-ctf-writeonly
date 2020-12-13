*This is from one of the Google's CTF 2020 challenges, namely the [writeonly](https://github.com/google/google-ctf/tree/master/2020/quals/sandbox-writeonly).*

Changes:
- modified the Dockerfile to connect the `chal` to port 1337. So we can run the container locally and test it
- an alternate `doit.py` exploit. inject the code directly within the child's loop and print the flag instead of starting a shell
- added a Makefile for commands used frequently during the hack

***

# Challenge Description

## Sandbox Writeonly

This sandbox executes any shellcode you send. But thanks to seccomp, you won't be able to read /home/user/flag.

# Details (warning: spoilers)

This challenge is intended as a beginners challenge and should be solvable
without too much time investment by experienced players.

The setup is as follows:
* the challenge reads shellcode from the user
* forks a new process
* child:
  * sleep indefinitely
* parent:
  * set up a seccomp filter that doesn't allow reading
  * executes the shellcode of the player

The intended solution is to inject code into the child.
I.e. opening /proc/childpid/mem, seeking to the right address and writing 2nd
stage shellcode that reads the flag.
