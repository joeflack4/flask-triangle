Step 3 : Building a Basic Form and Make It Work !
=================================================

*The main feature of Flask-Triangle is to define forms to be used in the HTML
templates and to validate data received by the server. This step will show
how-to build a basic form asking for profile informations and tell the user if
sent informations are valid or not.*


The profile
-----------

The profile form ask for a *first name*, a *last name*, a *birth date* and a
little *bio* about the user. The *bio* is the only optional field. Let's
complete the existing ``app.py`` to add the desired form and serve it at
`http://127.0.0.1:5000/profile <http://127.0.0.1:5000/profile>`_.

``app.py``::

    ...
    from flask.ext.triangle import Triangle, Form
    from flask.ext.triangle.widgets.standard import TextInput


    class Profile(Form):

        fname = TextInput('profile.fname', label='First Name', required=True)
        lname = TextInput('profile.lname', label='Last Name', required=True)
        bdate = TextInput('profile.bdate', label='Birthdate', required=True)
        bio = TextInput('profile.bio', label='Bio')


    app = Flask(__name__, static_path='/static')
    ...

    @app.route('/profile')
    def profile():
        return render_template('profile.html', form=Profile())


    if __name__ == '__main__':
        ...


The template will use ``form`` to generate the HTML code.

``templates/profile.html``::

    <!DOCTYPE html>
    <html lang="en" data-ng-app>

      <head>
        <meta charset="utf-8">
        <script src="/static/js/angular.min.js"></script>
        <script src="/static/js/app.js"></script>
        <title>Flask-Triangle - Tutorial</title>
      </head>

      <body data-ng-controller='TutoCtrl'>
        <form name="pForm">

          {% for field in form %}
            <label>{{field.label}}</label> {{field}} <br>
          {% endfor %}

          <button data-ng-click="send()" data-ng-disabled="pForm.$invalid">
            SEND
          </button>

        </form>
      </body>

    </html>


The HTML document requires a true AngularJS controller to be available in the
file ``/static/js/app.js``. The controller provides a ``send()`` method called
whenever the user click on the button to send entered data back to the server
with a ``POST`` method to ``/profile``.

``statis/js/app.js``::

    function TutoCtrl($scope, $http) {

        $scope.send = function() {
            $http.post('/profile', $scope.profile)
                 .success(function(){alert('ok')})
                 .error(function(){alert('fail')});
        }

    }


The last thing to do is to add the ability to receive ``POST`` requests on
``/profile`` and handle server-side validation.


``app.py``::

    ...
    from flask import Flask, render_template, request, abort
    ...

    ...
    @app.route('/profile', methods=['GET', 'POST'])
    def profile():

        form = Profile(vroot='profile')     # only the content of profile is
                                            # sent. We use a virtual root to
                                            # shift the schema.

        if request.method == 'POST':
            if form.validate(request.json): # validate the received data
                return 'ok !'
            else:
                abort(400)
        else:
            return render_template('profile.html', form=form)


    if __name__ == '__main__':
        ...

Test it
-------

Go to `http://127.0.0.1:5000/profile <http://127.0.0.1:5000/profile>`_ and fill
the form with valid data then click "SEND" : an alert box with the message
``ok`` should appear.

Because the validation is available on the client-side with the help of
AngularJS, you are not able to send invalid data. To do so, you can delete
``data-ng-disabled="pForm.$invalid"`` from the ``button`` tag or do an invalid
request with ``curl``::

    curl -v -X POST -H "Content-Type: application/json" -d '{"foo": "bar"}' http://127.0.0.1:5000/profile

The server should answer an HTTP error 400.

