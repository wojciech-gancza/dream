#-------------------------------------------------------------------------
# DREAM (C) WGan 2020
#-------------------------------------------------------------------------

""" Commonly used tools allowing various manipulations with data. 
    All morfing and translating function should be placed here. Also 
    some major adapters to language may be placed here when needed """
    
#-------------------------------------------------------------------------

class translator(object):

    """ class containing static functions translating between variour types 
        and contexts. """
        
    @classmethod
    def make_identifier(class_object, text):
        return text.replace(" ", "_").replace("\t", "_").replace("\n", "_").replace("\r", "_")
        
    @classmethod
    def make_nonempty_string(class_object, text):
        if text == "":
            return "-nothing-"
        else:
            return text
     
#-------------------------------------------------------------------------
