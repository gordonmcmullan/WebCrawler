import unittest
import os
import sys

from urllib.request import urlopen
from urllib.error import URLError
from threading import Thread

from helpers import Platform
from helpers import TestHttpServer

from scraper.crawlcontroller import CrawlController

class TestCrawlController(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        loaded = False
        cls.server_thread = Thread(group=None, target=TestHttpServer)
        cls.server_thread.start()

        while not loaded:
            try:
                urlopen("http://localhost:9999")
                loaded = True
            except(URLError):
                pass

    @classmethod
    def tearDownClass(cls):
        cls.server_thread.join()
        TestHttpServer.stop_server()


    def test_crawl_controller_constructor(self):
        target = "http://localhost:9999/onelink.html"
        controller = CrawlController(target)
        self.assertIsInstance(controller, CrawlController)

    def test_page_without_links(self):
        target = "http://localhost:9999/hasscripts.html"

        expected = [{'url': target,
                     'assets': ["http://localhost:9999/script.js"],
                     'form-targets': [],
                     'links': []
                     }]

        controller = CrawlController(target)
        controller.start()

        self.assertListEqual(controller.results, expected)

    def test_page_with_link_in_same_domain(self):
        self.maxDiff = None
        target = "http://localhost:9999/page_relative_link.html"
        controller = CrawlController(target)
        controller.start()

        expected = [{'url': target,
                     'assets': [],
                     'form-targets': [],
                     'links': ['http://localhost:9999/nextpage.html']
                     },
                    {'url': "http://localhost:9999/nextpage.html",
                     'assets': [],
                     'form-targets': [],
                     'links': ['http://localhost:9999/nextpage.html']
                     }
                    ]

        self.assertListEqual(controller.results, expected)

    def test_page_with_link_in_different_domain(self):
        self.maxDiff = None

        target = "http://localhost:9999/cross_domain_link.html"

        expected = [{'url': target,
                     'assets': [],
                     'links': [],
                     'form-targets': []
                     }]

        controller = CrawlController(target)
        controller.start()

        self.assertListEqual(controller.results, expected)

if __name__ == '__main__':
    unittest.main()
