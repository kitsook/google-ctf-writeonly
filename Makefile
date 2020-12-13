doit:
	python doit.py
build:
	docker build -t sandbox-writeonly .
start:
	docker run --rm --name sandbox-writeonly -p 127.0.0.1:1337:1337 sandbox-writeonly
stop:
	docker stop sandbox-writeonly
disass:
	objdump --disassemble=check_flag src/chal
