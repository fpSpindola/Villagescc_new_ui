from decimal import Decimal as D
from datetime import datetime

from ripple.tests import BasicTest

class BasicAccountTest(BasicTest):
    def test_display(self):
        unicode(self.account)
        unicode(self.node1_creditline)
    

