Introduction
============

**vasara** (*hammer*) is a small static site generator written in the Python programming language. Unlike some other static site generators, vasara is designed to be minimalistic. It only handles the most essential features for a static website:

**Routing**:

	Mapping different pages (known as *items* in vasara) to specific output paths. For example, an item with the key ``hello/world`` could be routed to ``hello/world/index.html``.

**Filtering**:

	Instead of writing items directly in HTML, it may be a good idea to use a markup language like Markdown_, Textile_ or reStructuredText_. These languages are more readable than plain HTML and also take out the trouble of escaping different character entities, etc. vasara lets you define multiple filters on the content of items, but does not include any default filters: the choice is up to you.

**Templating**:

	A website usually consists of multiple parts: for example, a header, the content block and a footer. Instead of duplicating this in every item, these common parts should be split into a template file. Just like with filters, the choice of a template engine is yours: vasara does not depend on any specific template engine. You can use anything from Python's string formatting functions to powerful templating engines like Jinja2_ or Mako_.

In summary, vasara abstracts out the boring stuff while leaving you in ultimate control.

.. note::
   You may be wondering why the documentation for vasara has been generated with Sphinx and not vasara itself. The answer is simple: Sphinx is the standard documentation generator for Python libraries and applications, and it is a very powerful tool designed for creating documentation. The same thing could be accomplished with vasara, but why reinvent the wheel?

Installation
------------

Right now, vasara only exists as an experimental tool in a git repository hosted at Github. So `clone the source`_ and do the following::

	cd vasara
	python setup.py develop

This will set you up to use the latest development version.

Sites using vasara
------------------

Here are some websites built with vasara:

* `Veeti Paananen`_: the personal website and blog of Veeti Paananen
* More coming soon?


.. _reStructuredText: http://docutils.sourceforge.net/rst.html
.. _Markdown: http://daringfireball.net/projects/markdown/
.. _Textile: http://www.textism.com/tools/textile/
.. _Jinja2: http://jinja.pocoo.org/docs/
.. _Mako: http://www.makotemplates.org/

.. _clone the source: http://github.com/rojekti/vasara/

.. _Veeti Paananen: http://veetipaananen.fi/