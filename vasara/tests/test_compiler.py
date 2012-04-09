from unittest import TestCase
from vasara.item import Item
from vasara.site import Site
from vasara.compiler import Compiler

from common import build_test_site, TEST_SITE

import os
import shutil
import sys

HERE = os.path.abspath(os.path.dirname(__file__))

class TestCompiler(TestCase):

    def setUp(self):
        self.site = build_test_site()
        self.compiler = Compiler(site=self.site, output_path=os.path.join(TEST_SITE, "output"))

        if HERE not in self.compiler.output_path:
            sys.exit("Something is terribly wrong. {}, {}".format(HERE, self.compiler.output_path))

        if os.path.exists(self.compiler.output_path):
            shutil.rmtree(self.compiler.output_path)

    def test_routing(self):
        """Ensures that compilation results are routed properly."""
        self.site.route(r"(.*)", lambda match, item: "{}/index.html".format(match.group(1)))
        self.site.route(r"index", lambda match, item: "index.html")
        self.compiler.compile()

        output = self.compiler.output_path
        self.assertTrue(os.path.exists(os.path.join(output)))
        self.assertTrue(os.path.exists(os.path.join(output, "index.html")))
        self.assertTrue(os.path.exists(os.path.join(output, "test", "index.html")))
        self.assertTrue(os.path.exists(os.path.join(output, "test", "test", "index.html")))
        self.assertTrue(os.path.exists(os.path.join(output, "test", "test", "test", "index.html")))