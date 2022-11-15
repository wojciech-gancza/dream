#-------------------------------------------------------------------------
# DREAM (C) WGan 2020
#-------------------------------------------------------------------------

""" Definition of error classes used as exceptions. Currently just
    one error can be raised: error containing only text. This is because
    program is just a proof of concept. Programmine errors and
    logic errors do not need to be distinguished """

#-------------------------------------------------------------------------

class error(Exception):

    """ error contain just error text message - nothing more is
        currently needed """

    def __init__(self, text):
        self._text = text

    def __str__(self):
        return "ERROR: " + self._text

#-------------------------------------------------------------------------

class break_action(Exception):

    """ error raised when problems with action execution was found """

    def __str__(self):
        return "BREAK: execution of command was broken."

#-------------------------------------------------------------------------
