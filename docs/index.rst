Welcome to Flask-Triangle
=========================

**With great UX comes great security needs.** *Uncle Ben*

*Flask-Triangle is utterly influenced by*
`Flask-WTF <https://flask-wtf.readthedocs.org/en/latest/>`_. *It aims to provide
you with similar features : form input handling and validation. The main
difference is that Flask-Triangle is designed with*
`AngularJS <http://angularjs.org/>`_ *and* 
`XHR <https://en.wikipedia.org/wiki/XMLHttpRequest>`_ *in mind.*

The Idea
--------

The idea behind Flask-Triangle is to provide a way to describe the expected data
on a per-object basis the same way as you can describe your data model (like the
SQLAlchemy's ORM for example).

This description is intended to generate an HTML fragment directly usable in
your templates as a form and a `JSON-schema <http://json-schema.org/>`_ to 
validate the data received from it. 

The use of HTML5 with AngularJS and JSON-schema lets you define a full
validating chain (client-side and server-side) in one place.

User's Guide
------------

This documentation will show you how to get started in using Flask-Triangle with
Flask.

.. toctree::
   :maxdepth: 2

   installing
   glance

