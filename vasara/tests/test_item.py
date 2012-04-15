from unittest import TestCase
from vasara.item import Item
from vasara.tests.common import build_test_site

TEST_ITEM = """---
{
    "name": "Test",
    "list": [1, 2, 3]
}
---

Hello, world! This is the actual content."""

class TestItem(TestCase):

    def setUp(self):
        self.site = build_test_site()
        self.item = Item(key="test", site=self.site, raw=TEST_ITEM)

    def test_content_matcher(self):
        """Tests that all metadata and actual content is properly parsed from input."""
        self.assertEqual(self.item.metadata["name"], "Test")
        self.assertEqual(self.item.metadata["list"], [1, 2, 3])
        self.assertEqual(self.item.raw_content, "Hello, world! This is the actual content.")

    def test_filter_not_twice(self):
        """Ensures that items don't filter themselves twice."""
        def increment_filter(item):
            if "counter" in item.metadata:
                item.metadata["counter"] += 1
            else:
                item.metadata["counter"] = 1

        self.item.filters.append(increment_filter)
        self.item.filter()
        self.item.filter() # Shouldn't do anything!

        self.assertEqual(1, self.item.metadata["counter"])

    def test_content_property(self):
        """Ensures that the item is filtered if the content property is retrieved."""
        def replacer_filter(item):
            item.filtered_content = "Unit Testing!"

        self.item.filters.append(replacer_filter)
        self.assertEqual("Unit Testing!", self.item.content)

    def test_templater_property(self):
        """Ensure that the item is templated if the templated property is retrieved."""
        def templater(item):
            return "Hello, test_templater_property!"

        self.item.templater = templater
        self.assertEqual("Hello, test_templater_property!", self.item.templated)

    def test_pretty_route(self):
        """Ensures that the pretty_route property displays a "prettified" route."""
        self.item.route = "test/index.html"
        self.assertEqual("test/", self.item.pretty_route)