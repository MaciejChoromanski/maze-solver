install:
	pip install -r requirements.txt

run:
	python maze_solver

run_with_file:
	python maze_solver -f $(FILE)

help:
	python maze_solver -h

test:
	python -m unittest discover

lint:
	flake8