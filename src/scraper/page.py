from bs4 import BeautifulSoup
from urllib.parse import urlparse, urlunparse as urlbuild, urljoin
from urllib.error import HTTPError, URLError
from ssl import SSLError
import logging
import requests
from socket import gaierror

class Page:
    """
    Page Model for extracting data relevant to a web crawler from a page

        :param url An http or https url to load the web page from

    """

    ALLOWED_SCHEMES = ("http", "https")

    def __init__(self, url,):
        self.url = url
        self.uri = urlparse(url)
        doc = self.get_document()
        self.htmldoc = self.parse_html(doc)
        self.links = self.get_links()
        self.resources = self.getresources()
        self.form_targets = self.get_form_targets()

    #ToDo: This should popbly be indicated as a private method as it's only really needed by __init__()
    def get_document(self):
        """
        fetch the document from the url supplied when this Page is created
        """

        document = ""
        response = None

        try:
            response = requests.get(self.url, auth="")
            document = response.text

        except URLError:
            logging.error("URL Error, is \"%s\" a valid URL" % self.url)
        except HTTPError:
            # this could be transient e.g.an HTTP 503, should we retry?
            #Todo: Needs a test
            logging.error("HTTP Error fetching {}".format(self.url))
        except SSLError:
            #Todo: Needs a test
            logging.error("SSL Error fetching {}".format(self.url))
        except Exception:
            logging.error("An unexpected error happened fetching {}".format(self.url))

        if response is not None:
            response.close()
        return document

    def parse_html(self, doc):
        """
        Parse an HTML document into a Beautiful Soup tree using the default Python html parser.
        This is slow but doesn't require additional binary parsers to be installed

        :param doc:
        :return: Beautiful Soup object representation of the html document
        """
        try:
            htmldoc = BeautifulSoup(doc, 'html.parser')
        except:
            htmldoc = BeautifulSoup("<html><head></head></html>", 'html.parser')
        return htmldoc

    def get_links(self):
        anchors = self.htmldoc.find_all('a')
        links = set()
        for anchor in anchors:
            link = anchor.get('href')
            if link:
                uri = urlparse(link)

                if uri.scheme in self.ALLOWED_SCHEMES:
                    links.add(link)

                if not uri.netloc and not uri.scheme:
                    link = self.makeabsolute(link, uri)
                    links.add(link)
        return links

    def get_form_targets(self):
        """
        Parse an HTML page for forms and extract the target of each form.
        
        :return: a set of form submission targets in the current page
        """
        forms = self.htmldoc.find_all('form')
        form_targets = set()
        for form in forms:
            target = form.get('action')
            target = target if target else self.url
            form_targets.add(target)
        return form_targets


    def getresources(self):
        """

        :return:
        """

        #ToDo: Change this to a single pass by using self.htmldoc.find_all(('img', 'script', 'link'...))
        # It would be more efficient to extract all the assets in a single pass and, this would also
        # remove some of the duplication in the called methods
        resources = self.get_image_srcs()
        resources = resources.union(self.get_external_script_srcs())
        resources = resources.union(self.get_external_stylesheet_srcs())
        #ToDo: include video tags
        return resources

    def get_image_srcs(self):
        images = set()
        imgs = self.htmldoc.find_all('img')
        for img in imgs:
            src = img.get('src')
            if src:
                uri = urlparse(src)
                if not uri.netloc and not uri.scheme:
                    src = self.makeabsolute(src, uri)
                images.add(src)
        return images

    def get_external_script_srcs(self):
        scripts = set()
        script_tags = self.htmldoc.find_all('script')
        for script_tag in script_tags:
            src = script_tag.get('src')
            if src:
                uri = urlparse(src)
                if not uri.netloc and not uri.scheme:
                    src = self.makeabsolute(src, uri)
                scripts.add(src)
        return scripts

    def get_external_stylesheet_srcs(self):
        stylesheets = set()
        link_tags = self.htmldoc.find_all('link', rel="stylesheet")
        for link_tag in link_tags:
            href = link_tag.get('href')
            if href:
                uri = urlparse(href)
            if not uri.netloc and not uri.scheme:
                href = self.makeabsolute(href, uri)
            stylesheets.add(href)
        return stylesheets

    #ToDo: Maybe Move this into a utility class, it's possibly reusable
    def makeabsolute(self, link, uri):
        if link[0] == "/":
            location = urlbuild((self.uri.scheme, self.uri.netloc, uri.path, uri.params, uri.query, uri.fragment))
        else:
            base = urlbuild((self.uri.scheme, self.uri.netloc, self.uri.path, "", "", ""))
            location = urljoin(base, link)
        return location