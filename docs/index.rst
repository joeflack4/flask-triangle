Flask-Triangle
==============


Flask-Triangle is a flask extension to easily design reusable forms for your
web application. It features a wide variety of inputs and many validators to
control data submitted by your users. It's aimed to be used in an AngularJS
environment. If you want more traditional forms, take a look to Flask-WTF_.

The main goal of Flask-Triangle is to provide you with an easy way to achieve
server-side validation to avoid hazardous or dirty data and client-side
validation with Angular to offer great user experience.

This document is an introduction.

.. _Flask-WTF: https://pythonhosted.org/Flask-WTF/


Installation
------------

Install the extension with the following command ::

    $ pip install git+https://github.com/morgan-del/flask-triangle.git

Please note that Flask-Triangle requires the following python libraries :

    * flask
    * jsonschema


Creating forms
--------------

Flask-Triangle provides you with a full collection of HTML widgets and
validators. For example ::

    from flask.ext.triangle import Form
    from flask.ext.triangle.widgets import TextInput
    from flask.ext.triangle.validators import Required

    class MyForm(Form):
        entry = TextInput(u'entry', validators=[Required()])

    form = MyForm(u'demo')

You can print this in your template by passing a MyForm instance to the 
template. This example demonstrate how to render such an instance ::

    <form name={{form.name}}>
      <div class="control-group" ng-class="{error: {{form.name}}.{{form.entry.name}}.$invalid}">
        <label>{{form.entry.label}}</label> {{ form.entry() }}
      </div>
    </form>

This example also embed Angular's client-side validation.


Server-side validation
----------------------

Because the form is transmitted to the server as a JSON objects (thanks to
AngularJS), the server-side validation process is based on json-schema
validation.

Each form has its own json-schema, generated from embed widgets and validators
which can be used for validation. To take advantage of it, each form provides a
class method acting as a function decorator for routed functions ::

    @route('/', methods=['POST'])
    @form.validate()
    def hello():
        return u'Sent data are valid !'

If sent data aren't valid, the server will answer an HTTP 4xx error depending
of the detected error.
