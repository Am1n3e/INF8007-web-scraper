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
age: main.py [-h] [--show_exception_tb] [--verbose] [--disable_crawling]
               [--trottle TROTTLE]
               {url,file,html,file_list,url_list} ...

Web crawler application

positional arguments:
  {url,file,html,file_list,url_list}
                        Resource type
    url                 Crawl URL. url -h for more details
    file                Crawl a file. file -h for more details
    html                Crawl html content from stdin. html -h for more
                        details
    file_list           Crawl file list from stdin. file_list -h for more
                        details
    url_list            Crawl url list from stdin. url_list -h for more
                        details

optional arguments:
  -h, --help            show this help message and exit
  --show_exception_tb   Show exception trace back
  --verbose             Show debug messages
  --disable_crawling    Disable crawling (go depth of 1). only for urls
  --trottle TROTTLE     Sleep time in secs between each 10 pages (to void rate
                        limiters). only for urls
```

### Crawling a URL
```
usage: main.py url [-h] [--trottle TROTTLE] [--disable_crawling] resource

positional arguments:
  resource            Url for the web page to crawl

optional arguments:
  -h, --help          show this help message and exit
```

```sh
python main.py url https://webscraper.io
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

### Crawling html content from stdin
```
usage: main.py html [-h] [html_content]

positional arguments:
  html_content

optional arguments:
  -h, --help    show this help message and exit
```

```sh
python main.py html < resources/webscraper.io.html

# or using a pipe
cat resources/webscraper.io.html | python main.py html
```

### Crawling file list from stdin
```
usage: main.py file_list [-h] [file_list]

positional arguments:
  file_list

optional arguments:
  -h, --help  show this help message and exit
```

```sh
python main.py  file_list < resources/file_list_1

# or using a pipe from a file 
cat resources/file_list_2 | python main.py  file_list

# or using a pip from stdout
echo resources/webscraper.io.html && echo resources/invalid.html| python main.py  file_list 
```

### Crawling url list from stdin
```
usage: main.py url_list [-h] [url_list]

positional arguments:
  url_list

optional arguments:
  -h, --help  show this help message and exit
```

```sh
python main.py  url_list < resources/url_list_1

# or using a pipe from a file 
cat resources/url_list_2 | python main.py  url_list

# or using a pip from stdout
echo https://webscraper.io && echo invalid_url | python main.py  file_list 
```

#### Trottling
Some websites use rate limiter which blocks the scrapper, to avoid this use the `--trotlle_duration_sec` arg to sleep after each 10
pages
Note that this argument is only applicable for url and url list

```sh
python main.py --trottle_duration_sec 5 url https://webscraper.io 
```

#### Disable crawling
To disable crawling (go only to depth of 1), use the `--disable_crawling` flag.</br>
Note that this argument is only applicable for url and url list

```sh
python main.py --disable_crawling url https://webscraper.io 
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
INFO:src.crawler:Visited 501 page(s)
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
