#-------------------------------------------------------------------------
# DREAM (C) WGan 2020
#-------------------------------------------------------------------------

""" Processor is a module which process and changes state of the game, by
    processing commands on given items """

import                  unittest
from errors      import error
from compiler    import exit_node, \
                        print_text_node, \
                        look_around_node, \
                        change_location_node, \
                        command_name, \
                        command, \
                        compiler
from tools_test  import _game_mock

#-------------------------------------------------------------------------

class Test_exit_node(unittest.TestCase):
    
    def test_of_exit_node(self):
        node = exit_node()
        game = _game_mock()
        node.run(game)
        self.assertEqual(game.log, "Stop was called\n")
        
    def test_of_exit_node_serialization(self):
        node = exit_node()
        self.assertEqual(str(node), "EXIT")
        
#-------------------------------------------------------------------------

class Test_print_text_node(unittest.TestCase):

    def test_of_serializing_node(self):
        node = print_text_node("This is a text")
        self.assertEqual(str(node), "PRINT This is a text")
        
    def test_of_execution(self):
        node = print_text_node("This is a text")
        game = _game_mock()
        node.run(game)
        self.assertEqual(game._console._buffer, "This is a text\n")

#-------------------------------------------------------------------------

class Test_look_around_node(unittest.TestCase):

    def test_of_serializing_node(self):
        node = look_around_node()
        self.assertEqual(str(node), "LOOK")
        
    def test_of_execution(self):
        node = look_around_node()
        game = _game_mock()
        node.run(game)
        self.assertEqual(game._console._buffer, "long description of location\n")
        
#-------------------------------------------------------------------------

class Test_change_location_node(unittest.TestCase):

    def test_of_serializing_node(self):
        node = change_location_node('somewhere')
        self.assertEqual(str(node), "GOTO somewhere")

    def test_of_execution(self):
        node = change_location_node("mansion hall")
        game = _game_mock()
        node.run(game)
        self.assertEqual(game._console._buffer, "You are in mansion hall\nYou see doors around however main door located on south looks not real.\n")
        
#-------------------------------------------------------------------------

class Test_command_name(unittest.TestCase):

    def test_of_matching_simple_command_text(self):
        names = command_name(["wake up", "die"])
        self.assertTrue(names.is_that_a_command("wake up"))
        self.assertFalse(names.is_that_a_command("resurect"))
        self.assertTrue(names.is_that_a_command("wake up"))
        self.assertFalse(names.is_that_a_command("give up"))
        
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
        x = comp._decompose_order("name1; name2 WITH parameter WHEN cond1; A=b; xyz THEN EXIT")
        self.assertEqual(str(x), "[['name1', 'name2'], ['parameter'], ['cond1', 'A=b', 'xyz'], ['EXIT']]")
        
    def test_of_decompose_order_2(self):
        comp = compiler()
        x = comp._decompose_order("name1; name2 THEN EXIT")
        self.assertEqual(str(x), "[['name1', 'name2'], [], [], ['EXIT']]")
        
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

    def test_compile_goto_node(self):
        comp = compiler()
        obj = comp._compile_goto_node("GOTO abc")
        self.assertTrue(type(obj) is change_location_node)
        self.assertEqual(obj._location_name, "abc")

            
#-------------------------------------------------------------------------

