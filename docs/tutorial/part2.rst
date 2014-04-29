Step 2 : Mixing Templates
=========================

This second step will show how to use a variable from the server context and
make it available in AngularJS by mixing both template engines. 

To begin, modify ``app.py`` to accept an URL segment as a variable and forward
it to the template :

``app.py``::

    @app.route('/')
    @app.route('/<default>')
    def index(default=''):
        return render_template('index.html', default=default)

This way, both `http://127.0.0.1:5000 <http://127.0.0.1:5000>`_ and
`http://127.0.0.1:5000/foo <http://127.0.0.1:5000/foo>`_ are working and ``foo``
is available from the template in the variable named ``default``.

Now modify ``templates/index.html`` to use the value of ``default`` to initialize
``yourName``.

``templates/index.html``::

    <!DOCTYPE html>
    <html lang="en" data-ng-app>
      <head>
        <meta charset="utf-8">
        <script src="/static/js/angular.min.js"></script>
        <title>Flask-Triangle - Tutorial</title>
      </head>
      <body ng-init="yourName='{{default}}';">
        <label>Name:</label>
        <input type="text" data-ng-model="yourName" placeholder="Enter a name here">
        <hr>
        <h1>Hello {{yourName|angular}}!</h1>
      </body>
    </html>

As you can see, the default value of yourName is set by Angular with the help
of the ``ng-init`` directive. The trick is that default is already rendered in
the HTML so Angular sees ``ng-init="yourName='value'"``.

If you navigate to `http://127.0.0.1:5000/World <http://127.0.0.1:5000/World>`_,
the input field will be set to ``World`` by default and the page will display
a classic ``Hello World !``.
