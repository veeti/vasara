import os
import io
import re
import sys
from vasara.item import Item

class Site(object):

    def __init__(self, base_path, items_path):
        """Constructor.

        :param base_path: absolute base path for site
        :param items_path: absolute path to site items"""

        self.base_path = base_path
        self.items_path = items_path
        self.items = {}
        """A dictioanry of the site's items."""
        self.scan()


    def scan(self):
        """Scans the site's items path for items."""
        path = os.path.abspath(self.items_path)
        for dirpath, dirnames, filenames in os.walk(path):
            for file in filenames:
                full = os.path.abspath(os.path.join(dirpath, file))
                key = full[len(path):][1:]

                # If on Windows, fix path separators in the key
                if sys.platform == "win32":
                    key = key.replace("\\", "/")

                self.items[key] = Item(filename=key, site=self, raw=io.open(full, "r").read())

    def match(self, expression):
        """Matches the site's items against the specified regular expression
        and returns them.

        :param expression: regular expression to match against item filename
        :returns: list of tuples: [(match, item)]"""
        exp = re.compile(expression)
        keys = self.items.keys()
        items = []
        for key in keys:
            match = exp.match(key)
            if match:
                items.append((match, self.items[key]))
        return items

    def route(self, expression, callable):
        """Matches and routes items using the specified router. See :func:`example.router` for more details on the ``callable``.

        :param expression: regular expression to match against item filename (see :func:`~Site.match`)
        :param callable: a callable object that takes two arguments: ``match`` and ``item`` and returns the route"""
        for match, item in self.match(expression):
            item.file_route = callable(match, item)

    def filter(self, expression, filter):
        """Matches and filters items using the specified filter. See :func:`example.filter` for more details on the ``filter``.

        :param expression: regular expression to match against item filename (see :func:`~Site.match`)
        :param filter: a callable object that takes the item as an argument"""
        for match, item in self.match(expression):
            item.filters.append(filter)

    def template(self, expression, templater):
        """Matches and templates items using the specified templater. See :func:`example.templater` for more details on the ``templater``.

        :param expression: regular expression to match against item filename (see :func:`~Site.match`)
        :param templater: a callable object that takes the item as an argument"""
        for match, item in self.match(expression):
            item.templater = templater