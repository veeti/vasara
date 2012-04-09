from vasara.site import Site

import os

TEST_SITE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_site")

def build_test_site():
    site = Site(base_path=TEST_SITE, items_path=os.path.join(TEST_SITE, "items"))
    return site