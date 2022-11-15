#-------------------------------------------------------------------------
# DREAM (C) WGan 2020
#-------------------------------------------------------------------------

""" Processor is a module which process and changes state of the game, by
    processing commands on given items """

import                  unittest
from errors      import error, \
                        break_action
from compiler    import object_provider, \
                        object_parameter_provider, \
                        exit_node, \
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
                        compiler, \
                        object_parameter_provider, \
                        subject_parameter_provider, \
                        constant_provider, \
                        new_object_provider, \
                        examine_node
from data        import items, \
                        item
from tools_test  import _game_mock

#-------------------------------------------------------------------------

class Test_object_provider(unittest.TestCase):

    def test_unitialized_object(self):
        node = object_provider()
        self.assertEqual(node._name, "")
        self.assertTrue(node._object is None)
        self.assertFalse(node._already_taken)
        
    def test_initialization_with_existing_object(self):
        node = object_provider()
        game = _game_mock()
        node.set_accessible_object_name("unisolated wire", game)
        self.assertEqual(node._name, "wire")
        self.assertTrue(node.peek_object() is game._pocket.peek_item("wire"))
        
    def test_initialization_with_non_existing_object(self):
        node = object_provider()
        game = _game_mock()
        node.set_accessible_object_name("unwired isolation", game)
        self.assertEqual(node._name, "unwired isolation")
        self.assertTrue(node.peek_object() is None)
        
    def test_taking_existing_object(self):
        node = object_provider()
        game = _game_mock()
        node.set_accessible_object_name("unisolated wire", game)
        self.assertEqual(node._name, "wire")
        wire = game._pocket.peek_item("wire")
        self.assertTrue(node.take_object(game) is wire)
        self.assertTrue(game._pocket.peek_item("wire") is None)
        
    def test_taking_non_existing_object(self):
        node = object_provider()
        game = _game_mock()
        node.set_accessible_object_name("unwired isolation", game)
        self.assertEqual(node._name, "unwired isolation")
        self.assertTrue(node.take_object(game) is None)
        
#-------------------------------------------------------------------------

class Test_object_parameter_provider(unittest.TestCase):

    def test_object_parameter_provider_found(self):
        node = object_parameter_provider()
        game = _game_mock()
        node.set_parameters(game, "wire connector")
        self.assertEqual(node.get_name(), "wire connector")
        self.assertTrue(node.peek_object() is None)

    def test_object_parameter_provider_not_found(self):
        node = object_parameter_provider()
        game = _game_mock()
        node.set_parameters(game, " connecting wire")
        self.assertEqual(node.get_name(), "wire")
        self.assertTrue(type(node.peek_object()) is item)

    def test_object_parameter_provider_to_string(self):
        node = object_parameter_provider()
        self.assertEqual(str(node), "OBJECT")

#-------------------------------------------------------------------------

class Test_subject_parameter_provider(unittest.TestCase):

    def test_subject_parameter_provider_found(self):
        node = subject_parameter_provider()
        game = _game_mock()
        node.set_parameters(game, "wire connector")
        self.assertEqual(node.get_name(), "wire")
        self.assertTrue(type(node.peek_object()) is item)

    def test_subject_parameter_provider_not_found(self):
        node = subject_parameter_provider()
        game = _game_mock()
        node.set_parameters(game, "connecting wire")
        self.assertEqual(node.get_name(), "connecting wire")
        self.assertTrue(node.peek_object() is None)

    def test_subject_parameter_provider_to_string(self):
        node = subject_parameter_provider()
        self.assertEqual(str(node), "SUBJECT")

#-------------------------------------------------------------------------

class Test_constant_provider(unittest.TestCase):

    def test_constant_provider_found(self):
        node = constant_provider("wire")
        game = _game_mock()
        node.set_parameters(game, "strange connector")
        self.assertEqual(node.get_name(), "wire")
        self.assertTrue(type(node.peek_object()) is item)

    def test_constant_provider_not_found(self):
        node = constant_provider("gizmo")
        game = _game_mock()
        node.set_parameters(game, "wire wire wire")
        self.assertEqual(node.get_name(), "gizmo")
        self.assertTrue(node.peek_object() is None)

    def test_constant_provider_to_string(self):
        node = constant_provider("some text")
        self.assertEqual(str(node), "some text")

#-------------------------------------------------------------------------

class Test_new_provider(unittest.TestCase):

    def test_new_provider_found(self):
        game = _game_mock()
        game._pocket.put_item( game._factory.get_object("box of matches") )
        obj = new_object_provider(constant_provider("mathes"))
        obj.set_parameters(game, "")
        self.assertEqual(obj.get_name(), "box of matches")
        self.assertTrue(type(obj.peek_object()) is item)
    
    def test_new_provider_not_found(self):
        node = new_object_provider(constant_provider("gizmo"))
        game = _game_mock()
        node.set_parameters(game, "wire wire wire")
        self.assertEqual(node.get_name(), "gizmo")
        self.assertTrue(type(node.peek_object()) is item)
    
    def test_new_provider_nonexisting_object(self):
        node = new_object_provider(constant_provider("gizmolada"))
        game = _game_mock()
        node.set_parameters(game, "wire wire wire")
        self.assertEqual(node.get_name(), "gizmolada")
        self.assertTrue(node.peek_object() is None)
    
    def test_new_provider_copies_item(self):
        game = _game_mock()
        game._pocket.put_item( game._factory.get_object("box of matches") )
        obj = new_object_provider(constant_provider("mathes"))
        obj.set_parameters(game, "")
        self.assertEqual(obj.get_name(), "box of matches")
        self.assertTrue(type(obj.take_object(game)) is item)
        self.assertFalse(game._pocket.peek_item("box of matches") is None)

    def test_new_creating_item_to_string(self):
        obj = new_object_provider(constant_provider("box of matches"))
        self.assertEqual(str(obj), "NEW box of matches")

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
        game._pocket = items()
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
        self.assertTrue(game._pocket.peek_item("gizmo") is None)
        node.run(game, "")
        self.assertTrue(game._location._items.peek_item("gizmo") is None)
        self.assertFalse(game._pocket.peek_item("gizmo") is None)
        
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
        self.assertFalse(game._pocket.peek_item("wire") is None)
        node.run(game, "")
        self.assertFalse(game._location._items.peek_item("wire") is None)
        self.assertTrue(game._pocket.peek_item("wire") is None)
        
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
        self.assertFalse(game._pocket.peek_item("wire") is None)
        node.run(game, "")
        self.assertTrue(game._location._items.peek_item("wire") is None)
        self.assertTrue(game._pocket.peek_item("wire") is None)
        
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
        cmd = command(command_name(["good by", "sayonara"]), [exit_node()] )
        game = _game_mock()
        self.assertFalse( cmd.try_execute("hello", game) )
        self.assertEqual( game.log, "" )
        self.assertTrue( cmd.try_execute("sayonara", game) )
        self.assertEqual( game.log, "Stop was called\n" )
    
    def test_serializing_command(self):
        cmd = command(command_name(["good by", "sayonara"]), [exit_node()] )
        self.assertEqual(str(cmd), "good by; sayonara THEN EXIT")
      
#-------------------------------------------------------------------------

class Test_compiler(unittest.TestCase):

    def test_of_compile_order_1(self):
        comp = compiler()
        order = comp.compile("hello THEN PRINT You say 'hello'. You hear random time echos showing the place to be large and complex.")
        self.assertEqual(order._name._possibilities[0], "hello")
        self.assertTrue(type(order._executables[0]) is print_text_node)
        self.assertEqual(order._executables[0]._text, "You say 'hello'. You hear random time echos showing the place to be large and complex.")
       
    def test_of_compile_order_2(self):
        comp = compiler()
        order = comp.compile("wake up; exit THEN EXIT")
        self.assertEqual(order._name._possibilities[0], "wake up")
        self.assertEqual(order._name._possibilities[1], "exit")
        self.assertTrue(type(order._executables[0]) is exit_node)
       
    def test_of_compile_order_3(self):
        comp = compiler()
        order = comp.compile("look THEN LOOK")
        self.assertEqual(order._name._possibilities[0], "look")
        self.assertTrue(type(order._executables[0]) is look_around_node)
       
    def test_of_compile_order_4(self):
        comp = compiler()
        order = comp.compile("look THEN EXAMINE single item")
        self.assertTrue(type(order._executables[0]) is examine_node)
       
    def test_of_compile_order_5(self):
        comp = compiler()
        order = comp.compile("x THEN TAKE single item")
        self.assertTrue(type(order._executables[0]) is take_item_node)
       
    def test_of_compile_order_6(self):
        comp = compiler()
        order = comp.compile("x THEN DROP single item")
        self.assertTrue(type(order._executables[0]) is drop_item_node)
       
    def test_of_compile_order_7(self):
        comp = compiler()
        order = comp.compile("x THEN DEL single item")
        self.assertTrue(type(order._executables[0]) is delete_item_node)
       
    def test_of_failing_compilation_because_no_name(self):
        comp = compiler()
        try:
            order = comp.compile("THEN EXIT")
            self.assertTrue(False)
        except error as err:
            self.assertEqual(str(err), "ERROR: At least one name should be attached to action")

    def test_of_failing_compilation_because_no_command(self):
        comp = compiler()
        try:
            order = comp.compile("wake up; exit")
            self.assertTrue(False)
        except error as err:
            self.assertEqual(str(err), "ERROR: At least one statement should be attached to action")

    def test_of_splitting_on_word(self):
        comp = compiler()
        x = comp._split_on_word("name1; name2 WITH parameters", "WITH")
        self.assertEqual(x[0], "name1; name2 ")
        self.assertEqual(x[1], " parameters")
         
    def test_of_splitting_on_nonexisting_word(self):
        comp = compiler()
        x = comp._split_on_word("name1; name2 WITH parameters", "THEN")
        self.assertEqual(x[1], "")
        self.assertEqual(x[0], "name1; name2 WITH parameters")
        
    def test_of_decompose_list(self):
        comp = compiler()
        x = comp._decompose_list("name1; name2; parameters")
        self.assertEqual(len(x), 3)
        self.assertEqual(x[0], "name1")
        self.assertEqual(x[1], "name2")
        self.assertEqual(x[2], "parameters")
        
    def test_of_decompose_order_1(self):
        comp = compiler()
        x = comp._decompose_order("name1; name2 WHEN cond1; A=b; xyz THEN EXIT")
        self.assertEqual(str(x), "[['name1', 'name2'], ['cond1', 'A=b', 'xyz'], ['EXIT']]")
        
    def test_of_decompose_order_2(self):
        comp = compiler()
        x = comp._decompose_order("name1; name2 THEN EXIT")
        self.assertEqual(str(x), "[['name1', 'name2'], [], ['EXIT']]")
        
    def test_of_checking_if_command_exist(self):
        comp = compiler()
        self.assertTrue( comp._is_it_command("just HELLO, darling", "HELLO") )
        self.assertTrue( comp._is_it_command("HELLO, just darling", "HELLO") )
        self.assertTrue( comp._is_it_command("just, darling HELLO", "HELLO") )
        self.assertFalse( comp._is_it_command("just, darling HELLO", "ZDRAWSTWUJTE") )
    
    def test_of_check_no_parameters_1(self):
        comp = compiler()
        try:
            comp._check_no_parameters("EXITS", "EXIT")
            self.assertTrue(False)
        except error as err:
            self.assertEqual(str(err), "ERROR: EXIT command must stay alone. It does not accept parameters")
        
    def test_of_check_no_parameters_2(self):
        comp = compiler()
        comp._check_no_parameters("EXIT", "EXIT")
    
    def test_of_get_single_after_parameter_1(self):
        comp = compiler()
        try:
            comp._get_single_after_parameter("12 PRINT abcde", "PRINT")
            self.assertTrue(False)
        except error as err:
            self.assertEqual(str(err), "ERROR: PRINT  must start with PRINT command.")
    
    def test_of_get_single_after_parameter_2(self):
        comp = compiler()
        self.assertEqual( comp._get_single_after_parameter("PRINT abcde", "PRINT"), "abcde")
    
    def test_of_get_single_after_parameter_3(self):
        comp = compiler()
        self.assertEqual( comp._get_single_after_parameter("PRINT", "PRINT"), "")
    
    def test_of_compiling_exit_node(self):
        comp = compiler()
        obj = comp._compile_exit_node("EXIT")
        self.assertTrue(type(obj) == exit_node )
        try:
            obj = comp._compile_exit_node("xEXIT")
            self.assertTrue(False)
        except error as err:
            self.assertEqual(str(err), "ERROR: EXIT command must stay alone. It does not accept parameters")
    
    def test_of_compiling_print_text_node(self):
        comp = compiler()
        obj = comp._compile_look_around_node("LOOK")
        self.assertTrue(type(obj), look_around_node)
        try:
            obj = comp._compile_look_around_node("LOOK at item")
            self.assertTrue(False)
        except error as err:
            self.assertEqual(str(err), "ERROR: LOOK command must stay alone. It does not accept parameters")
    
    def test_of_compiling_inventory_node(self):
        comp = compiler()
        obj = comp._compile_inventory_node("POCKET")
        self.assertTrue(type(obj), inventory_node)
        try:
            obj = comp._compile_inventory_node("POCKET with item")
            self.assertTrue(False)
        except error as err:
            self.assertEqual(str(err), "ERROR: POCKET command must stay alone. It does not accept parameters")
    
    def test_compile_single_order_1(self):
        comp = compiler()
        obj = comp._compile_single_order("EXIT")
        self.assertTrue(type(obj) is exit_node)

    def test_compile_single_order_2(self):
        comp = compiler()
        try:
            obj = comp._compile_single_order("EXITTE dragon")
            self.assertTrue(False)
        except error as err:
            self.assertEqual(str(err), "ERROR: EXIT command must stay alone. It does not accept parameters")

    def test_compile_single_order_3(self):
        comp = compiler()
        try:
            obj = comp._compile_single_order("BENNE")
            self.assertTrue(False)
        except error as err:
            self.assertEqual(str(err), "ERROR: Unknown command: 'BENNE'")

    def test_compile_single_order_4(self):
        comp = compiler()
        obj = comp._compile_single_order("GOTO xyz")
        self.assertTrue(type(obj) is change_location_node)
        self.assertEqual(obj._location_name, "xyz")

    def test_compile_single_order_5(self):
        comp = compiler()
        obj = comp._compile_single_order("POCKET")
        self.assertTrue(type(obj) is inventory_node)

    def test_compile_single_order_6(self):
        comp = compiler()
        obj = comp._compile_single_order("EXEC look")
        self.assertTrue(type(obj) is execute_command_node)

    def test_compile_goto_node(self):
        comp = compiler()
        obj = comp._compile_goto_node("GOTO abc")
        self.assertTrue(type(obj) is change_location_node)
        self.assertEqual(obj._location_name, "abc")
        
    def test_compile_object_provider_object(self):
        comp = compiler()
        obj = comp._compile_object_provider("OBJECT")
        self.assertTrue(type(obj) is object_parameter_provider)
        
    def test_compile_object_provider_subject(self):
        comp = compiler()
        obj = comp._compile_object_provider("SUBJECT")
        self.assertTrue(type(obj) is subject_parameter_provider)
        
    def test_compile_object_provider_constant(self):
        comp = compiler()
        obj = comp._compile_object_provider("jakis item")
        self.assertTrue(type(obj) is constant_provider)
        self.assertEqual(obj._constant_name, "jakis item")
        
    def test_compile_new_provider_constant(self):
        comp = compiler()
        obj = comp._compile_object_provider("NEW jakis item")
        self.assertTrue(type(obj) is new_object_provider)
        self.assertEqual(obj._child_provider._constant_name, "jakis item")
        
    def test_compilation_examine_node(self):
        comp = compiler()
        obj = comp._compile_examine_node("EXAMINE jakis object")
        self.assertTrue(type(obj) is examine_node)
        self.assertTrue(type(obj._object_provider) is constant_provider)
        
    def test_compilation_take_node(self):
        comp = compiler()
        obj = comp._compile_take_node("TAKE jakis object")
        self.assertTrue(type(obj) is take_item_node)
        self.assertTrue(type(obj._object_provider) is constant_provider)
        
    def test_compilation_drop_node(self):
        comp = compiler()
        obj = comp._compile_drop_node("DROP jakis object")
        self.assertTrue(type(obj) is drop_item_node)
        self.assertTrue(type(obj._object_provider) is constant_provider)
        
    def test_compilation_delete_node(self):
        comp = compiler()
        obj = comp._compile_del_item_node("DEL jakis object")
        self.assertTrue(type(obj) is delete_item_node)
        self.assertTrue(type(obj._object_provider) is constant_provider)
        
    def test_compilation_exec_node(self):
        comp = compiler()
        obj = comp._compile_exec_node("EXEC look")
        self.assertTrue(type(obj) is execute_command_node)
        self.assertEqual(obj._text, "look")
        
#-------------------------------------------------------------------------

