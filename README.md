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
usage: main.py [-h] [--verbose] [--trottle TROTTLE] [--show_exception_tb]
               [--disable_crawling]
               website_url

Web crawler application

positional arguments:
  website_url          Url of the website to crawl

optional arguments:
  -h, --help           show this help message and exit
  --verbose            Show debug messages
  --trottle TROTTLE    Sleep time in secs between each 10 pages (to void rate
                       limiters)
  --show_exception_tb  Show exception trace back
  --disable_crawling   Disable crawling (go depth of 1)
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

### Show exceptions trace back 
By default the exception trace back are not shown for a cleaner output. However, to enable the 
printing trace back, use `--show_exception_tb` flag 

```sh
python main.py https://webscraper.io --show_exception_tb
```

### Disable crawling
To disable crawling (go only to depth of 1), use the `--disable_crawling` flag.

```sh
python main.py https://webscraper.io --disable_crawling
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
A connection error can be that the connection was reset/refused by peer or timeout. To know the exact error, use the `--show_exception_tb` flag.

### Exit code:
0: Success (but some pages might not been crawled (bad links, rate limiters)</br>
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
