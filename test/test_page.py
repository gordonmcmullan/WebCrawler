from scraper.page import Page
from helpers import TestHttpServer, Platform

from threading import Thread
from urllib.parse import urlparse, urlunparse as urlbuild
from urllib.request import urlopen
from urllib.error import URLError

import os
import logging
import unittest

class Test_Page(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        loaded = False
        logging.basicConfig(level=logging.INFO)

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
        TestHttpServer.stop_server()
        #Todo: Could be a litttle more robust, the server sometime seems to hang on exit
        cls.server_thread.join()

    def test_page_load_httpurl(self):
        target = "http://localhost:9999/"
        mypage = Page(target)
        self.assertEqual(mypage.url, target)

    def test_page_without_valid_url_fails(self):
        target = "http://notarealexample.none/"
        mypage = Page(target)
        self.assertRaises(URLError)

    def test_page_with_one_link(self):
        target = "http://localhost:9999/onelink.html"
        mypage = Page(target)
        self.assertSetEqual(mypage.links,set(["http://localhost/nextpage"]))

    def test_unsupported_scheme(self):
        target = "http://localhost:9999/unsupported_scheme.html"
        mypage = Page(target)
        self.assertSetEqual(mypage.links,set([]))

    def test_server_relative_link(self):
        target = "http://localhost:9999/server_relative_link.html"
        target_url = urlparse(target)
        testlink = urlbuild((target_url.scheme, target_url.netloc, "/nextpage.html", "", "", ""))
        mypage = Page(target)
        self.assertSetEqual(mypage.links,set([testlink]))

    def test_relative_link(self):
        target = "http://localhost:9999/page_relative_link.html"
        mypage = Page(target)
        self.assertSetEqual(mypage.links,set(["http://localhost:9999/nextpage.html"]))

    def test_image(self):
        target = "http://localhost:9999/hasimage.html"
        mypage = Page(target)
        self.assertSetEqual(mypage.resources, set(["http://localhost:9999/image.jpg"]))

    def test_script(self):
        target = "http://localhost:9999/hasscripts.html"
        mypage = Page(target)
        self.assertSetEqual(mypage.resources, set(["http://localhost:9999/script.js"]))

    def test_stylesheet(self):
        target = "http://localhost:9999/hasstylesheet.html"
        mypage = Page(target)
        self.assertSetEqual(mypage.resources, set(["http://localhost:9999/stylesheet.css"]))

    def test_form_with_action(self):
        target = "http://localhost:9999/hasformwithaction.html"
        mypage = Page(target)
        self.assertSetEqual(mypage.form_targets, set(["/formaction"]))

    def test_form_without_action(self):
        target = "http://localhost:9999/hasformwithoutaction.html"
        mypage = Page(target)
        self.assertSetEqual(mypage.form_targets, set(["http://localhost:9999/hasformwithoutaction.html"]))

    def test_form_with_button_with_formaction(self):
        target = "http://localhost:9999/hasformwithbuttonactionoverride.html"
        mypage = Page(target)
        self.assertSetEqual(mypage.form_targets, set(["/formaction", "/button-override"]))

    def test_form_with_input_with_formaction(self):
        target = 'http://localhost:9999/hasformwithactionoverride.html'
        mypage=Page(target)
        result = mypage.form_targets
        expected = set(["/formaction", "/overrideaction"])
        self.assertSetEqual(result, expected)

    def test_form_with_multiple_formactions(self):
        target = "http://localhost:9999/hasformwithbuttonandinputactionoverride.html"
        mypage = Page(target)
        result = mypage.form_targets
        expected = set(["/formaction", "/button-override", "/input-override"])
        self.assertSetEqual(result, expected)

if __name__ == '__main__':
    unittest.main()