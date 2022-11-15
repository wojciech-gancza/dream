#-------------------------------------------------------------------------
# DREAM (C) WGan 2020
#-------------------------------------------------------------------------

""" Commonly used tools allowing various manipulations with data. 
    All morfing and translating function should be placed here. Also 
    some major adapters to language may be placed here when needed """
    
import                  unittest

from tools       import translator
from data        import location, \
                        items
from errors      import error
from builder     import object_factory, \
                        factory_realm_cache, \
                        factory_location_cache

#-------------------------------------------------------------------------

class testing_console(object):

    """ Console adapter to be used in tests - writes store result into 
        string which can be checked after processing. Instead of input
        this fake terminal reads from list """
        
    def __init__(self, input):
        self._buffer = ""
        if not type(input) is list:
            raise error("Testing console must be feed by array of commands")
        self._input = input
        self._input_pos = 0
        
    def write(self, text):
        self._buffer = self._buffer + text + "\n"
        
    def get_output(self):
        return self._buffer
        
    def read(self):
        if self._input_pos >= len(self._input):
            return None
        else:
            line = self._input[self._input_pos]
            self._input_pos = self._input_pos + 1
            return line
    
#-------------------------------------------------------------------------

class _game_mock:
    
    """ For test use only. Class mocking game allowing testing how 
        game services are used """
    
    def __init__(self, inputs = []):
        self.log = ""
        self._console = testing_console(inputs)
        self._location = location()
        self._location._description.set_description("loc.", "long description of location")
        self._factory = factory_location_cache(3, factory_realm_cache(object_factory("../dream/tests")))
        self._pocket = items()
        self._pocket.put_item( self._factory.get_object("lockpick made from wire") )
        self._pocket.put_item( self._factory.get_object("unisolated wire") )
        
    def execute(self, command_text):
        if self._pocket.try_execute(command_text, self):
            return True
        if self._location.try_execute(command_text, self):
            return True
        return False      

    def stop(self):
        self.log = self.log + "Stop was called\n"
  
#-------------------------------------------------------------------------

class Test_testing_console(unittest.TestCase):
    
    def test_of_initialisation_error(self):
        try:
            io = testing_console("just text")
            self.assertTrue(False)
        except error as err:
            self.assertEqual(str(err), "ERROR: Testing console must be feed by array of commands")
    
    def test_of_reading_subsequent_lines(self):
        io = testing_console(["first", "second line", "last"])
        self.assertEqual(io.read(), "first")
        self.assertEqual(io.read(), "second line")
        self.assertEqual(io.read(), "last")
        self.assertEqual(io.read(), None)
        self.assertEqual(io.read(), None)
    
    def test_of_preparing_output(self):
        io = testing_console([])
        io.write("first")
        io.write("second")
        io.write("last")
        self.assertEqual(io.get_output(), "first\nsecond\nlast\n")

#-------------------------------------------------------------------------
     
class Test_translator(unittest.TestCase):
    
    def test_of_making_identifier(self):
        self.assertEqual(translator.make_identifier("abc"), "abc")
        self.assertEqual(translator.make_identifier("a b c"), "a_b_c")
        self.assertEqual(translator.make_identifier("\ra\tb\nc"), "_a_b_c")
        
    def test_of_making_nonempty_string(self):
        self.assertEqual(translator.make_nonempty_string("abc"), "abc")
        self.assertEqual(translator.make_nonempty_string(""), "-nothing-")
      
#-------------------------------------------------------------------------
