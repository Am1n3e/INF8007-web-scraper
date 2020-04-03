# INF8007-web-scraper

Web scraper python application for the INF8007 winter 2020.

## Authors
- Amine El hattami
- Khizer Uddin

## Installation

This code has been tested with `python 3.7`, but should work with any python version 3.3+

1- Create a virtual environment
```sh
python3.7 -m venv env
source env/bin/activate
```

2- Install required libraries

```sh
pip install -r requirements.txt  # or requirement-dev.txt to install dev libraries
```


## Usage

```
usage: main.py [-h] [--show_exception_tb] [--verbose] [--disable_crawling]
               [--throttle_duration_sec THROTTLE_DURATION_SEC]
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
  --throttle_duration_sec THROTTLE_DURATION_SEC
                        Sleep time in secs between each 10 pages (to void rate
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

**Example**
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

**Example**
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

**Example**
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

**Example**
```sh
python main.py  file_list < resources/file_list_1

# or using a pipe from a file 
cat resources/file_list_2 | python main.py  file_list

# or using a pip from stdout
(echo resources/webscraper.io.html && echo resources/invalid.html) | python main.py  file_list 
```

### Crawling url list from stdin
```
usage: main.py url_list [-h] [url_list]

positional arguments:
  url_list

optional arguments:
  -h, --help  show this help message and exit
```

**Example**
```sh
python main.py  url_list < resources/url_list_1

# or using a pipe from a file 
cat resources/url_list_2 | python main.py  url_list

# or using a pip from stdout
(echo https://webscraper.io && echo invalid_url) | python main.py  url_list 
```
### Optional arguments
#### Throttling
Some websites use rate limiter which blocks the scrapper, to avoid this use the `--throtlle_duration_sec` argument to sleep after each 10
pages
Note that this argument is only applicable for url and url list

**Example**
```sh
python main.py --throttle_duration_sec 5 url https://webscraper.io 
```

#### Disable crawling
To disable crawling (go only to depth of 1), use the `--disable_crawling` flag.</br>
Note that this argument is only applicable for url and url list

**Example**
```sh
python main.py --disable_crawling url https://webscraper.io 
```

#### Verbose mode
To start the application in verbose mode, use the `--verbose` flag. 

**Example**
```sh
python main.py --verbose url https://webscraper.io 
python main.py --verbose file resources/webscraper.io.html
```

#### Show exceptions trace back 
By default the exception trace back are not shown for a cleaner output. However, to enable the 
printing trace back, use `--show_exception_tb` flag 

**Example**
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
A connection error can refer to a reset/refused by peer or timeout connection. To know the exact error, use the `--show_exception_tb` flag.

### Exit code:
**0**: Success (but some pages might not been crawled (bad links, rate limiters)</br>
**1**: Fatal error (exceptions, ...)

## Running the crawler against a node server

This repository also provides a bash script that will run the crawler against a node web server

### Requirements

The bash script requires the following binaries:</br>
- git (we used version 2.24.1)</br>
- npm (we used version 6.13.4)</br>
- lsof (we used version 4.91)</br>
- curl (we used 7.64.1)</br>

### Usage
```
Usage: run.sh node_webserver_git_repo node_webserver_port [git_clone_dest]

positional arguments
        node_webserver_git_repo: The node webserver git repository
        node_webserver_port: The port to start the node webserver
        git_clone_dest: Set the destination for git clone. Optional default to pwd
```

**The script will perform the following:**</br>
- Clones the web server source code using the provided git repository in the provided destination</br>
- Install the npm packages</br>
- Run the server on the provided port</br>
- Run the crawler</br>
- Terminate the server

**Notes**</br>
- Since the script does not control the cloned web server, we assumed that it a working webserver. Any error will be just dumped to the user.</br>
- If the git destination folder exists, a prompt will ask if repository needs to be re-cloned</br>
```
scratch directory exits already. Do you want to delete and re-clone [y/N] ?
```

### Sample output

```sh
/scripts/run.sh https://github.com/bhanushalimahesh3/node-website.git 4000 scratch
```

```
#************************************************************
# Command line arguments
#************************************************************
node_webserver_git_repo = https://github.com/bhanushalimahesh3/node-website.git
node_webserver_port     = 4000
git_clone_dest          = scratch
#------------------------------------------------------------


#************************************************************
# Check requirements
#************************************************************
git ... Found
npm ... Found
lsof ... Found
curl ... Found
Python env ... enabled!
Checking requirements ... OK!
#------------------------------------------------------------


#************************************************************
# Setup webserver
#************************************************************
>>> Cloning https://github.com/bhanushalimahesh3/node-website.git
scratch directory exits already. Do you want to delete and re-clone [y/N] ?
y
Cloning into 'scratch'...
remote: Enumerating objects: 1146, done.
remote: Counting objects: 100% (1146/1146), done.
remote: Compressing objects: 100% (842/842), done.
remote: Total 1146 (delta 242), reused 1143 (delta 242), pack-reused 0
Receiving objects: 100% (1146/1146), 1.53 MiB | 2.92 MiB/s, done.
Resolving deltas: 100% (242/242), done.
>>> Installing npm package
npm WARN saveError ENOENT: no such file or directory, open '/Users/amineelhattami/work/INF8007-web-scraper/package.json'
npm WARN enoent ENOENT: no such file or directory, open '/Users/amineelhattami/work/INF8007-web-scraper/package.json'
npm WARN INF8007-web-scraper No description
npm WARN INF8007-web-scraper No repository field.
npm WARN INF8007-web-scraper No README data
npm WARN INF8007-web-scraper No license field.

up to date in 0.552s
found 0 vulnerabilities

>>> Running the web server
/Users/amineelhattami/work/INF8007-web-scraper
>>> Waiting for server to start ...
.

> website@0.0.0 start /Users/amineelhattami/work/INF8007-web-scraper/scratch
> node ./bin/www

#------------------------------------------------------------


#************************************************************
# Running the crawler
#************************************************************
2020-04-02 19:49:12,958 - src.crawler - DEBUG - Crawling: http://localhost:4000. Found 2 link(s)
2020-04-02 19:49:12,964 - src.crawler - DEBUG - Checking: http://localhost:4000/about OK!
2020-04-02 19:49:12,970 - src.crawler - DEBUG - Crawling: http://localhost:4000/about. Found 2 link(s)
2020-04-02 19:49:12,976 - src.crawler - DEBUG - Checking: http://localhost:4000/contact OK!
2020-04-02 19:49:12,983 - src.crawler - DEBUG - Crawling: http://localhost:4000/contact. Found 2 link(s)
2020-04-02 19:49:12,983 - src.crawler - INFO - Visited 2 page(s)
2020-04-02 19:49:12,983 - __main__ - INFO - No dead links found
#------------------------------------------------------------


#************************************************************
# Clean up
#************************************************************
>>> Terminating the server
#------------------------------------------------------------
```

## Contribution

### Formating

We use [black](https://github.com/psf/black) to format the source code and make sure it follows PEP8 standards.

Usage:

```sh
# Current directory is assumed to be root folder of the project

black .
```

### Linting

We use [pylint](https://www.pylint.org) to link the source code.

Usage:

```sh
# Current directory is assumed to be root folder of the project

pylint .
```

### Bash script

For bash scripts we follow [The google style guide](https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=1&cad=rja&uact=8&ved=2ahUKEwjT5q_W9sroAhXDU80KHYrnDxwQFjAAegQIBhAB&url=https%3A%2F%2Fgoogle.github.io%2Fstyleguide%2Fshell.xml&usg=AOvVaw3vE76VbFUMz5kmsV8pKzYX)
