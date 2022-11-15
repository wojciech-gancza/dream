#-------------------------------------------------------------------------
# DREAM (C) WGan 2020
#-------------------------------------------------------------------------

""" Command line input/output - output goes directly to screen, reading
    keyboard commands and test classes used to mock them in tests """

from errors  import error

#-------------------------------------------------------------------------

class console(object):

    """ Console input/output adapter """

    def write(self, text):
        print(text)
        
    def read(self):
        try:
            return raw_input("??? > ")
        except:
            return input("??? > ")
     
#-------------------------------------------------------------------------

