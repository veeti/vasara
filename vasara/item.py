import json
import re

# This regex pattern has been shamelessly lifted from Mynt, licensed under the
# BSD license. Mynt is available at https://github.com/Anomareh/mynt
MATCHER = re.compile(r"\A---\s+^(.+?)$\s+---\s*(.*)\Z", re.M | re.S)

class Item(object):

    def __init__(self, filename, site, raw, route=None):
        self.filename = filename
        """The item's filename."""
        self.site = site
        """The item's :class:`Site`."""
        self.raw_content = raw
        """The raw, unprocessed contents of the item."""
        self.file_route = route
        """The item's output path."""
        self.filters = []
        """A list of the item's filters. See :func:`example.filter`."""
        self.filtered = False
        """Specifies if the item has already gone through filtering."""
        self.templater = None
        """The item's templater. See :func:`example.templater`."""
        self.metadata = {}
        """Any metadata associated with the file."""

        # Read metadata if it exists
        match = MATCHER.match(self.raw_content)
        if match and len(match.groups()) == 2:
            self.metadata = json.loads(match.groups()[0])
            self.raw_content = match.groups()[1]

        self.filtered_content = self.raw_content
        """The filtered contents of the item. Should be manipulated by filters. Don't get this directly."""

    def filter(self):
        """Runs all the specified filters on the item. For convenience, returns itself.

        (Will not filter if the item has already been filtered.)

        :returns: self"""
        if self.filtered is False:
            for filter in self.filters:
                filter(self)

        self.filtered = True
        return self

    @property
    def content(self):
        """Generates the item's final, filtered contents.

        :returns: contents"""
        return self.filter().filtered_content

    @property
    def templated(self):
        """Generates the item's final, filtered contents templated with the specified :attr:`~Item.templater`.

        :returns: templated contents"""
        # Make sure that the item has been filtered
        self.filter()
        if self.templater is None:
            return self.content
        return self.templater(self)

    @property
    def route(self):
        """Generates a "pretty" route for the item based on its file route. Omits index.html from the
        end of paths for cleaner URL's.

        :returns: URL"""
        return self.file_route.replace("/index.html", "/")