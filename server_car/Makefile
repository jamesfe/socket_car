
# Set up an environment for the server
.PHONY: setuppython
setuppython:
	 mkdir -p ../localenv/
	 python3 -m venv ../localenv/
	 source ../localenv/bin/activate
	 pip install -r requirements.txt

.ONESHELL .PHONY : test
test:
	../localenv/bin/python3 -m unittest discover -v

.PHONY: run
run:
	pigpiod
	python3 -m car_serve.car_serve ./config/config.json


.PHONY: testrun
testrun:
	python3 -m car_serve.car_serve ./config/no_rpi_config.json


.PHONY: coverage
coverage:
	coverage run --source car_serve -m unittest discover -v
	coverage report -m
