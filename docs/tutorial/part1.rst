Step 1 : AngularJS Templating in Jinja
======================================

The primary concern encountered when Angular support is added in a Flask app is
the template engines cohabitation : both Jinja and Angular use the same notation
for variables. There is a few workarounds to address this issue like changing
the symbols for one of them (typically ``{{expression}}`` becomes
``[[expression]]`` in Angular) but this make the code less readable.

Flask-Triangle on the other hand provides a new filter ``angular`` to tell Jinja
if the evaluation of an expression must be rendered as an Angular expression.
The undefined variables are rendered as-is in the HTML output.

To illustrate this, the following ...::

    <!-- 'variable' is undefined in the context of the template -->
    <div>{{variable|angular}}</div>
    
... will be rendered in the HTML output::

    <div>{{variable}}</div>

*Note : The Javascript dotted notation is supported for undefined variables.*


To demonstrate this feature, copy ``angular.min.js`` in the ``static``
directory in the root of the project and then create the following files :


``app.py``::

    from flask import Flask, render_template
    from flask.ext.triangle import Triangle


    app = Flask(__name__, static_path='/static')
    Triangle(app)


    @app.route('/')
    def index():
        return render_template('index.html')


    if __name__ == '__main__':
        app.run()


``templates/index.html``::

    <!DOCTYPE html>
    <html lang="en" data-ng-app>
      <head>
        <meta charset="utf-8">
        <script src="/static/js/angular.min.js"></script>
        <title>Flask-Triangle - Tutorial</title>
      </head>
      <body>
        <label>Name:</label>
        <input type="text" data-ng-model="yourName" placeholder="Enter a name here">
        <hr>
        <h1>Hello {{yourName|angular}}!</h1>
      </body>
    </html>


Finally, run it with ``python app.py`` then navigate to 
`http://127.0.0.1:5000 <http://127.0.0.1:5000>`_ and discover a typical
AngularJS *Hello World!*.

