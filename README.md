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
usage: main.py [-h] [--show_exception_tb] [--verbose] {url,file} ...

Web crawler application

positional arguments:
  {url,file}           Resource type
    url                Crawl URL. url -h for more details
    file               Crawl a file. file -h for more details

optional arguments:
  -h, --help           show this help message and exit
  --show_exception_tb  Show exception trace back
  --verbose            Show debug messages
```

### Crawling a URL
```
usage: main.py url [-h] [--trottle TROTTLE] [--disable_crawling] resource

positional arguments:
  resource            Url for the web page to crawl

optional arguments:
  -h, --help          show this help message and exit
  --trottle TROTTLE   Sleep time in secs between each 10 pages (to void rate
                      limiters)
  --disable_crawling  Disable crawling (go depth of 1)
```

```sh
python main.py url https://webscraper.io
```

#### Trottling
Some websites use rate limiter which blocks the scrapper, to avoid this use the trottle args to sleep after each 10
pages

```sh
python main.py url https://webscraper.io --trottle 5
```

#### Disable crawling
To disable crawling (go only to depth of 1), use the `--disable_crawling` flag.

```sh
python main.py url https://webscraper.io --disable_crawling
```

### Crawling a file 
```
usage: main.py file [-h] resource

positional arguments:
  resource    file path of the html page to crawl

optional arguments:
  -h, --help  show this help message and exit
```

```sh
python main.py file resources/webscraper.io.html
```

### Verbose mode
To start the app in verbose mode, use the `--verbose` flag. 

```sh
python main.py --verbose url https://webscraper.io 
python main.py --verbose file resources/webscraper.io.html
```

### Show exceptions trace back 
By default the exception trace back are not shown for a cleaner output. However, to enable the 
printing trace back, use `--show_exception_tb` flag 

```sh
python main.py --show_exception_tb url https://webscraper.io 
python main.py --show_exception_tb file resources/webscraper.io.html
```


### Sample output
```
INFO:src.crawler:Visited 502 page(s)
INFO:__main__:dead links:
Link                                                           Reason
-------------------------------------------------------------  -----------------------------------------
https://www.youtube.com/yt/about/en                            Bad status code: 404 'Not Found'
https://www.wbs-law.de/eng/practice-areas/internet-law/it-law  Bad status code: 410 'Gone'
https://website.com                                            Connection error
https://api.webscraper.io/api/v1/sitemap?api_token=&lt         Bad status code: 405 'Method Not Allowed'
http://webscraper.io/&quot                                     Bad status code: 404 'Not Found'
https://api.webscraper.io/api/v1/sitemap/&lt                   Bad status code: 401 'Unauthorized'
https://api.webscraper.io/api/v1/sitemaps?api_token=&lt        Bad status code: 401 'Unauthorized'
https://api.webscraper.io/api/v1/scraping-job?api_token=&lt    Bad status code: 405 'Method Not Allowed'
https://api.webscraper.io/api/v1/scraping-job/&lt              Bad status code: 401 'Unauthorized'
https://api.webscraper.io/api/v1/scraping-jobs?api_token=&lt   Bad status code: 401 'Unauthorized'
https://api.webscraper.io/api/v1/account?api_token=&lt         Bad status code: 401 'Unauthorized'
https://example.com/robots.txt                                 Connection error
https://example.com/sitemap.xml                                Connection error
http://example.com/page                                        Connection error
http://example.com/page/1                                      Connection error
http://example.com/page/2                                      Connection error
http://example.com/page/3                                      Connection error
http://example.com/page/001                                    Connection error
http://example.com/page/002                                    Connection error
http://example.com/page/003                                    Connection error
http://example.com/page/0                                      Connection error
http://example.com/page/10                                     Connection error
http://example.com/page/20                                     Connection error
```

About **Connection error**</br>
A connection error can refere to a reset/refused by peer or timeout connection. To know the exact error, use the `--show_exception_tb` flag.

### Exit code:
**0**: Success (but some pages might not been crawled (bad links, rate limiters)</br>
**1**: Fatal error (exceptions, ...)


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
