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
                        object_parameter_provider, \
                        subject_parameter_provider, \
                        constant_provider, \
                        new_object_provider, \
                        constant_value_expression, \
                        sum_expression, \
                        product_expression, \
                        object_property_provider, \
                        subject_property_provider, \
                        location_property_provider, \
                        player_property_provider, \
                        item_property_provider, \
                        free_text_property_provider, \
                        item_parameter_provider, \
                        dice_expression, \
                        location_provider, \
                        realm_provider, \
                        player_provider
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
                        advance_property_node, \
                        set_property_node, \
                        set_trace_node, \
                        dump_node
from condition   import comparision_less_or_equal_condition, \
                        comparision_greater_or_equal_condition, \
                        comparision_not_equal_condition, \
                        comparision_less_condition, \
                        comparision_greater_condition, \
                        comparision_equal_condition
from compiler    import compiler
from data        import items, \
                        item
from tools_test  import _game_mock

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

    def test_compile_single_order_7(self):
        comp = compiler()
        obj = comp._compile_single_order("BECOME knight")
        self.assertTrue(type(obj) is become_node)

    def test_compile_single_order_8(self):
        comp = compiler()
        obj = comp._compile_single_order("MODIFY ITEM property BY 100")
        self.assertTrue(type(obj) is advance_property_node)

    def test_compile_single_order_9(self):
        comp = compiler()
        obj = comp._compile_single_order("MODIFY ITEM property TO 100")
        self.assertTrue(type(obj) is set_property_node)

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
        
    def test_compile_object_provider_item(self):
        comp = compiler()
        obj = comp._compile_object_provider("ITEM")
        self.assertTrue(type(obj) is item_parameter_provider)
        
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
        
    def test_compilation_become_node(self):
        comp = compiler()
        obj = comp._compile_become_node("BECOME knight")
        self.assertTrue(type(obj) is become_node)
        self.assertEqual(obj._hero_type, "knight")
        
    def test_of_compile_modify_node_1(self):
        comp = compiler()
        node = comp._compile_modify_node("MODIFY anvil weight BY 100")
        self.assertTrue(type(node) is advance_property_node)
        self.assertTrue(type(node._expression) is constant_value_expression)
        self.assertEqual(node._expression._value, 100)
        self.assertTrue(type(node._property) is free_text_property_provider)
        self.assertEqual(node._property._full_property_name, "anvil weight")
    
    def test_of_compile_modify_node_2(self):
        comp = compiler()
        node = comp._compile_modify_node("MODIFY anvil weight TO 100")
        self.assertTrue(type(node) is set_property_node)
        self.assertTrue(type(node._expression) is constant_value_expression)
        self.assertEqual(node._expression._value, 100)
        self.assertTrue(type(node._property) is free_text_property_provider)
        self.assertEqual(node._property._full_property_name, "anvil weight")
    
    def test_of_compile_modify_node_error_1(self):
        comp = compiler()
        try:
            node = comp._compile_modify_node("MODIFY anvil weight 100")
            self.assertTrue(False)
        except error as err:
            self.assertEqual(str(err), "ERROR: MODIFY must have format: <property> BY/TO <expression>")
        except Exception:
            self.assertTrue(False)      
    
    def test_of_compile_modify_node_error_2(self):
        comp = compiler()
        try:
            node = comp._compile_modify_node("MODIFY TO anvil weight TO 100")
            self.assertTrue(False)
        except error as err:
            self.assertEqual(str(err), "ERROR: MODIFY must have format: <property> TO <expression>")
        except Exception:
            self.assertTrue(False)      
    
    def test_of_compile_modify_node_error_3(self):
        comp = compiler()
        try:
            node = comp._compile_modify_node("MODIFY TO 100")
            self.assertTrue(False)
        except error as err:
            self.assertEqual(str(err), "ERROR: At least two words are needed to specify item nad property names.")
        except Exception:
            self.assertTrue(False)      
    
    def test_of_compile_modify_node_error_4(self):
        comp = compiler()
        try:
            node = comp._compile_modify_node("MODIFY TO anvil weight TO")
            self.assertTrue(False)
        except error as err:
            self.assertEqual(str(err), "ERROR: MODIFY must have format: <property> TO <expression>")
        except Exception:
            self.assertTrue(False)      
    
    def test_get_two_expressions(self):
        comp = compiler()
        result = comp._get_two_expressions("123 XXX 654", "XXX")
        self.assertEqual(result[0].value(None, None), 123)
        self.assertEqual(result[1].value(None, None), 654)
        
    def test_get_two_expressions_missing_parameter_1(self):
        comp = compiler()
        try:
            result = comp._get_two_expressions("123 XXX", "XXX")
            self.assertTrue(False)
        except error as err:
            self.assertEqual(str(err), "ERROR: Right expression cannot be empty")
        except Exception:
            self.assertTrue(False)
        
    def test_get_two_expressions_missing_parameter_1(self):
        comp = compiler()
        try:
            result = comp._get_two_expressions("XXX 546", "XXX")
            self.assertTrue(False)
        except error as err:
            self.assertEqual(str(err), "ERROR: Left expression cannot be empty")
        except Exception:
            self.assertTrue(False)
        
    def test_get_two_expressions_wrong_expression(self):
        comp = compiler()
        result = comp._get_two_expressions("sometgi sdsd XXX 546", "XXX")
        self.assertTrue(type(result[0]) == free_text_property_provider)
        
    def test_of_compile_single_conditions_1(self):
        comp = compiler()
        result = comp._compile_single_condition("1<2")
        self.assertTrue(type(result) is comparision_less_condition)
        
    def test_of_compile_single_conditions_2(self):
        comp = compiler()
        result = comp._compile_single_condition("1>2")
        self.assertTrue(type(result) is comparision_greater_condition)
        
    def test_of_compile_single_conditions_3(self):
        comp = compiler()
        result = comp._compile_single_condition("1=2")
        self.assertTrue(type(result) is comparision_equal_condition)
        
    def test_of_compile_single_conditions_4(self):
        comp = compiler()
        result = comp._compile_single_condition("1<=2")
        self.assertTrue(type(result) is comparision_less_or_equal_condition)
        
    def test_of_compile_single_conditions_5(self):
        comp = compiler()
        result = comp._compile_single_condition("1>=2")
        self.assertTrue(type(result) is comparision_greater_or_equal_condition)
        
    def test_of_compile_single_conditions_6(self):
        comp = compiler()
        result = comp._compile_single_condition("1!=2")
        self.assertTrue(type(result) is comparision_not_equal_condition)
        
    def test_of_compile_single_conditions_error_1(self):
        comp = compiler()
        try:
            result = comp._compile_single_condition("sometgiNG >")
            self.assertTrue(False)
        except error as err:
            self.assertEqual(str(err), "ERROR: Right expression cannot be empty")
        except Exception:
            self.assertTrue(False)

    def test_of_compile_single_conditions_error_2(self):
        comp = compiler()
        try:
            result = comp._compile_single_condition("=sometgiNG")
            self.assertTrue(False)
        except error as err:
            self.assertEqual(str(err), "ERROR: Left expression cannot be empty")
        except Exception:
            self.assertTrue(False)

    def test_of_compile_single_conditions_error_3(self):
        comp = compiler()
        try:
            result = comp._compile_single_condition("<>=>>")
            self.assertTrue(False)
        except error as err:
            self.assertEqual(str(err), "ERROR: At least two words are needed to specify item nad property names.")
        except Exception:
            self.assertTrue(False)

    def test_of_compile_single_conditions_error_4(self):
        comp = compiler()
        try:
            result = comp._compile_single_condition("=")
            self.assertTrue(False)
        except error as err:
            self.assertEqual(str(err), "ERROR: Left expression cannot be empty")
        except Exception:
            self.assertTrue(False)

    def test_of_compile_single_conditions_error_5(self):
        comp = compiler()
        try:
            result = comp._compile_single_condition("sometgiNG XXX 546")
            self.assertTrue(False)
        except error as err:
            self.assertEqual(str(err), "ERROR: 'sometgiNG XXX 546' is not a condition")
        except Exception:
            self.assertTrue(False)

    def test_of_compare_less(self):
        comp = compiler()
        result = comp._compare_less("1<2")
        self.assertTrue(type(result) is comparision_less_condition)
        self.assertEqual(result._left.value(None, None), 1)
        self.assertEqual(result._right.value(None, None), 2)
            
    def test_of_compare_greater(self):
        comp = compiler()
        result = comp._compare_greater("1>2")
        self.assertTrue(type(result) is comparision_greater_condition)
        self.assertEqual(result._left.value(None, None), 1)
        self.assertEqual(result._right.value(None, None), 2)
            
    def test_of_compare_equal(self):
        comp = compiler()
        result = comp._compare_equal("1=2")
        self.assertTrue(type(result) is comparision_equal_condition)
        self.assertEqual(result._left.value(None, None), 1)
        self.assertEqual(result._right.value(None, None), 2)
        
    def test_of_compare_less_or_equal(self):
        comp = compiler()
        result = comp._compare_less_or_equal("1<=2")
        self.assertTrue(type(result) is comparision_less_or_equal_condition)
        self.assertEqual(result._left.value(None, None), 1)
        self.assertEqual(result._right.value(None, None), 2)
        
    def test_of_compare_greater_or_equal(self):
        comp = compiler()
        result = comp._compare_greater_or_equal("1>=2")
        self.assertTrue(type(result) is comparision_greater_or_equal_condition)
        self.assertEqual(result._left.value(None, None), 1)
        self.assertEqual(result._right.value(None, None), 2)
            
    def test_of_compare_not_equal(self):
        comp = compiler()
        result = comp._compare_not_equal("1!=2")
        self.assertTrue(type(result) is comparision_not_equal_condition)
        self.assertEqual(result._left.value(None, None), 1)
        self.assertEqual(result._right.value(None, None), 2)
            
    def test_of_split_on_operations_1(self):
        comp = compiler()
        result = comp._split_on_operations("123+34-223+12-54", "+", "-")
        self.assertEqual(result, ( ["12", "34", "123"], ["54", "223"] ) )
        
    def test_of_split_on_operations_2(self):
        comp = compiler()
        result = comp._split_on_operations("123+34+223", "+", "-")
        self.assertEqual(result, ( ["223", "34", "123"], [ ] ) )
        
    def test_of_split_on_operations_3(self):
        comp = compiler()
        result = comp._split_on_operations("-223", "+", "-")
        self.assertEqual(result, ( [ ], [ "223" ] ) )
        
    def test_of_is_unit_after_split_1(self):
        comp = compiler()
        self.assertTrue(comp._is_unit_after_split([1], []))
        self.assertFalse(comp._is_unit_after_split([], [1]))
        self.assertFalse(comp._is_unit_after_split([], [1, 1]))
        self.assertFalse(comp._is_unit_after_split([1], [1]))
        
    def test_of_compile_simple_expression(self):
        comp = compiler()
        obj = comp._compile_simple_expression("123")
        self.assertTrue(type(obj) == constant_value_expression)
        self.assertEqual(obj.value(None, None), 123)
        
    def test_of_compile_simple_expression(self):
        comp = compiler()
        obj = comp._compile_simple_expression("x123 sss")
        self.assertTrue(type(obj) == free_text_property_provider)
        self.assertEqual(obj._property_name, "x123 sss")

    def test_of_compile_multiplication(self):
        comp = compiler()
        obj = comp._compile_multiplication("20 * 50 / 4 * 5 / 10")
        self.assertTrue(type(obj) == product_expression)
        self.assertEqual(len(obj._mul), 3)
        self.assertEqual(len(obj._div), 2)
        self.assertEqual(obj.value(None, None), 125)
        
    def test_of_simple_multiplication(self):
        comp = compiler()
        obj = comp._compile_multiplication("201")
        self.assertTrue(type(obj) == constant_value_expression)
        self.assertEqual(obj.value(None, None), 201)
        
    def test_of_compile_single_expression(self):
        comp = compiler()
        obj = comp._compile_single_expression("200-120+60*2-20+332")
        self.assertTrue(type(obj) == sum_expression)
        self.assertEqual(len(obj._add), 3)
        self.assertEqual(len(obj._sub), 2)
        self.assertEqual(obj.value(None, None), 512)
        
    def test_of_compile_single_expression_with_multiplication(self):
        comp = compiler()
        obj = comp._compile_single_expression("3*4")
        self.assertTrue(type(obj) == product_expression)
        self.assertEqual(obj.value(None, None), 12)
        
    def test_of_compile_expression_error_1(self):
        comp = compiler()
        try:
            obj = comp._compile_single_expression("3 * * 2")
            self.assertTrue(False)
        except error as err:
            self.assertEqual(str(err), "ERROR: Expression '3 * * 2' is not valid expression")
        
    def test_of_compile_expression_error_2(self):
        comp = compiler()
        try:
            obj = comp._compile_single_expression("3 + + 2")
            self.assertTrue(False)
        except error as err:
            self.assertEqual(str(err), "ERROR: Expression '3 + + 2' is not valid expression")
        
    def test_of_compile_object_property_provider(self):
        comp = compiler()
        obj = comp._compile_property_provider("OBJECT weigth")
        self.assertTrue(type(obj) is object_property_provider)
        self.assertEqual(obj._property_name, "weigth")
        
    def test_of_compile_object_property_provider_error(self):
        comp = compiler()
        try:
            obj = comp._compile_property_provider("OBJECT")
            self.assertTrue(False)
        except error as err:
            self.assertEqual(str(err), "ERROR: Property name must be specified.")
        except Exception:
            self.assertTrue(False)

    def test_of_compile_subject_property_provider(self):
        comp = compiler()
        obj = comp._compile_property_provider("SUBJECT weigth")
        self.assertTrue(type(obj) is subject_property_provider)
        self.assertEqual(obj._property_name, "weigth")
     
    def test_of_compile_subject_property_provider_error(self):
        comp = compiler()
        try:
            obj = comp._compile_property_provider("SUBJECT")
            self.assertTrue(False)
        except error as err:
            self.assertEqual(str(err), "ERROR: Property name must be specified.")
        except Exception:
            self.assertTrue(False)
     
    def test_of_compile_location_property_provider(self):
        comp = compiler()
        obj = comp._compile_property_provider("LOCATION weigth")
        self.assertTrue(type(obj) is location_property_provider)
        self.assertEqual(obj._property_name, "weigth")
     
    def test_of_compile_location_property_provider_error(self):
        comp = compiler()
        try:
            obj = comp._compile_property_provider("LOCATION")
            self.assertTrue(False)
        except error as err:
            self.assertEqual(str(err), "ERROR: Property name must be specified.")
        except Exception:
            self.assertTrue(False)
     
    def test_of_compile_player_property_provider(self):
        comp = compiler()
        obj = comp._compile_property_provider("PLAYER weigth")
        self.assertTrue(type(obj) is player_property_provider)
        self.assertEqual(obj._property_name, "weigth")
     
    def test_of_compile_player_property_provider_error(self):
        comp = compiler()
        try:
            obj = comp._compile_property_provider("PLAYER")
            self.assertTrue(False)
        except error as err:
            self.assertEqual(str(err), "ERROR: Property name must be specified.")
        except Exception:
            self.assertTrue(False)
     
    def test_of_compile_item_property_provider(self):
        comp = compiler()
        obj = comp._compile_property_provider("ITEM weigth")
        self.assertTrue(type(obj) is item_property_provider)
        self.assertEqual(obj._property_name, "weigth")
     
    def test_of_compile_item_property_provider_error(self):
        comp = compiler()
        try:
            obj = comp._compile_property_provider("ITEM")
            self.assertTrue(False)
        except error as err:
            self.assertEqual(str(err), "ERROR: Property name must be specified.")
        except Exception:
            self.assertTrue(False)
     
    def test_of_free_text_property_provider(self):
        comp = compiler()
        obj = comp._compile_property_provider("anvil weigth")
        self.assertTrue(type(obj) is free_text_property_provider)
        self.assertEqual(obj._property_name, "anvil weigth")
     
    def test_of_free_text_property_provider_error(self):
        comp = compiler()
        try:
            obj = comp._compile_property_provider("anvil")
            self.assertTrue(False)
        except error as err:
            self.assertEqual(str(err), "ERROR: At least two words are needed to specify item nad property names.")
        except Exception:
            self.assertTrue(False)
     
    def test_of_compile_dice_expression_1(self):
        comp = compiler()
        expr = comp._compile_simple_expression("DICE")
        self.assertTrue(type(expr) is dice_expression)
        self.assertTrue(type(expr._inner_expression) is constant_value_expression)
        self.assertEqual(expr._inner_expression._value, 6)
     
    def test_of_compile_dice_expression_2(self):
        comp = compiler()
        expr = comp._compile_simple_expression("DICE 20")
        self.assertTrue(type(expr) is dice_expression)
        self.assertTrue(type(expr._inner_expression) is constant_value_expression)
        self.assertEqual(expr._inner_expression._value, 20)
     
    def test_of_compile_dump_node_1(self):
        comp = compiler()
        node = comp._compile_single_order("DUMP item")
        self.assertTrue(type(node) is dump_node)
        self.assertTrue(type(node._object_provider) is constant_provider)
        self.assertEqual(node._object_provider._constant_name, "item")
        
    def test_of_compile_dump_node_2(self):
        comp = compiler()
        node = comp._compile_dump_node("DUMP item")
        self.assertTrue(type(node) is dump_node)
        self.assertTrue(type(node._object_provider) is constant_provider)
        self.assertEqual(node._object_provider._constant_name, "item")
        
    def test_of_compile_dump_node_3_error(self):
        comp = compiler()
        try:
            node = comp._compile_dump_node("DUMP")
            self.assertTrue(False)
        except error as err:
            self.assertEqual(str(err), "ERROR: DUMP need parameter - object to dump")
        
    def test_of_compile_trace_node_1(self):
        comp = compiler()
        node = comp._compile_trace_node("TRACE 1")
        self.assertTrue(type(node) is set_trace_node)
        self.assertTrue(type(node._expression) is constant_value_expression)
        self.assertEqual(node._expression._value, 1)
        
    def test_of_compile_trace_node_2(self):
        comp = compiler()
        node = comp._compile_single_order("TRACE 1")
        self.assertTrue(type(node) is set_trace_node)
        self.assertTrue(type(node._expression) is constant_value_expression)
        self.assertEqual(node._expression._value, 1)
        
    def test_of_compile_trace_node_3_error(self):
        comp = compiler()
        try:
            node = comp._compile_single_order("TRACE")
            self.assertTrue(False)
        except error as err:
            self.assertEqual(str(err), "ERROR: TRACE need parameter - value or expression")
        
    def test_of_compile_trace_node_4_error(self):
        comp = compiler()
        node = comp._compile_single_order("TRACE 1 2 3")
        self.assertTrue(type(node._expression) is free_text_property_provider)
        self.assertEqual(node._expression._property_name, "1 2 3")
        
    def test_of_compile_dump_location_provider(self):
        comp = compiler()
        prov = comp._compile_dump_object_provider("LOCATION")
        self.assertTrue(type(prov) is location_provider)
        
    def test_of_compile_dump_realm_provider(self):
        comp = compiler()
        prov = comp._compile_dump_object_provider("REALM")
        self.assertTrue(type(prov) is realm_provider)
        
    def test_of_compile_dump_player_provider(self):
        comp = compiler()
        prov = comp._compile_dump_object_provider("PLAYER")
        self.assertTrue(type(prov) is player_provider)
        
    def test_of_compile_dump_object_provider(self):
        comp = compiler()
        prov = comp._compile_dump_object_provider("OBJECT")
        self.assertTrue(type(prov) is object_parameter_provider)
        
    def test_of_compile_dump_subject_provider(self):
        comp = compiler()
        prov = comp._compile_dump_object_provider("SUBJECT")
        self.assertTrue(type(prov) is subject_parameter_provider)
        
    def test_of_compile_dump_constant_provider(self):
        comp = compiler()
        prov = comp._compile_dump_object_provider("gold")
        self.assertTrue(type(prov) is constant_provider)
        
    
#-------------------------------------------------------------------------

