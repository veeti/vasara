import os
import io
import re
import sys
from vasara.item import Item

class Site(object):

    def __init__(self, base_path, items_path):
        self.base_path = base_path
        self.items_path = items_path
        self.items = {}
        self.scan()

    def scan(self):
        """Scans the site's items path for items."""
        path = os.path.abspath(self.items_path)
        for dirpath, dirnames, filenames in os.walk(path):
            for file in filenames:
                full = os.path.abspath(os.path.join(dirpath, file))
                key = os.path.splitext(full[len(path):])[0][1:]

                # If on Windows, fix path separators in the key
                if sys.platform == "win32":
                    key = key.replace("\\", "/")

                self.items[key] = Item(key=key, site=self, raw=io.open(full, "r").read())

    def match(self, expression):
        """Matches the site's items against the specified regular expression
        and returns them in a list of tuples; the first item in a tuple being the
        match object and the second being the item itself."""
        exp = re.compile(expression)
        keys = self.items.keys()
        items = []
        for key in keys:
            match = exp.match(key)
            if match:
                items.append((match, self.items[key]))
        return items

    def route(self, expression, callable):
        for match, item in self.match(expression):
            item.route = callable(match, item)

    def filter(self, expression, filter):
        for match, item in self.match(expression):
            item.filters.append(filter)

    def template(self, expression, templater):
        for match, item in self.match(expression):
            item.templater = templater