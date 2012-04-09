from unittest import TestCase
from vasara.site import Site
from common import build_test_site

import os

class TestSite(TestCase):

    def setUp(self):
        self.site = build_test_site()

    def test_scan(self):
        """Ensures that the item structure of a site is properly scanned."""
        self.assertIn("index", self.site.items)
        self.assertIn("test/test", self.site.items)
        self.assertIn("test/test/test", self.site.items)

    def test_match_items(self):
        """Ensures that the item matcher functions."""
        # Returns a tuple
        matches = self.site.match(r"(.*)")
        self.assertIsInstance(matches[0], tuple)

        # Returns match data and the item itself
        for match, item in matches:
            self.assertEqual(match.group(1), item.key)

    def test_route(self):
        """Ensures that routes are set properly on items."""

        # Set a global route for all items
        self.site.route(r"(.*)", lambda match, item: "{}/index.html".format(match.group(1)))
        # Override the index item's route
        self.site.route(r"index", lambda match, item: "index.html")

        self.assertEqual("index.html", self.site.items["index"].route)
        self.assertEqual("test/test/index.html", self.site.items["test/test"].route)

    def test_filter(self):
        """Ensures that filters are set properly on items."""

        # Set a global filter for all items
        self.site.filter(r"(.*)", lambda item: item)
        # Set another filter on the index item
        self.site.filter(r"index", lambda item: item)

        self.assertEqual(2, len(self.site.items["index"].filters))
        self.assertEqual(1, len(self.site.items["test/test"].filters))

    def test_templater(self):
        """Ensures that templaters are set properly on items."""

        # Set a global templater for all items
        self.site.template(r"(.*)", lambda item: "ALL")
        # Set another templater on the index item
        self.site.template(r"index", lambda item: "INDEX")

        # Since an item can only have one templater, the index templater should have been overwritten
        self.assertEqual("INDEX", self.site.items["index"].templated)
        self.assertEqual("ALL", self.site.items["test/test"].templated)