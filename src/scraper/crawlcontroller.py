from scraper.page import Page
from collections import deque
from urllib.parse import urlparse
import logging

class CrawlController:
    """
    :param Url to start crawling from
    :param logging level default: INFO
    """

    def __init__(self, startpoint, logging_level=logging.INFO):
        logging.basicConfig(level=logging_level)
        self.tocrawl = deque([startpoint])
        self.crawled = set()
        self.results = []

    def start(self):
        """
        Begin crawling
        :return: boolean - currently always true
        """
        while self.tocrawl:
            target = self.tocrawl.popleft()
            logging.info('\tparsing %s' % target)
            page = Page(target)
            result = {'url': page.url,
                      'assets': list(page.resources),
                      'links': list(page.links),
                      'form-targets': list(page.form_targets)}
            self.results.append(result)
            self.crawled.add(target)
            for link in page.links:
                if self.samedomain(target, link):
                    if not link in self.crawled and not link in self.tocrawl:
                        self.tocrawl.append(link)
        #ToDo: add error handling and return False if crawling fails
        return True

    #ToDo: Maybe Move this into a utility class, it's possibly reusable
    def samedomain(self, target, link):
        """
        Determine if two links are in the same domain
        :param target: string representing a web url
        :param link: string representing a web url
        :return: boolean
        """
        samedomain = False
        target_uri = urlparse(target)
        link_uri = urlparse(link)
        if (target_uri.hostname == link_uri.hostname):
            samedomain = True
        return samedomain

