
# Set up an environment for the server
.PHONY: setuppython
setuppython:
	 mkdir ../localenv/
	 python3 -m venv ../localenv/
	 source ../localenv/bin/activate
	 pip install -r requirements.txt

.ONESHELL .PHONY : test
test:
	../localenv/bin/python3 -m unittest discover -v

.PHONY: run
run:
	python3 -m car_serve.car_serve
