Items
=====

.. currentmodule:: vasara

Each page of your site is an **item**. Items are stored in the site's :attr:`~Site.items_path`. When a site is created, that path is automatically scanned for items and they are added to the site's :attr:`~Site.items` dictionary. :attr:`Site.items` stores items by their filename (which is also accessible as :attr:`Item.filename`).

Note that nothing prevents you from doing all sorts of magic with your code and creating :class:`Item` objects manually and adding them to the site. For example, category pages for blog posts could be generated dynamically.

Routing
-------

An item points to a specific output path which is called the :attr:`Item.file_route`. For example, if an item has the `file_route` of ``index.html``, it will be written to ``output_path/index.html``.

There are two ways to define routes:

Manual routing
~~~~~~~~~~~~~~

Since a route is just an attribute on an item, it can be set manually. For example:

.. code-block:: python

    site.items["index.html"].file_route = "hello_world.html"

Using the route helper
~~~~~~~~~~~~~~~~~~~~~~

The :class:`Site` has a function called :meth:`~Site.route` that lets you easily use regular expressions to apply routes to multiple items. To use :meth:`~Site.route`, you need to create a *router function*:

.. currentmodule:: example
.. function:: router(match, item)

    Defines the :attr:`~Item.file_route` for an :class:`Item`.

    :param match: match result against :attr:`Item.filename` from :meth:`Site.route`
    :param item: the item being routed
    :returns: :attr:`~Item.file_route` to be set for :class:`Item`
    :rtype: str
.. currentmodule:: vasara

When :meth:`~Site.route` is called, each item of the site is matched against the specified regular expression. If a match is found, the router function is called - and the ``match`` argument contains the ``re`` match object. The ``item`` argument is the :class:`Item`. The router function should return the :attr:`~Item.file_route` for the :class:`Item`.

For example:

.. code-block:: python

    def my_router(match, item):
        import os
        if item.filename == "index.html":
            return item.filename
        return "{}/index.html".format(os.path.splitext(item.filename)[0])

(``os.path.splitext`` is used to remove the trailing file extension from the item's filename - for example, ``products/garden-gnome.html`` becomes ``products/garden-gnome``.)

Depending on the level of complexity that you want to have with your site's routers, a simple router like this could work for all of your items. Here's an example of the paths it would map for different items:

* ``item path`` -> ``item key`` -> ``file route``
* ``index.html`` -> ``index`` -> ``index.html``
* ``products.html`` -> ``products`` -> ``products/index.html``
* ``products/garden-gnome.html`` -> ``products/garden-gnome`` -> ``products/garden-gnome/index.html``

This is a common style of routing used by many other static site generators.

.. note::

    Since each item has its own directory and its file is called ``index.html``, this means that you can omit the ``index.html`` from the paths completely. This results in nicer URL's like ``http://www.garden-gnomes.example/products/garden-gnome/``.

Applying this router with the :meth:`Site.route` function is easy:

.. code-block:: python

    site.route(r".*", my_router)

Filters
-------

You might need to do some sort of processing on the raw item contents before the item is compiled. For example, a blogger might want to write their posts in Markdown_ instead of raw HTML. This can be accomplished with *filters*.

Each item has a ``list`` of filters called :attr:`Item.filters`. You are free to manipulate this list as you wish, and a helper method like :meth:`Site.route` also exists. It's obviously called :meth:`Site.filter`.

A filter is just a simple Python function:

.. currentmodule:: example
.. function:: filter(item)

    A function that filters the contents of an :class:`Item`. Should manipulate the :attr:`Item.filtered_content` attribute.

    :param item: the item being filtered
    :returns: nothing
.. currentmodule:: vasara

For example, if we wanted to filter posts using a fictional markup language called reTextDown and its Python module would contain a single function called ``retextdown_text``, we could wrap this function with a filter like this:

.. code-block:: python

    from retextdown import retextdown_text

    def retextdown_filter(item):
        item.filtered_content = retextdown_text(item.filtered_content)

.. warning::

    Don't use the :attr:`Item.content` attribute in a filter. :attr:`~Item.content` is a property that does two things: it filters the item if necessary and returns the filtered contents. If you call it during filtering, it might result in an infinite loop and the end of the world.

We can add the filter to our items:

.. code-block:: python

    # Manipulate the filters directly
    site.items["index.html"].filters.append(retextdown_filter)

    # Use Site.filter
    site.filter(r".*", retextdown_filter)

And we're done.

Templaters
----------

A website usually has a header and a footer. Instead of duplicating these elements in every single item, we can apply a *templater function* to the items that takes care of it for us.

.. currentmodule:: example
.. function:: templater(item)

    A function that templates the contents of an :class:`Item`.

    :param item: the item being templated
    :returns: templated contents
    :rtype: str
.. currentmodule:: vasara

For example, if we wanted to make a lasting impression on the visitor, we could create a templater like this:

.. code-block:: python

    def my_templater(item):
        return "<blink>{}</blink>".format(item.content)

And apply it (you know this already):

.. code-block:: python

    # Manipulate the templater directly
    site.items["index.html"].templater = my_templater

    # Use Site.template
    site.template(r".*", my_templater)

And we're done!

.. note::

    Be sure to use :attr:`Item.content` in the templater to fetch the item's contents. This ensures that all filters have been run on the item.

(More realistically speaking, you could just wrap the contents in your own HTML template or use a complete template engine like Jinja2_ or Mako_.)

A note on applying routes and templaters
----------------------------------------

If you're using :meth:`Site.route`/:meth:`~Site.template` to apply your routes and templaters, note that the call order matters. If you call the function twice and the same item is matched twice, the last call will overwrite the first one.

For example:

.. code-block:: python

    site.route(r"index.html", router_one)
    site.route(r"index.html", router_two)

Will set ``router_two``'s output as the ``index`` item's route.

Metadata
--------

vasara supports associating *metadata* with each item. For example, a blog site could store a ``date`` field with each item, which could be used to programmatically find and sort posts from different dates.

Metadata is stored in a JSON object at the beginning of each file. For example:

.. code-block:: text

    ---
    {
        "date": "2012-04-22",
        "hello": "world"
    }
    ---

    Hello, world! This is the actual content area of the item.

The section of the item separated by three dashes (``---``) will automatically be picked up by vasara. It will try to parse the string inside as JSON and save the result to :attr:`Item.metadata`. The metadata of this item could then be accessed like this:

.. code-block:: python

    >>> item.metadata["date"]
    "2012-04-22"

As a practical example, a templater could read an item's ``title`` metadata attribute and set it as the page's HTML ``<title>``.

.. _Markdown: http://daringfireball.net/projects/markdown/

.. _Jinja2: http://jinja.pocoo.org/docs/
.. _Mako: http://www.makotemplates.org/