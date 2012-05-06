from vasara.item import Item
from vasara.site import Site

import io
import os

class Compiler(object):

    def __init__(self, site, output_path):
        self.site = site
        self.output_path = output_path
        """Absolute path to the output directory in disk."""

    def compile(self):
        """Compiles and writes all the items to disk."""
        if not os.path.exists(self.output_path):
            os.makedirs(self.output_path)

        for key, item in self.site.items.iteritems():
            content = item.templated
            route = item.file_route

            if route is None:
                print "Item {} has no route. Skipping.".format(item.filename)
                continue

            path = os.path.join(self.output_path, route)
            path_dir = os.path.dirname(path)

            if not os.path.exists(path_dir):
                os.makedirs(path_dir)

            file = io.open(path, "wb")
            file.write(content)
            file.close()