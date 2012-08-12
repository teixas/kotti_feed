==========
kotti_feed
==========

This is an extension to the Kotti CMS that allows you to generate RSS
2.0 feeds from your Kotti site.

`Find out more about Kotti`_

Setting up
==========

To setup which content types should be available on RSS feeds set the
``kotti_feed.content_types`` variable. An example configuration::

 kotti.configurators = 
   kotti_tinymce.kotti_configure
   kotti_feed.kotti_configure
 kotti_feed.content_types = document image

.. _Find out more about Kotti: http://pypi.python.org/pypi/Kotti
