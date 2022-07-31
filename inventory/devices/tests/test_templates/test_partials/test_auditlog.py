import copy

from django.test import SimpleTestCase
from django.template import Context, Template


default_template = Template("{% include  'devices/partials/device_auditlog.html'%}")


class DeviceAssignmentAuditlogTest(SimpleTestCase):
    def setUp(self):
        self.context = Context({})
        self.template = copy.deepcopy(default_template)
