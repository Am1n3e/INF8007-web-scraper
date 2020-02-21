# INF8007-web-scarper

Web scraper python application for the INF8007 winter 2020.


## Authors
- Amine El hattami
- Khizer Uddin

## Installation

This code have been tested with `python 3.7`, but should work with any python verion 3.3+

1- Create a virtual environment
```sh
python3.7 -m venv env
source env/bin/activate
```

2- Install required libraies

```sh
pip install -r requirements.txt  # or requirement-dev.txt to install dev libraries
```


## Usage

```
usage: main.py [-h] [--verbose] [--trottle TROTTLE] website_url

Web crawler application

positional arguments:
  website_url        Url of the website to crawl

optional arguments:
  -h, --help         show this help message and exit
  --verbose          Show debug messages
  --trottle TROTTLE  Sleep time in secs between each 10 pages (to void rate
                     limiters)
```


```sh
python main.py https://webscraper.io
```

### Verbose mode
To start the app in verbose mode, the `--verbose` flag.

```sh
python main.py https://webscraper.io --verbose
```

### Trottling
Some websites use rate limiter which blocks the scrapper, to avoid this use the trottle args to sleep after each 10
pages

```sh
python main.py https://webscraper.io --verbose --trottle 10
```


### Exit code:
0: Success (but some pages might not been crawled (bad links, rate limiters)
1: Fatal error (exceptions, ...)


## Contribution

### Formating

We use [black](https://github.com/psf/black) to format the source code and make sure it follows PEP8 standards.

Usage:

```bash
# Current directory is assumed to be root folder of the project

black .
```

### Linting

We use [pylint](https://www.pylint.org) to link the source code.

Usage:

```bash
# Current directory is assumed to be root folder of the project

pylint .
```
