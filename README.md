# maze-solver
Python script which can solve a maze based on an image

## Table of contents
1. [Images restrictions](#images-restrictions)
2. [Current stack](#current-stack)
3. [Installation](#installation)
4. [Tests](#tests)
5. [Lint](#lint)
6. [Author](#author)
7. [License](#license)

## Images restrictions

This script solves mazes from images. The method used to determine where the exit is relies on always sticking with the right wall of the maze. The width and the height of the image doesn't matter. However, the image must contain only 3 colors:

1. Grey - this one represents entrance and exit of the maze,
2. Black - this one represents the walls of the maze,
3. White - this one represents the walking space of the maze.

Additional info:
1. The entrance of the maze must be located at (0, 0) pixel.
2. The exit of the maze must be located at (<max_width>, <max_height>) pixel.

## Current stack
* [Python 3.8](https://www.python.org/)
* [Flake8](https://flake8.pycqa.org/en/latest/)
* [Pre-commit](https://pre-commit.com/)
* [Travis CI](https://travis-ci.com/)

## Installation
These steps will help you set up the project on your machine. They were written with UNIX/UNIX-like based systems in mind.

### Prerequisites
You'll need [virtualenv](https://pypi.org/project/virtualenv/) to set up this project properly.

### Installing

Create and activate virtual environment in the root directory of the project:
```
virtualenv <virtual_env_name> && source venv/bin/activate
```

Running the app in 'file' mode:
```
make run_with_file FILE=<file_name>
```

Running the app in 'test' mode:
```
make run
```

Displaying help text
```
make help
```

## Tests
Run the tests:
```
make test
```

## Lint
Run the lint:
```
make lint
```

## Author
* **Maciej Choromański** - [MaciejChoromanski](https://github.com/MaciejChoromanski)

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
