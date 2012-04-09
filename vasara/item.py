import json
import re

# This regex pattern has been shamelessly lifted from Mynt, licensed under the
# BSD license. Mynt is available at https://github.com/Anomareh/mynt
MATCHER = re.compile(r"\A---\s+^(.+?)$\s+---\s*(.*)\Z", re.M | re.S)

class Item(object):

    def __init__(self, key, site, raw, route=None):
        self.key = key
        self.site = site
        self.raw_content = raw
        self.route = route
        self.filters = []
        self.filtered = False
        self.templater = None

        # Read data
        matches = MATCHER.match(self.raw_content).groups()
        self.metadata = json.loads(matches[0])
        self.raw_content = matches[1]
        self.filtered_content = self.raw_content

    def filter(self):
        """Runs all the specified filters on the item. For convenience, returns itself."""
        if self.filtered is False:
            for filter in self.filters:
                filter(self)

        self.filtered = True
        return self

    @property
    def content(self):
        return self.filter().filtered_content

    @property
    def templated(self):
        # Make sure that the item has been filtered
        self.filter()
        if self.templater is None:
            return self.content
        return self.templater(self)

    @property
    def pretty_route(self):
        return self.route.replace("/index.html", "/")