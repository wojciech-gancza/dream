#-------------------------------------------------------------------------
# DREAM (C) WGan 2020
#-------------------------------------------------------------------------

""" Builder provides construction of objects from files definition """

import                unittest

from errors    import error
from tools     import translator
from data      import location, \
                      name, \
                      description, \
                      properties, \
                      actions, \
                      item, \
                      realm
from builder   import file_data_source, \
                      array_tokenizer, \
                      buffered_token_source, \
                      data_reader, \
                      object_builder, \
                      object_factory
from compiler  import compiler

#-------------------------------------------------------------------------

class Test_file_data_source(unittest.TestCase):

    def test_of_reading_file(self):
        source = file_data_source("test-dream")
        content = source.get_data_set("dark cave")
        self.assertEqual(content[0], "[type]\n")

#-------------------------------------------------------------------------

class Test_array_tokenizer(unittest.TestCase):
    
    def test_of_tokenization_of_empty_array(self):
        tokens = array_tokenizer([])
        token = tokens.get_token()
        self.assertEqual(token, None)
        
    def test_of_reading_various_tokens(self):
        tokens = array_tokenizer(["[token]", "not token"])
        token = tokens.get_token()
        self.assertTrue(token[0])
        self.assertEqual(token[1], "token")
        token = tokens.get_token()
        self.assertFalse(token[0])
        self.assertEqual(token[1], "not token")
        token = tokens.get_token()
        self.assertEqual(token, None)
        
    def test_of_skiping_empty_lines(self):
        tokens = array_tokenizer([" ", "not token", "", "\n\r\t", "last", ""])
        token = tokens.get_token()
        self.assertFalse(token[0])
        self.assertEqual(token[1], "not token")
        token = tokens.get_token()
        self.assertFalse(token[0])
        self.assertEqual(token[1], "last")
        token = tokens.get_token()
        self.assertEqual(token, None)
        
#-------------------------------------------------------------------------

class Test_buffered_token_source(unittest.TestCase):

    def test_of_prerequisite(self):
        tokens = buffered_token_source(array_tokenizer([" ", "not token", "", "\n\r\t", "last", ""]))
        token = tokens.get_token()
        self.assertFalse(token[0])
        self.assertEqual(token[1], "not token")
        token = tokens.get_token()
        self.assertFalse(token[0])
        self.assertEqual(token[1], "last")
        token = tokens.get_token()
        self.assertEqual(token, None)
       
    def test_of_pushing_back(self):
        tokens = buffered_token_source(array_tokenizer([" ", "not token", "", "\n\r\t", "last", ""]))
        token = tokens.get_token()
        self.assertFalse(token[0])
        self.assertEqual(token[1], "not token")
        token = tokens.get_token()
        self.assertFalse(token[0])
        self.assertEqual(token[1], "last")
        tokens.revert_laset_token()
        token = tokens.get_token()
        self.assertFalse(token[0])
        self.assertEqual(token[1], "last")
    
    def test_of_pushing_back_error(self):
        tokens = buffered_token_source(array_tokenizer([" ", "not token", "", "\n\r\t", "last", ""]))
        try:
            tokens.revert_laset_token()
            self.assertTrue(False)
        except error as err:
            self.assertEqual(str(err), "ERROR: Cannot rollback when data was not read")
    
    def test_of_twice_pushing_back_error(self):
        tokens = buffered_token_source(array_tokenizer([" ", "not token", "", "\n\r\t", "last", ""]))
        token = tokens.get_token()
        tokens.revert_laset_token()
        try:
            tokens.revert_laset_token()
            self.assertTrue(False)
        except error as err:
            self.assertEqual(str(err), "ERROR: Cannot rollback when data was not read")
    
#-------------------------------------------------------------------------

class Test_data_reader(unittest.TestCase):
    
    def test_of_reading_token(self):
        tokens = data_reader(array_tokenizer(["[token]", "not token"]))
        token = tokens.get_token("token")
        self.assertEqual(token, "token")
        try:
            token = tokens.get_token("token")
            self.assertTrue(False)
        except error as err:
            self.assertEqual(str(err), "ERROR: Expects token but found data 'not token'")
            
    def test_of_not_reading_token(self):
        tokens = data_reader(array_tokenizer( [] ))
        try:
            token = tokens.get_token("token")
            self.assertTrue(False)
        except error as err:
            self.assertEqual(str(err), "ERROR: Expects token but found end of data")
        
    def test_of_reading_token_or_eof(self):
        tokens = data_reader(array_tokenizer(["[token]", "not token"]))
        token = tokens.get_token_or_eof("token")
        self.assertEqual(token, "token")
        try:
            token = tokens.get_token_or_eof("token")
            self.assertTrue(False)
        except error as err:
            self.assertEqual(str(err), "ERROR: Expects token but found data 'not token'")
        token = tokens.get_token_or_eof("token")
        self.assertEqual(token, None)
            
    def test_of_not_reading_token(self):
        tokens = data_reader(array_tokenizer( [] ))
        try:
            token = tokens.get_token("token")
            self.assertTrue(False)
        except error as err:
            self.assertEqual(str(err), "ERROR: Expects token but found end of data")
        
    def test_of_reading_data(self):
        tokens = data_reader(array_tokenizer(["not token", "[token]"]))
        data = tokens.get_data("data")
        self.assertEqual(data, "not token")
        try:
            token = tokens.get_data("data")
            self.assertTrue(False)
        except error as err:
            self.assertEqual(str(err), "ERROR: Expects data but found token '[token]'")
            
    def test_of_not_reading_data(self):
        tokens = data_reader(array_tokenizer( [] ))
        try:
            data = tokens.get_data("data")
            self.assertTrue(False)
        except error as err:
            self.assertEqual(str(err), "ERROR: Expects data but found end of data")
    
    def test_of_trying_get_data(self):
        tokens = data_reader(buffered_token_source(array_tokenizer( ["data1", "data2", "[token]"] )))
        self.assertEqual( tokens.try_get_data(), "data1" )
        self.assertEqual( tokens.try_get_data(), "data2" )
        self.assertEqual( tokens.try_get_data(), None )
        self.assertEqual( tokens.try_get_data(), None )
        self.assertEqual( tokens.get_token("token"), "token" )
        self.assertEqual( tokens.try_get_data(), None )

#-------------------------------------------------------------------------

class Test_object_builder(unittest.TestCase):
    
    def test_of_building_description(self):
        data_source = data_reader(buffered_token_source(array_tokenizer( \
            ["short", "long"] )))
        description = object_builder._create_description(data_source)
        self.assertEqual(str(description), "[description]\nshort\nlong\n")
        
    def test_of_failing_building_description_1(self):
        data_source = data_reader(buffered_token_source(array_tokenizer( \
            [] )))
        try:
            description = object_builder._create_description(data_source)
            self.assertTrue(False)
        except error as err:
            self.assertEqual(str(err), "ERROR: Expects short description but found end of data")
        
    def test_of_failing_building_description_2(self):
        data_source = data_reader(buffered_token_source(array_tokenizer( \
            ["short"] )))
        try:
            description = object_builder._create_description(data_source)
            self.assertTrue(False)
        except error as err:
            self.assertEqual(str(err), "ERROR: Expects long description but found end of data")

    def test_of_failing_building_description_3(self):
        data_source = data_reader(buffered_token_source(array_tokenizer( \
            ["[A]"] )))
        try:
            description = object_builder._create_description(data_source)
            self.assertTrue(False)
        except error as err:
            self.assertEqual(str(err), "ERROR: Expects short description but found token '[A]'")
        
    def test_of_failing_building_description_4(self):
        data_source = data_reader(buffered_token_source(array_tokenizer( \
            ["short", "[B]"] )))
        try:
            description = object_builder._create_description(data_source)
            self.assertTrue(False)
        except error as err:
            self.assertEqual(str(err), "ERROR: Expects long description but found token '[B]'")

    def test_of_creation_name(self):
        data_source = data_reader(buffered_token_source(array_tokenizer( \
            ["name1", "name2", "name3"] )))
        name = object_builder._create_name(data_source)
        self.assertEqual(str(name), "[name]\nname1\nname2\nname3\n")
        
    def test_of_ending_read_at_token(self):
        data_source = data_reader(buffered_token_source(array_tokenizer( \
            ["name1", "name2", "", "[next]", "name3"] )))
        name = object_builder._create_name(data_source)
        self.assertEqual(str(name), "[name]\nname1\nname2\n")
        
    def test_of_creation_empty_namestet(self):
        data_source = data_reader(buffered_token_source(array_tokenizer( \
            ["[next]", "name3"] )))
        name = object_builder._create_name(data_source)
        self.assertEqual(str(name), "[name]\n-nothing-\n")
        
    def test_of_creation_empty_propert_set(self):
        data_source = data_reader(buffered_token_source(array_tokenizer( \
            ["[next]", "name3"] )))
        props = object_builder._create_properties(data_source)
        self.assertEqual(str(props), "[properties]\n")
        
    def test_of_creation_filled_propert_set(self):
        data_source = data_reader(buffered_token_source(array_tokenizer( \
            ["a=234", "b=324", "c=331"] )))
        props = object_builder._create_properties(data_source)
        self.assertEqual(str(props), "[properties]\na = 234\nc = 331\nb = 324\n")
        
    def test_of_propert_set_with_wrong_definition_1(self):
        data_source = data_reader(buffered_token_source(array_tokenizer( \
            ["a", "b=324", "c=331"] )))
        try:
            props = object_builder._create_properties(data_source)
            self.assertTrue(False)
        except error as err:
            self.assertEqual(str(err), "ERROR: Wrong format of property definition. Should be 'name = value', but is 'a'")
        
    def test_of_propert_set_with_wrong_definition_2(self):
        data_source = data_reader(buffered_token_source(array_tokenizer( \
            ["a=324", "b=d=324", "c=331"] )))
        try:
            props = object_builder._create_properties(data_source)
            self.assertTrue(False)
        except error as err:
            self.assertEqual(str(err), "ERROR: Wrong format of property definition. Should be 'name = value', but is 'b=d=324'")
        
    def test_of_propert_set_with_wrong_definition_3(self):
        data_source = data_reader(buffered_token_source(array_tokenizer( \
            ["a=324", "b=d", "c=331"] )))
        try:
            props = object_builder._create_properties(data_source)
            self.assertTrue(False)
        except error as err:
            self.assertEqual(str(err), "ERROR: Value of property must be integer, but is 'd'")
        
    def test_of_getting_object(self):
        data_source = array_tokenizer( [\
            "[type]", \
            "location", \
            "[name]", \
            "dark cave", \
            "cave", \
            "[description]", \
            "Short piece of shiny wire", \
            "This is a piece of wire. It is about 20cm long and it looks like made of aluminium. It is preety hard to bend, but bendable in bare fingers." ] )
        item = object_builder.get_object(data_source)
        self.assertEqual(str(item), "[type]\nlocation\n\n[name]\ndark cave\ncave\n\n[properties]\n\n[description]\nShort piece of shiny wire\nThis is a piece of wire. It is about 20cm long and it looks like made of aluminium. It is preety hard to bend, but bendable in bare fingers.\n\n[actions]\n")
 
    def test_of_wrong_format_1(self):
        data_source = array_tokenizer( [\
            "type", \
            "item", \
            "[name]", \
            "wire" ] )
        try:
            item = object_builder.get_object(data_source)
            self.assertTrue(False)
        except error as err:
            self.assertEqual(str(err), "ERROR: Expects type but found data 'type'")
        
    def test_of_wrong_format_2(self):
        data_source = array_tokenizer( [] )
        try:
            item = object_builder.get_object(data_source)
            self.assertTrue(False)
        except error as err:
            self.assertEqual(str(err), "ERROR: Expects type but found end of data")
        
    def test_of_wrong_format_3(self):
        data_source = array_tokenizer( [\
            "[type]", \
            "[name]", \
            "wire" ] )
        try:
            item = object_builder.get_object(data_source)
            self.assertTrue(False)
        except error as err:
            self.assertEqual(str(err), "ERROR: Expects name of type but found token '[name]'")
        
    def test_of_wrong_format_4(self):
        data_source = array_tokenizer( [\
            "[type]", \
            "unknown object", \
            "wire" ] )
        try:
            item = object_builder.get_object(data_source)
            self.assertTrue(False)
        except error as err:
            self.assertEqual(str(err), "ERROR: Cannot create object of type 'unknown object'")
        
    def test_of_wrong_format_5(self):
        data_source = array_tokenizer( [\
            "[type]", \
            "location", \
            "[wire]", \
            "wire" ] )
        try:
            item = object_builder.get_object(data_source)
            self.assertTrue(False)
        except error as err:
            self.assertEqual(str(err), "ERROR: Unknows element type 'wire'")
        
    def test_of_create_actions(self):
        data_source = data_reader(buffered_token_source(array_tokenizer( [\
            "look THEN PRINT You see nothing.", 
            "touch THEN PRINT You feal wet stone"])))
        act = object_builder._create_actions(data_source)
        self.assertEqual(str(act), "[actions]\nlook THEN PRINT You see nothing.\ntouch THEN PRINT You feal wet stone\n")
        
    def test_of_method_creating_realm(self):
        data_source = data_reader(buffered_token_source(array_tokenizer( \
            ["reality"] )))
        factory = object_factory("test-dream") 
        rlm = object_builder._create_realm(data_source, factory)
        self.assertEqual(str(rlm), "[type]\nrealm\n\n[name]\nreality\n\n[actions]\nwake up; exit THEN PRINT You woke up from the dream.; EXIT\nlook THEN LOOK\n")

    def test_of_getting_realm(self):
        data_source = array_tokenizer( \
            ["[type]", "location", "[realm]", "reality"] )
        factory = object_factory("test-dream") 
        loc = object_builder.get_object(data_source, factory)
        self.assertEqual(str(loc._realm), "[type]\nrealm\n\n[name]\nreality\n\n[actions]\nwake up; exit THEN PRINT You woke up from the dream.; EXIT\nlook THEN LOOK\n")

#-------------------------------------------------------------------------
 
class Test_object_factory(unittest.TestCase):
    
    def test_of_creation_object_2(self):
        factory = object_factory("test-dream")
        obj = factory.get_object("dark cave")
        self.assertEqual(str(obj), "[type]\nlocation\n\n[name]\ndark cave\ncave\nunknown cave\n\n[realm]\nreality\n\n[properties]\nvolume = 1000\nlight = 5\n\n[description]\nThe cave is really dark\nYou see barly nothing. The cave is really dark. After a while you seem to see a shadows in the darkness but you cannot realize what it can be. You see no way out and no possiblility to move safely.\n\n[actions]\nlook THEN PRINT It is too dark to see anything. You should relay or other senses.\n")       

    def test_of_creation_object_1(self):
        factory = object_factory("test-dream")
        obj = factory.get_object("unisolated wire")
        self.assertEqual(str(obj), "[type]\nlocation\n\n[name]\nwire\nunisolated wire\naluminum wire\n\n[properties]\nresistance = 1\n\n[description]\nShort piece of shiny wire.\nThis is a piece of wire. It is about 20cm long and it looks like made of aluminium. It is preety hard to bend, but bendable in bare fingers.\n")
  
#-------------------------------------------------------------------------
 
