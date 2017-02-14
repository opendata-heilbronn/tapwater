---
title: Test documentation
author: Gregor Schäfer
geometry: margin=2cm
version: 1.0
---

Status: Final

## Running Unit-Tests
1. ```docker-compose run web python manage.py test```

## Testing code

### PEP 257 -- Docstring Conventions
#### Requirements
1. pydocstyle

#### Installation
```
pip install pydocstyle
```

#### Running test
Change to main directory.

```
pydocstyle -v -e wasser tests tests_selenium
```

### Pylint
#### Requirements
1. pylint
1. pylint_django

#### Installation
```
pip install pylint
pip install pylint_django
```

#### Running test
Change to main directory.

```
pylint --load-plugins pylint_django wasser
```

### Flake8
#### Requirements 
1. flake8

#### Installation
```
pip install flake8
```

#### Running test
Change to main directory

```
flake8 wasser tests tests_selenium
```

### Dodgy
#### Requirements 
1. dodgy

#### Installation
```
pip install dodgy
```

#### Running test
Change to main directory

```
dodgy
```

## Benchmark tests

### Apache Benchmark
1. ```ab -n 100000 -c 10 -t 30 http://127.0.0.1:8000/de/```
 1. -n = Users -c = concurrent connections n * c = max requests
 1. -t = time
