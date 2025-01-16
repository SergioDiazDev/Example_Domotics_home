all: venv

#Create venv
venv:
	python3 -m venv venv
	. venv/bin/activate
	@echo "Virtual environment created"
	@echo "To activate the virtual environment, run: source venv/bin/activate"
	@echo "To install the dependencies, run: make install"
#Install dependencies
install:
	pip install -r requirements.txt
	@echo "Dependencies installed"

exec:
	python3 sensors.py

.phony: all venv install