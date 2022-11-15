#-------------------------------------------------------------------------
# DREAM (C) WGan 2020
#-------------------------------------------------------------------------

""" Definition of error classes used as exceptions. Currently just
    one error can be raised: error containing only text. This is because
    program is just a proof of concept. Programmine errors and
    logic errors do not need to be distinguished """

import              unittest

from errors  import error, \
                    break_action

#-------------------------------------------------------------------------

class Test_error(unittest.TestCase):

    def test_of_raising_error(self):
        try:
            raise error("This is error text")
        except error as err:
            self.assertEqual(str(err), "ERROR: This is error text")

#-------------------------------------------------------------------------

class Test_break_action(unittest.TestCase):

    def test_of_breaking_action_exception(self):
        try:
            raise break_action
        except break_action as err:
            self.assertEqual(str(err), "BREAK: execution of command was broken.")

#-------------------------------------------------------------------------
