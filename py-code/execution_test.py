#-------------------------------------------------------------------------
# DREAM (C) WGan 2020
#-------------------------------------------------------------------------

""" Processor is a module which process and changes state of the game, by
    processing commands on given items """

import                  unittest
from errors      import error, \
                        break_action
from expression  import object_provider, \
                        object_parameter_provider, \
                        subject_parameter_provider, \
                        constant_provider, \
                        player_property_provider, \
                        new_object_provider, \
                        constant_value_expression, \
                        location_provider, \
                        player_provider, \
                        realm_provider
from execution   import exit_node, \
                        translating_text_node, \
                        print_text_node, \
                        look_around_node, \
                        change_location_node, \
                        inventory_node, \
                        take_item_node, \
                        drop_item_node, \
                        delete_item_node, \
                        execute_command_node, \
                        command_name, \
                        command, \
                        examine_node, \
                        become_node, \
                        modify_property_base, \
                        advance_property_node, \
                        set_property_node, \
                        set_trace_node, \
                        dump_node
from condition   import comparision_equal_condition
from compiler    import compiler
from data        import items, \
                        item
from tools_test  import _game_mock, \
                        testing_console
from builder     import object_factory
from game        import processor

#-------------------------------------------------------------------------

class Test_exit_node(unittest.TestCase):
    
    def test_of_exit_node(self):
        node = exit_node()
        game = _game_mock()
        node.run(game, "")
        self.assertEqual(game.log, "Stop was called\n")
        
    def test_of_exit_node_serialization(self):
        node = exit_node()
        self.assertEqual(str(node), "EXIT")
        
#-------------------------------------------------------------------------

class Test_translating_text_node(unittest.TestCase):

    def test_of_keeping_text(self):
        node = translating_text_node("Just a text")
        game = _game_mock()
        text = node._get_text(game, "bended wire")
        self.assertEqual(text, "Just a text")

    def test_of_translation_of_OBJECT(self):
        node = translating_text_node("The OBJECT is here")
        game = _game_mock()
        text = node._get_text(game, "bended wire")
        self.assertEqual(text, "The lockpick is here")

#-------------------------------------------------------------------------

class Test_print_text_node(unittest.TestCase):

    def test_of_serializing_node(self):
        node = print_text_node("This is a text")
        self.assertEqual(str(node), "PRINT This is a text")
        
    def test_of_execution(self):
        node = print_text_node("This is a text")
        game = _game_mock()
        node.run(game, "")
        self.assertEqual(game._console._buffer, "This is a text\n")
        
    def test_of_execution_with_current_item_name(self):
        node = print_text_node("This is OBJECT")
        game = _game_mock()
        node.run(game, "bended wire")
        self.assertEqual(game._console._buffer, "This is lockpick\n")

    def test_of_execution_with_non_selected_item(self):
        node = print_text_node("This is ITEM")
        game = _game_mock()
        try:
            node.run(game, "")
            self.assertTrue(False)
        except error as err:
            self.assertEqual(str(err), "ERROR: ITEM was not selected. It must be specified in condition.")
        except Exception:
            self.assertTrue(False)
        
    def test_of_execution_with_selected_item(self):
        node = print_text_node("This is ITEM")
        game = _game_mock()
        it = item()
        it._name._main_name = "gizmo"
        game._memo["ITEM"] = it
        node.run(game, "bended wire")
        self.assertEqual(game._console._buffer, "This is gizmo\n")

#-------------------------------------------------------------------------

class Test_look_around_node(unittest.TestCase):

    def test_of_serializing_node(self):
        node = look_around_node()
        self.assertEqual(str(node), "LOOK")
        
    def test_of_execution(self):
        node = look_around_node()
        game = _game_mock()
        node.run(game, "")
        self.assertEqual(game._console._buffer, "long description of location\n")
        
#-------------------------------------------------------------------------

class Test_change_location_node(unittest.TestCase):

    def test_of_serializing_node(self):
        node = change_location_node('somewhere')
        self.assertEqual(str(node), "GOTO somewhere")

    def test_of_execution(self):
        node = change_location_node("mansion hall")
        game = _game_mock()
        node.run(game, "")
        self.assertEqual(game._console._buffer, "You are in mansion hall\nYou see doors around however main door located on south looks not real.\n")
        
#-------------------------------------------------------------------------

class Test_inventory_node(unittest.TestCase):

    def test_of_serializing_node(self):
        node = inventory_node()
        self.assertEqual(str(node), "POCKET")

    def test_of_execution_with_filled_inventory(self):
        node = inventory_node()
        game = _game_mock()
        node.run(game, "")
        self.assertEqual(game._console._buffer, "You have:\n - Lockpick made of thin shiny wire.\n - Short piece of shiny wire.\n")
        
    def test_of_execution_with_empty_inventory(self):
        node = inventory_node()
        game = _game_mock()
        game._player._items = items()
        node.run(game, "")
        self.assertEqual(game._console._buffer, "You have nothing.\n")
        
#-------------------------------------------------------------------------

class Test_examine_node(unittest.TestCase):

    def test_of_serializing_node(self):
        node = examine_node(constant_provider("xyz"))
        self.assertEqual(str(node), "EXAMINE xyz")
    
    def test_of_examining_object(self):
        node = examine_node(constant_provider("unisolated wire"))
        game = _game_mock()
        node.run(game, "")
        self.assertEqual(game._console._buffer, 
            "This is a piece of wire. It is about 20cm long and it looks like " \
            "made of aluminium. It is preety hard to bend, but bendable in " \
            "bare fingers.\n")
        
    def test_of_examining_nonexisting_object(self):
        node = examine_node(constant_provider("wired unisolation"))
        game = _game_mock()
        node.run(game, "")
        self.assertEqual(game._console._buffer, "I see no wired unisolation\n")
    
#-------------------------------------------------------------------------

class Test_take_item_node(unittest.TestCase):

    def test_of_serializing_node(self):
        node = take_item_node(constant_provider("xyz"))
        self.assertEqual(str(node), "TAKE xyz")
    
    def test_of_examining_object(self):
        node = take_item_node(constant_provider("gizmo"))
        game = _game_mock()
        game._location._items.put_item( game._factory.get_object("gizmo") )
        self.assertFalse(game._location._items.peek_item("gizmo") is None)
        self.assertTrue(game._player._items.peek_item("gizmo") is None)
        node.run(game, "")
        self.assertTrue(game._location._items.peek_item("gizmo") is None)
        self.assertFalse(game._player._items.peek_item("gizmo") is None)
        
    def test_of_examining_nonexisting_object(self):
        node = take_item_node(constant_provider("wired unisolation"))
        game = _game_mock()
        node.run(game, "")
        self.assertEqual(game._console._buffer, "I see no wired unisolation\n")

#-------------------------------------------------------------------------

class Test_drop_item_node(unittest.TestCase):

    def test_of_serializing_node(self):
        node = drop_item_node(constant_provider("xyz"))
        self.assertEqual(str(node), "DROP xyz")

    def test_of_examining_object(self):
        node = drop_item_node(constant_provider("wire"))
        game = _game_mock()
        self.assertTrue(game._location._items.peek_item("wire") is None)
        self.assertFalse(game._player._items.peek_item("wire") is None)
        node.run(game, "")
        self.assertFalse(game._location._items.peek_item("wire") is None)
        self.assertTrue(game._player._items.peek_item("wire") is None)
        
    def test_of_examining_nonexisting_object(self):
        node = drop_item_node(constant_provider("wired unisolation"))
        game = _game_mock()
        node.run(game, "")
        self.assertEqual(game._console._buffer, "I see no wired unisolation\n")

#-------------------------------------------------------------------------

class Test_delete_item_node(unittest.TestCase):

    def test_of_serializing_node(self):
        node = delete_item_node(constant_provider("xyz"))
        self.assertEqual(str(node), "DEL xyz")

    def test_of_examining_object(self):
        node = delete_item_node(constant_provider("wire"))
        game = _game_mock()
        self.assertTrue(game._location._items.peek_item("wire") is None)
        self.assertFalse(game._player._items.peek_item("wire") is None)
        node.run(game, "")
        self.assertTrue(game._location._items.peek_item("wire") is None)
        self.assertTrue(game._player._items.peek_item("wire") is None)
        
    def test_of_examining_nonexisting_object(self):
        node = delete_item_node(constant_provider("wired unisolation"))
        game = _game_mock()
        node.run(game, "")
        self.assertEqual(game._console._buffer, "I see no wired unisolation\n")
  
#-------------------------------------------------------------------------

class Test_execute_command_node(unittest.TestCase):

    def test_of_serializing_node(self):
        node = execute_command_node("look")
        self.assertEqual(str(node), "EXEC look")

    def test_of_execution_proper_command(self):
        node = execute_command_node("look")
        game = _game_mock()
        game._location = game._factory.get_object("test location")
        node.run(game, "")
        self.assertEqual(game._console._buffer, "It is too dark to see anything. You should relay or other senses.\n")
        
    def test_of_execution_private_command(self):
        node = execute_command_node("_ run something")
        game = _game_mock()
        game._location = game._factory.get_object("test location")
        node.run(game, "")
        self.assertEqual(game._console._buffer, "Something was running\n")
       
    def test_of_examining_nonexisting_object(self):
        node = execute_command_node("nonexisting command")
        game = _game_mock()
        try:
            node.run(game, "")
            self.assertTrue(False)
        except break_action: 
            pass
        except:
            self.assertTrue(False)
  
#-------------------------------------------------------------------------

class Test_of_become_node(unittest.TestCase):

    def test_of_properely_executed_become_node(self):
        become = become_node("knight")
        game = _game_mock()
        become.run(game, "")
        self.assertTrue(type(game._player._items.peek_item("matches")) is item)
        
    def test_of_object_type_error(self):
        become = become_node("test1")
        game = _game_mock()
        try:
            become.run(game, "")
            self.assertTrue(False)
        except error as err:
            self.assertEqual(str(err), "ERROR: 'test1' is not a character")
        except Exception:
            self.assertTrue(False)

    def test_of_missing_object_error(self):
        become = become_node("nobody")
        game = _game_mock()
        try:
            become.run(game, "")
            self.assertTrue(False)
        except error as err:
            self.assertEqual(str(err), "ERROR: Cannot create object named 'nobody' because '[Errno 2] No such file or directory: '../dream/tests/nobody.def''")
        except Exception:
            self.assertTrue(False)

#-------------------------------------------------------------------------

class Test_modify_property_base(unittest.TestCase):

    def test_building_node(self):
        property = player_property_provider("life")
        expression = constant_value_expression(123)
        exe = modify_property_base(property, expression)
        game = _game_mock()
        self.assertTrue(exe._property.value(game, ""), 1000)
        self.assertTrue(exe._expression.value(game, ""), 123)
        
#-------------------------------------------------------------------------

class Test_advance_property_node(unittest.TestCase):

    def test_of_advance_property_1(self):
        property = player_property_provider("life")
        expression = constant_value_expression(123)
        exe = advance_property_node(property, expression)
        game = _game_mock()
        exe.run(game, "")
        exe.run(game, "")
        self.assertTrue(game._player._properties.get("life"), 1246)
        
    def test_of_advance_property_1(self):
        property = player_property_provider("x23")
        expression = constant_value_expression(123)
        exe = advance_property_node(property, expression)
        game = _game_mock()
        exe.run(game, "")
        exe.run(game, "")
        self.assertTrue(game._player._properties.get("x23"), 246)
 
    def test_of_serialization(self):
        property = player_property_provider("x23")
        expression = constant_value_expression(123)
        exe = advance_property_node(property, expression)
        self.assertEqual(str(exe), "MODIFY PLAYER x23 BY 123")
 
#-------------------------------------------------------------------------

class Test_set_property_node(unittest.TestCase):

    def test_of_advance_property_1(self):
        property = player_property_provider("life")
        expression = constant_value_expression(123)
        exe = set_property_node(property, expression)
        game = _game_mock()
        exe.run(game, "")
        exe.run(game, "")
        self.assertTrue(game._player._properties.get("life"), 123)
        
    def test_of_advance_property_1(self):
        property = player_property_provider("x23")
        expression = constant_value_expression(123)
        exe = set_property_node(property, expression)
        game = _game_mock()
        exe.run(game, "")
        exe.run(game, "")
        self.assertTrue(game._player._properties.get("x23"), 123)
        
    def test_of_serialization(self):
        property = player_property_provider("x23")
        expression = constant_value_expression(123)
        exe = set_property_node(property, expression)
        self.assertEqual(str(exe), "MODIFY PLAYER x23 TO 123")
 
#-------------------------------------------------------------------------

class Test_dump_node(unittest.TestCase):

    def test_of_dump_player(self):
        node = dump_node(player_provider())
        game = _game_mock()
        node.run(game, "")
        self.assertEqual(game._console._debug, \
                "[type]\n" \
                "player\n\n" \
                "[properties]\n" \
                "mana = 5000\n" \
                "life = 1000\n\n" \
                "[items]\n" \
                "lockpick\n" \
                "wire\n")
    
    def test_of_dump_location(self):
        node = dump_node(location_provider())
        game = _game_mock()
        node.run(game, "")
        self.assertEqual(game._console._debug, \
                "[type]\n" \
                "location\n\n" \
                "[name]\n" \
                "-nothing-\n\n" \
                "[realm]\n" \
                "reality\n\n" \
                "[properties]\n\n" \
                "[items]\n\n" \
                "[description]\n" \
                "loc.\nlong description of location\n\n[actions]\n")
    
    def test_of_dump_realm(self):
        node = dump_node(realm_provider())
        game = _game_mock()
        node.run(game, "wire")
        self.assertEqual(game._console._debug, \
                "[type]\n" \
                "realm\n\n" \
                "[name]\n" \
                "reality\n\n" \
                "[actions]\n" \
                "wake up; exit THEN PRINT You woke up from the dream.; EXIT\n" \
                "look THEN LOOK\ni; inventory; pocket THEN POCKET\ntake THEN TAKE OBJECT\n")
    
    def test_of_dump_object(self):
        node = dump_node(object_parameter_provider())
        game = _game_mock()
        node.run(game, "wire")
        self.assertEqual(game._console._debug, \
                "[type]\n" \
                "item\n\n" \
                "[name]\n" \
                "wire\n" \
                "unisolated wire\n" \
                "aluminum wire\n\n" \
                "[properties]\n" \
                "resistance = 1\n\n" \
                "[description]\n" \
                "Short piece of shiny wire.\n" \
                "This is a piece of wire. It is about 20cm long and it looks like made of aluminium. It is preety hard to bend, but bendable in bare fingers.\n\n[actions]\n")
    
    def test_of_dump_serialization(self):
        node = dump_node(location_provider())
        self.assertEqual(str(node), "DUMP LOCATION")
    
#-------------------------------------------------------------------------

class Test_trace_node(unittest.TestCase):

    def test_of_start_trace(self):
        orders  = [ "on", "look" ]
        io      = testing_console(orders)
        factory = object_factory("../dream/tests")
        game    = processor(factory, io, "tracetest")
        game.run()
        self.assertEqual(game._console._debug, 
                "----- trace started\nattempt to execute player items actions\n" \
                "attempt to execute location items actions\nattempt to execute location actions\nattempt to execute realm acctions\n" \
                " - action 'look THEN LOOK' match user command\n" \
                "   - all conditions satisfied;\n" \
                "   - executing: LOOK\n")
 
    def test_of_stop_trace(self):
        orders  = [ "on", "off", "look" ]
        io      = testing_console(orders)
        factory = object_factory("../dream/tests")
        game    = processor(factory, io, "tracetest")
        game.run()
        self.assertEqual(game._console._debug, \
                "----- trace started\nattempt to execute player items actions\n" \
                "attempt to execute location items actions\nattempt to execute location actions\n" \
                " - action 'off THEN TRACE 0' match user command\n" \
                "   - all conditions satisfied;\n" \
                "   - executing: TRACE 0\n" \
                "----- trace stopped\n")
 
    def test_of_trace_serialization(self):
        node = set_trace_node(constant_value_expression(1))
        self.assertEqual(str(node), "TRACE 1")
    
#-------------------------------------------------------------------------

class Test_command_name(unittest.TestCase):

    def test_of_matching_simple_command_text(self):
        names = command_name(["wake up", "die"])
        self.assertEqual(7, names.length_of_a_command_if_match("wake up"))
        self.assertEqual(0, names.length_of_a_command_if_match("resurect"))
        self.assertEqual(3, names.length_of_a_command_if_match("die"))
        self.assertEqual(0, names.length_of_a_command_if_match("give up"))
        
    def test_of_matching_whole_word(self):
        names = command_name(["n"])
        self.assertEqual(0, names.length_of_a_command_if_match("ne"))
        self.assertEqual(0, names.length_of_a_command_if_match("ne 123"))

    def test_of_names_serialization(self):
        names = command_name(["wake up", "die", "sayonara"])
        self.assertEqual(str(names), "wake up; die; sayonara")
        
#-------------------------------------------------------------------------

class Test_command(unittest.TestCase):
    
    def test_executing_command_1(self):
        cmd = command(command_name(["good by", "sayonara"]), [], [exit_node()] )
        game = _game_mock()
        self.assertFalse( cmd.try_execute("hello", game) )
        self.assertEqual( game.log, "" )
        self.assertTrue( cmd.try_execute("sayonara", game) )
        self.assertEqual( game.log, "Stop was called\n" )
    
    def test_executing_command_with_condition_1(self):
        cmd = command(command_name( ["good by", "sayonara"]), \
                                    [comparision_equal_condition(player_property_provider("life"), constant_value_expression(1000))], \
                                    [exit_node()] )
        game = _game_mock()
        self.assertTrue( cmd.try_execute("sayonara", game) )
        
    def test_executing_command_with_condition_2(self):
        cmd = command(command_name( ["good by", "sayonara"]), \
                                    [comparision_equal_condition(player_property_provider("life"), constant_value_expression(3000))], \
                                    [exit_node()] )
        game = _game_mock()
        self.assertFalse( cmd.try_execute("sayonara", game) )
    
    def test_serializing_commandwithout_condition(self):
        cmd = command(command_name(["good by", "sayonara"]), [], [exit_node()] )
        self.assertEqual(str(cmd), "good by; sayonara THEN EXIT")

    def test_serializing_command_with_conditions(self):
        cmd = command(command_name( ["good by", "sayonara"]), \
                                    [comparision_equal_condition(player_property_provider("life"), constant_value_expression(3000)), \
                                     comparision_equal_condition(player_property_provider("mana"), constant_value_expression(1000)) ], \
                                    [exit_node()] )
        game = _game_mock()
        self.assertEqual( str(cmd), "good by; sayonara WHEN PLAYER life = 3000; PLAYER mana = 1000 THEN EXIT" )
    
        
#-------------------------------------------------------------------------

