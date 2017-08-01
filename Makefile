.ONESHELL .PHONY : test
test:
	source /usr/local/bin/virtualenvwrapper.sh
	cd server_car
	workon socket_car
	python -m unittest discover -v
