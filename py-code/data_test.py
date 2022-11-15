#-------------------------------------------------------------------------
# DREAM (C) WGan 2020
#-------------------------------------------------------------------------

""" Main data structures of RPG environment. """

import                  unittest

from data        import description, \
                        name, \
                        property, \
                        properties, \
                        actions, \
                        item, \
                        location, \
                        realm
from tools       import translator
from compiler    import command, \
                        exit_node, \
                        command_name, \
                        print_text_node
from tools_test  import _game_mock

#-------------------------------------------------------------------------

class Test_description(unittest.TestCase):
    
    def test_of_empty_description(self):
        descr = description()
        self.assertEqual(descr.get_short_text(), "-nothing-")
        self.assertEqual(descr.get_long_text(), "-nothing-")

    def test_of_empty_assing(self):
        descr = description()
        descr.set_description("", "b");
        self.assertEqual(descr.get_short_text(), "-nothing-")
        self.assertEqual(descr.get_long_text(), "b")
        descr.set_description("a", "");
        self.assertEqual(descr.get_short_text(), "a")
        self.assertEqual(descr.get_long_text(), "-nothing-")

    def test_of_setting_value(self):
        descr = description()
        descr.set_description("short", "much much longer, however still short")
        self.assertEqual(descr.get_short_text(), "short")
        self.assertEqual(descr.get_long_text(), "much much longer, however still short")

    def test_of_casting_to_string(self):
        descr = description()
        descr.set_description("short", "much much longer, however still short")
        self.assertEqual(str(descr), "[description]\nshort\nmuch much longer, however still short\n")

#-------------------------------------------------------------------------

class Test_name(unittest.TestCase):

    def test_of_empty_nameset(self):
        empty_name = name()
        self.assertEqual(str(empty_name), "[name]\n-nothing-\n")
        
    def test_of_seting_names(self):
        just_name = name()
        just_name.set_names(["just name"])
        self.assertEqual(str(just_name), "[name]\njust name\n")
        just_name.set_names(["name1", "name2", "name3"])
        self.assertEqual(str(just_name), "[name]\nname1\nname2\nname3\n")
        self.assertEqual(just_name.get_name(), "name1")
        just_name.set_names([])
        self.assertEqual(str(just_name), "[name]\n-nothing-\n")
        self.assertEqual(just_name.get_name(), "-nothing-")

#-------------------------------------------------------------------------

class Test_property(unittest.TestCase):

    def test_of_empty_value(self):
        prop = property()
        self.assertEqual(prop.get(), property.DEFAULT_VALUE)
        
    def test_of_cumulating_values(self):
        prop = property()
        prop.add(123)
        prop.add(43)
        self.assertEqual(prop.get(), 166)
        
    def test_of_upper_limit(self):
        prop = property()
        prop.add(8000)
        prop.add(8000)
        self.assertEqual(prop.get(), property.MAXIMAL_VALUE)
        
    def test_of_lower_limit(self):
        prop = property()
        prop.add(1000)
        prop.add(-8000)
        self.assertEqual(prop.get(), property.MINIMAL_VALUE)
 
    def test_of_casting_to_string(self):
        prop = property()
        prop.add(1234)
        self.assertEqual(str(prop), "1234")
 
#-------------------------------------------------------------------------
        
class Test_properties(unittest.TestCase):
    
    def test_of_empty_value(self):
        props = properties()
        self.assertEqual(props.get("Mana"), property.DEFAULT_VALUE)
        
    def test_of_many_values(self):
        props = properties()
        props.add("Health", 123)
        props.add("Health", 43)
        props.add("x", 8000)
        props.add("x", 8000)
        props.add("y", 1000)
        props.add("y", -8000)
        props.add("Mana", 1234)
        self.assertEqual(props.get("x"), property.MAXIMAL_VALUE)
        self.assertEqual(props.get("Health"), 166)
        self.assertEqual(props.get("y"), property.MINIMAL_VALUE)
        self.assertEqual(props.get("Mana"), 1234)
        
    def test_of_casting_to_string(self):
        props = properties()
        props.add("Health", 123)
        props.add("x", 8000)
        props.add("y", 1000)
        props.add("Mana", 1234)
        self.assertEqual(str(props), "[properties]\ny = 1000\nx = 8000\nHealth = 123\nMana = 1234\n")

#-------------------------------------------------------------------------

class Test_actions(unittest.TestCase):

    def test_serialization_of_empty_actions(self):
        act = actions()
        self.assertEqual(str(act), "[actions]\n")
        
    def test_serialization_of_filled_actions(self):
        act = actions()
        act.add_action(command(command_name(["Hello"]), [exit_node()]))
        act.add_action(command(command_name(["Bye"]), [exit_node()]))
        self.assertEqual(str(act), "[actions]\nHello THEN EXIT\nBye THEN EXIT\n")
        
    def test_execution_of_filled_actions(self):
        act = actions()
        game = _game_mock()
        act.add_action(command(command_name(["Hello"]), [exit_node()]))
        act.add_action(command(command_name(["Bye"]), [exit_node()]))
        self.assertEqual(str(act), "[actions]\nHello THEN EXIT\nBye THEN EXIT\n")
        self.assertTrue( act.try_execute("Hello", game) )
        self.assertFalse( act.try_execute("Hail", game) )
        self.assertTrue( act.try_execute("Bye", game) )
        self.assertEqual( game.log, "Stop was called\nStop was called\n" )
        
#-------------------------------------------------------------------------

class Test_item(unittest.TestCase):

    def test_of_serialization_of_empty_item(self):
        it = item()
        self.assertEqual(str(it), "[type]\nlocation\n\n[name]\n-nothing-\n\n[properties]\n\n[description]\n-nothing-\n-nothing-\n")
        
    def test_of_filled_item(self):
        it = item()
        it._name.set_names(["a", "b", "c"])
        it._properties.add("x", 12)
        self.assertEqual(str(it), "[type]\nlocation\n\n[name]\na\nb\nc\n\n[properties]\nx = 12\n\n[description]\n-nothing-\n-nothing-\n")
      
#-------------------------------------------------------------------------

class Test_location(unittest.TestCase):

    def test_of_serialization_of_empty_object(self):
        obj = location()
        self.assertEqual(str(obj), "[type]\nlocation\n\n[name]\n-nothing-\n\n[properties]\n\n[description]\n-nothing-\n-nothing-\n\n[actions]\n")
        
    def test_of_filled_element_1(self):
        obj = location()
        obj._name.set_names(["abc", "xyz"])
        self.assertEqual(str(obj), "[type]\nlocation\n\n[name]\nabc\nxyz\n\n[properties]\n\n[description]\n-nothing-\n-nothing-\n\n[actions]\n")
        
    def test_of_filled_element_2(self):
        obj = location()
        obj._actions._actions.append(command(command_name(["abc"]), [exit_node()]))
        self.assertEqual(str(obj), "[type]\nlocation\n\n[name]\n-nothing-\n\n[properties]\n\n[description]\n-nothing-\n-nothing-\n\n[actions]\nabc THEN EXIT\n")
        
    def test_of_execution_command(self):
        obj = location()
        obj._actions._actions.append(command(command_name(["abc"]), [print_text_node("1.")]))
        obj._realm = realm()
        obj._realm._actions._actions.append(command(command_name(["abc"]), [print_text_node("abc")]))
        obj._realm._actions._actions.append(command(command_name(["xyz"]), [print_text_node("xyz")]))
        game = _game_mock()
        self.assertTrue(obj.try_execute("abc", game))
        self.assertFalse(obj.try_execute("Afr", game))
        self.assertTrue(obj.try_execute("xyz", game))
        self.assertEqual(game._console.get_output(), "1.\nxyz\n")
       
#-------------------------------------------------------------------------

class Test_realm(unittest.TestCase):

    def test_of_serialization_of_empty_object(self):
        obj = realm()
        self.assertEqual(str(obj), "[type]\nrealm\n\n[name]\n-nothing-\n\n[actions]\n")
        
    def test_of_filled_element_1(self):
        obj = realm()
        obj._name.set_names(["abc"])
        obj._actions._actions.append(command(command_name(["abc"]), [exit_node()]))
        self.assertEqual(str(obj), "[type]\nrealm\n\n[name]\nabc\n\n[actions]\nabc THEN EXIT\n")

#-------------------------------------------------------------------------
       

