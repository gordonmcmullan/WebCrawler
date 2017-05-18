import argparse
import json
import logging

from scraper.crawlcontroller import CrawlController

parser = argparse.ArgumentParser(description="Crawl Web Pages")
parser.add_argument('--target',
                    type=str,
                    nargs='?',
                    default="https://gocardless.com/",
                    help='Start point for the crawl default is https://gocardless.com/')

parser.add_argument('--logging_level',
                    type=str,
                    nargs='?',
                    default=logging.ERROR,
                    help='Start point for the crawl default is https://gocardless.com/')

args = parser.parse_args()
logging.debug("Starting a webcrawl at %s" %args.target)
controller = CrawlController(args.target, args.logging_level)
controller.start()
# ToDo: Stream the output
print(json.dumps(controller.results))
