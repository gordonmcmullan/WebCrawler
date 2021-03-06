## Simple Webcrawler
This is a simple python web crawler, which will start at a given target page and crawl links from that page and any 
subsequent page.

### Installation
setup and configure a Python 3.5 virtualenv environment and use 
pip to install the requirements in the requirements.txt file.

`pip install virtualenv`

`cd <project path>`

`virtualenv -p </path/to/python3.5> virtualenv`

`source ./virtualenv/bin/activate` or just  `./virtualenv/Scripts/activate` if on Windows

`pip install -r requirements.txt`

### Usage
`python web_crawler.py [--target] <start_url> --logging_level`

Default domain is https://google.com
logging_level is set numerically as follows:

Logging Level | Numeric value to use
---      | ---
CRITICAL | 50
ERROR 	 | 40 (default)
WARNING  | 30
INFO     | 20
DEBUG    | 10
NOTSET   |  0

### Limitations

&lt;img&gt;, &lt;script&gt;, and &lt;link rel='stylesheet'&gt; tags are currently parsed for resources.

Only &lt;a&gt; tags are parsed for links, &lt;form&gt; tags are parsed for form-targets 

The output isn't pretty printed and is only created once a crawl is complete.

The error reporting isn't very useful, and potentially misleading.

It uses the standard Python html parser, which is slow, but avoids the need to install an additional parser such as lxml
