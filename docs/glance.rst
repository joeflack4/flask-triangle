A glance at ...
===============

*The snippets on this page aren’t intended to be a complete demonstration of all
the features provided by Flask-Triangle but a sufficient glance to be able to
understand the most important of them.*


Widgets
-------

The ``Widget`` is the base component of Flask-Triangle and must be understood
before going any further. Each widget represents a given type of input you want
to put in an HTML source code.

To instantiate a widget, you must specify at least those arguments :

    - its Angular's ``bind``\ ing
    - its ``name``

::

    Widget('angular.binding', name='mywidget')


Then there is additionnal arguments common to all widgets and specific 
keyword-arguments to setup advanced behaviors of a particular widget type. You
will find more about it later in this documentation.


Forms
-----

The ``Form`` is a widget container by analogy to the ``<form>`` HTML element.
You must subclass it in your own classes like the following example::

    from flask.ext.triangle import Form
    from flask.ext.triangle.widgets.standard import TextInput 

    class MyForm(Form):

        username = TextInput('user.name', pattern='^[a-z_]$')
        description = TextInput('user.description')

When missing, the widget's name is extrapolated from the property name.
*Note: the property* ``schema`` *is reserved to hold the validation schema of
the form. If you need a widget named schema, use the* ``name`` *argument
explicitly.*

Finally, you can render a ``Form`` instance ``form`` in a template ::

  <form name="myform">
    {% for widget in form %}
      <label>{{widget.label}}</label> {{widget()}}
    {% endfor %}
  </form>

A ``Form`` instance is iterable and the declaration order of the widgets is
guaranteed, direct access to the properties remains available !


Validation
----------

The other goal of a form is to compile and provide the validating JSON-schema of
it. The validation process is provided by a function of Flask-Triangle::

    from flask.ext.triangle import validate

    form = MyForm(vroot='user')
    validate(form, parsed_json)

When instantiating a ``Form`` object, the optional ``vroot`` argument lets you
define the subschema to use in the validation. To illustrate this, the raw
schema of a ``MyForm`` instance expect to validate something like this::

    {
        "user": {
            "username": "a_valid_value",
            "description": "A description of the user."
        }
    }

The fact is because the top-level container was defined for the confort¹ you are
more susceptible to receive this from the client::

    {
        "username": "a_valid_value",
        "description": "A description of the user."
    }

The virtual root (*vroot*) lets you do this and supports the dotted notation of
Javascript.

¹ : the client code is generally something like this :


Helpers
-------

Flask-Triangle comes with some helpers.

The angular filter
^^^^^^^^^^^^^^^^^^

The filter ``angular`` helps you to mix AngularJS templating features with 
Jinja::

    >>> from jinja2 import Template

    >>> template = Template('<span>{{angular.template.value|angular}}</span>')
    >>> template.render()
    '<span>{{angular.template.value}}</span>'

    >>> template = Template('<span>{{interpolation|angular}}</span>')
    >>> template.render(interpolation='angular.other.value')
    '<span>{{angular.other.value}}</span>'


