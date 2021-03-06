import json

from django import forms
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe


class JSONEditorWidget(forms.Widget):
    template_name = "django_admin_json_editor/editor.html"

    def __init__(
        self,
        schema,
        collapsed=True,
        sceditor=False,
        editor_options=None,
        obj=None,
        inline=False,
    ):
        super(JSONEditorWidget, self).__init__()
        self._schema = schema
        self._collapsed = collapsed
        self._sceditor = sceditor
        self._obj = obj
        self._editor_options = {
            "theme": "bootstrap4",
            "iconlib": "fontawesome4",
        }
        self._editor_options.update(editor_options or {})
        self.inline = inline

    def render(self, name, value, attrs=None, renderer=None):
        if self._obj is not None:
            obj = self._obj
        else:
            obj = self._obj
        if callable(self._schema):
            schema = self._schema(self, obj)
        else:
            schema = self._schema

        schema["title"] = " "
        schema["options"] = {"collapsed": int(self._collapsed)}

        editor_options = self._editor_options.copy()
        editor_options["schema"] = schema
        field_name = name.split("-")[-1]
        reference_name = "testcase"
        # print(name.replace(field_name, reference_name))
        context = {
            "name": name,
            "underscore_name": name.replace("-", "_"),
            "data": value,
            "field_name": field_name,
            "selector_name": "id_" + name.replace(field_name, reference_name),
            "editor_options": json.dumps(editor_options),
            "inline": self.inline,
        }
        return mark_safe(render_to_string(self.template_name, context))

    @property
    def media(self):
        css = {
            "all": [
                "django_admin_json_editor/fontawesome/css/font-awesome.min.css",
                "django_admin_json_editor/style.css",
            ]
        }
        js = [
            "django_admin_json_editor/jsoneditor/jsoneditor.min.js",
        ]

        if self._editor_options["theme"] == "bootstrap4":
            css["all"].append(
                "django_admin_json_editor/bootstrap/css/bootstrap.min.css"
            )
            js.append("django_admin_json_editor/jquery/jquery-3.5.1.min.js")
            js.append(
                "django_admin_json_editor/bootstrap/js/bootstrap.bundle.min.js"
            )

        if self._sceditor:
            css["all"].append(
                "django_admin_json_editor/sceditor/themes/default.min.css"
            )
            js.append(
                "django_admin_json_editor/sceditor/jquery.sceditor.bbcode.min.js"
            )
        return forms.Media(css=css, js=js)
