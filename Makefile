
botname = donotbot
ROOT_DIR:=$(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))

.PHONY: buid config run stop start restart clean

build: Dockerfile
	docker build -t sopel-crypto .

config: build
	docker run --rm -it -v $(ROOT_DIR)/$(botname):/home/sopel/.sopel sopel-crypto sopel -w

run:
	docker run -d --name $(botname) -v $(ROOT_DIR)/$(botname):/home/sopel/.sopel sopel-crypto sopel

stop:
	docker run --rm -it -v $(ROOT_DIR)/$(botname):/home/sopel/.sopel sopel-crypto sopel -q
	docker stop $(botname)

start:
	docker start $(botname)

restart: stop start

install: build config
	docker run -d --restart=always --name $(botname) -v $(ROOT_DIR)/$(botname):/home/sopel/.sopel sopel-crypto sopel

clean:
	docker container rm $(botname)
	docker image rm sopel-crypto
