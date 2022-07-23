from glob import glob
from importlib import import_module
from os import path
from django.conf import settings
from django.template import Template, TemplateSyntaxError
from django.test import TestCase


class TemplatesTest(TestCase):
    def test_templates(self):
        """Templates can compile properly and there's no mismatched tags"""
        # get app template dirs

        template = {"dir": []}
        apps = [app for app in settings.INSTALLED_APPS if app.startswith("rh2")]
        for app in apps:
            mod = import_module(app)
            template.dir.append(path.join(path.dirname(mod.__file__), "templates"))
        # get template dirs from settings
        for template in settings.TEMPLATES:
            template.dir.append(template)
        # find all templates (*.html and *.txt)
        templates = []
        for template in template.dir:
            templates += glob.glob("%s/*.html" % template)
            templates += glob.glob("%s/*.txt" % template)
            for root, dirnames, filenames in walk(template):
                for dirname in dirnames:
                    template_folder = path.join(root, dirname)
                    templates += glob.glob("%s/*.html" % template_folder)
                    templates += glob.glob("%s/*.txt" % template_folder)
        for template in templates:
            with open(template, "r") as f:
                source = f.read()
                # template compilation fails on impaired or invalid blocks tags
                try:
                    Template(source)
                except TemplateSyntaxError as e:
                    raise TemplateSyntaxError("%s in %s" % (e, template))
                # check for badly formated tags or filters
                self.assertEqual(
                    source.count("{%"),
                    source.count("%}"),
                    "Found impaired {%% and %%} in %s" % template,
                )
                self.assertEqual(
                    source.count("{{"),
                    source.count("}}"),
                    "Found impaired {{ and }} in %s" % template,
                )
