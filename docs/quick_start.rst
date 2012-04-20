Introductory tutorial
=====================

Let's create a simple website with vasara that shows off some of the most basic features.

Creating the site
-----------------

A vasara site can be structured in any way that you want to, but a good basic structure is one like the following::

    - mysite
      - items
      - output
      __init__.py

The ``__init__`` module should contain a single function called ``get_vasara_compiler()`` that returns a :class:`Compiler` instance for your site. (Technically this is only required if you want to use the ``vsra`` command line utility to work with the site. We'll assume that you do.)

Let's get started::

    $ mkdir mysite
    $ cd mysite
    $ mkdir items
    $ touch __init__.py

Add this to ``__init__.py``:

.. code-block:: python
    :linenos:

    from vasara import Site, Compiler
    from os.path import join, dirname, abspath

    BASE_PATH = dirname(abspath(__file__))

    def get_vasara_compiler():
        site = Site(
            base_path=BASE_PATH,
            items_path=join(BASE_PATH, "items")
        )
        compiler = Compiler(
            site=site,
            output_path=join(BASE_PATH, "output")
        )

        return compiler

Let's go through this code and figure out what we're doing:

* On the first and second lines we import some classes and functions. The :class:`Site` and :class:`Compiler` classes are essential parts of a vasara site. We also import some file path handling functions from the Python standard library.

* On the fourth line we define a variable called ``BASE_PATH``. This variable contains an absolute path to the directory where ``__init__.py`` is located, and it's the "base path" of our site.

* As mentioned above, a function called ``get_vasara_compiler`` is required. In this function, we instantiate a new :class:`Site` and a :class:`Compiler` for the site. The site contains all information about the website: the items it consists of and more. The compiler takes a site and compiles it. We define the path to the site's *items* and the compiler's *output* path.

* We return the compiler.

When calling ``vsra``, it will look for the ``get_vasara_compiler`` method in the current working directory and will throw an error if it doesn't exist::

    (in mysite)
    $ vsra
    usage: vsra [-h] {compile} ...

    $ cd ..
    $ vsra
    A site doesn't seem to exist in the working directory. Exiting.

Adding an item
--------------

If we try to compile our site with ``vsra compile``, nothing exciting will happen (yet). This is because we have no items (pages) on our site. Websites usually consist of many pages: for example, a blog's each post would have its own :class:`Item`.

When a new instance of :class:`Site` is created, it automatically scans the specified item path for items and adds them to the site. Each item exists as an instance of :class:`Item`. Let's try this out by creating a new item called ``index`` (each item is identified in your site by its ``key``). Create a new file called ``index.html`` in the ``items`` directory, and write this in it:

.. code-block:: html

    <h1>Hello, vasara!</h1>

However, we aren't done yet. Let's try compiling the site::

    $ vsra compile
    Item index has no route. Skipping.

vasara knows that the item is there, but it doesn't know where to put it. We need to add a *route* for it. Since this is the front page of our website, we probably want it to be saved as just ``index.html`` to the root of the output directory.

Open ``__init__.py`` and add this after the site declaration:

.. code-block:: python
    :linenos:

    site.items["index"].file_route = "index.html"

As mentioned before, each :class:`Item` has its own **key**. This key is automatically generated from its path on the filesystem: the file extension is omitted from the key. All the :class:`Site`'s items are accessible from the ``items`` property.

Compile the site again. If you look at the ``output`` directory, you can see that a file called ``index.html`` now exists in it. Open it: the contents will look very familiar.

Adding new pages
----------------

It looks like things are finally starting to get exciting. Let's add a couple of other pages, just to test vasara out a little more.

Create and open ``items/about.html`` and add some contents to it. For example:

.. code-block:: html

    <h1>About us</h1>

    <p>Bob's garden gnomes is a family business. We have been trading for hundreds of years now.</p>

Just like with the ``index`` item, our ``about`` item also needs to be routed somewhere. We could do it the same way we did with ``index``, or we could try out a more powerful routing function in vasara. :class:`Site` has a function called :func:`Site.route`, which lets you use *regular expressions* to match items by their key and apply routes to them.

.. note::

    If you're not very familiar with Python's ``re`` module or regular expressions in general, you may want to familiarize yourself with them and skip this section for now.

:func:`~Site.route` expects a callable. This callable is a *router function* that will return the desired route for each item. Here's what we'll be using:

.. code-block:: python
    :linenos:

    def my_router(match, item):
        return "{}.html".format(item.key)

If you were to associate this router with the ``index`` item, the route it would return would be ``index.html`` - based on the item's key. Of course, since routers are ordinary Python functions, you can do all kinds of complex logic to route your items.

Let's put this router into use. Remove the route for ``index`` that we added in the last section, and put in this instead:

.. code-block:: python

    def my_router(match, item):
        return "{}.html".format(item.key)

    site.route(r"(.*)", my_router)

Notice how the ``my_router`` function is passed to the :func:`~Site.route` function and not the result of calling my_router.

All the items that match with the regular expression defined (in this case, every item) will be routed with ``my_router``.

.. note::

    A more detailed introduction to items and routes can be found in the next chapter. For now, compile the site and look at the output result: both items will now exist in the output directory.

Trying out filters
------------------

What if we want to modify (*filter*) the contents of an item before it's compiled? For example, items could be written in an intermediary markup language like Textile that can be converted to plain HTML.

For the purposes of this tutorial, we want to keep things simple and avoid any external library dependencies, so let's do something a bit different. Modify ``index.html`` to something like this:

.. code-block:: html

    <h1>Hello, vasara!</h1>

    <p>One plus one equals {}</p>

(Hopefully you're familiar enough with Python to recognize ``{}`` as a replacement field. We can use string formatting to replace the ``{}`` with anything we want to.)

We want to compute the result of ``1 + 1`` and replace the ``{}`` in our ``index`` item before it's written to disk. To accomplish this, we can define a ``filter`` function. Filters are very simple, and here's the one that we're going to be using:

.. code-block:: python

    def calculate_one_plus_one(item):
        item.filtered_content = item.filtered_content.format((1 + 1))

Our filter is very simple: we manipulate the :attr:`Item.filtered_content` attribute of an item to change its output contents. (The attribute is initially set to the unfiltered contents).

But how do we add this filter to our item? Well, there are two ways to do this:

* Get the item manually from the :class:`Site` and associate the filter with it.

* Use the :func:`Site.filter` function, which works just like :func:`Site.route` does.

We'll pick the first method, since we only want to filter ``index``. Add this to ``__init__.py``:

.. code-block:: python

    site.items["index"].filters.append(calculate_one_plus_one)

Notice that each :class:`Item` has a list of filters. This is an ordinary Python list and you can do whatever you want to with it.

Compile the site and open ``output/index.html``. Here's what you should see:

.. code-block:: html

    <h1>Hello, vasara!</h1>

    <p>One plus one equals 2</p>

Amazing!

Adding a template
-----------------

Any website worth visiting is built on a basic template with elements that are visible on all pages: a header, a footer, maybe a sidebar. There are many ways to accomplish this. Let's look into *templaters* which can be used to integrate a templating engine into our site.

A templater is very similar to a filter. It takes the item as an argument and must return the templated contents of the item.

Let's build a basic template for our site. It won't be pretty, but it'll work for the purposes of this demo:

.. code-block:: html

    <!DOCTYPE HTML>
    <html>
        <head>
            <title>Test website</title>
        </head>
        <body>
            <a href="/">Front page</a> - <a href="/about.html">About</a>
            {content}
        </body>
    </html>

Applying this basic template to our items is very simple: we just need to define a *templater* function on the item. Here's what we'll use:

.. code-block:: python

   def templater(item):
       return """<!DOCTYPE HTML>
                 <html>
                     <head>
                         <title>Test website</title>
                     </head>
                     <body>
                         <a href="/">Front page</a> - <a href="/about.html">About</a>
                         {content}
                     </body>
                 </html>""".format(content=item.content)

Once again, applying a templater to an item works just like with routes and filters. Let's use the expression syntax:

.. code-block:: python

    site.template(r"(.*)", templater)

Compile the site. Notice how we now have a navigation at the top of the page!

What's next?
------------

This has been a very basic introduction to vasara and the core features like routes and filters. The following chapters are a more in-depth introduction to vasara.
