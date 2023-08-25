# aliases
default: install

# commands
install:
    echo "Installing dependencies..."
    poetry install --with dev,test,docs

build:
    echo "Building..."
    poetry build

test:
    echo "Running tests..."
    poetry run pytest

watch:
    echo "Running tests..."
    poetry run ptw

coverage:
    echo "Running tests with coverage..."
    poetry run pytest --cov crias --cov-report term-missing

publish:
    echo "Publishing..."
    poetry publish --build

