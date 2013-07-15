# -*- encoding: utf-8 -*-
"""
    flask_triangle.template
    -----------------------

    :copyright: (c) 2013 by Morgan Delahaye-Prat.
    :license: BSD, see LICENSE for more details.
"""


from __future__ import absolute_import
from __future__ import unicode_literals


form_template = """
<form name={{form.name}}>
  {% for field in form %}
  <div class="control-group" ng-class="{error: {{form.name}}.{{field.name}}.$invalid}">
    <label class="control-label"{% if field.id %} for="{{field.id}}"{% endif %}>{{field.label.format(**kwargs).capitalize()}}</label>
    <div class="controls">
      {{field(**kwargs)}}
      {% if field.description %}
      <span class="help-inline">
        <a>
          <i tooltip="{{field.description.format(**kwargs)}}" class="icon-question-sign"></i>
        </a>
      </span>
      {% endif %}
    </div>
  </div>
  {% endfor %}
</form>
"""
