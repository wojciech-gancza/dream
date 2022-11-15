#-------------------------------------------------------------------------
# DREAM (C) WGan 2020
#-------------------------------------------------------------------------

""" compiler allow compilation of actions """

from errors      import error, \
                        break_action
from tools       import translator
from expression  import object_provider, \
                        object_parameter_provider, \
                        object_parameter_provider, \
                        subject_parameter_provider, \
                        item_parameter_provider, \
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
                        dice_expression, \
                        player_provider, \
                        location_provider, \
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
                        advance_property_node, \
                        set_property_node, \
                        dump_node, \
                        set_trace_node
from condition   import comparision_less_or_equal_condition, \
                        comparision_greater_or_equal_condition, \
                        comparision_not_equal_condition, \
                        comparision_less_condition, \
                        comparision_greater_condition, \
                        comparision_equal_condition

#-------------------------------------------------------------------------

class compiler(object):

    """ this is potential command - command which can be attached to the
        location, item, player or realm """

    def __init__(self):
        pass
        
    def compile(self, command_definition):
        elements = self._decompose_order(command_definition)
        if elements[0] == []:
            raise error("At least one name should be attached to action")
        if elements[2] == []:
            raise error("At least one statement should be attached to action")
        names = command_name( elements[0] )
        conditions = [ self._compile_single_condition(single_condition) for single_condition in elements[1] ]
        commands = [ self._compile_single_order(single_order) for single_order in elements[2] ]
        return command(names, conditions, commands)

    def _split_on_word(self, haystack, nedle):
        parts = haystack.split(nedle)
        if len(parts) > 2:
            raise error("Keyword '" + nedle + "' can be used only once in command")
        if len(parts) == 1:
            parts.append("")
        return parts
        
    def _decompose_list(self, text):
        if text.strip() == "":
            return []
        else:
            return [ element.strip() for element in text.split(";") ]
        
    def _decompose_order(self, text):
        result = [[],[],[]]
        parts = self._split_on_word(text, "THEN")
        result[2] = self._decompose_list(parts[1])
        parts = self._split_on_word(parts[0], "WHEN")
        result[1] = self._decompose_list(parts[1])
        result[0] = self._decompose_list(parts[0])
        return result
        
    def _compile_single_order(self, text):
        if self._is_it_command(text, "EXIT"):
            return self._compile_exit_node(text)
        if self._is_it_command(text, "PRINT"):
            return self._compile_print_node(text)
        if self._is_it_command(text, "GOTO"):
            return self._compile_goto_node(text)
        if self._is_it_command(text, "LOOK"):
            return self._compile_look_around_node(text)
        if self._is_it_command(text, "POCKET"):
            return self._compile_inventory_node(text)
        if self._is_it_command(text, "EXAMINE"):
            return self._compile_examine_node(text)
        if self._is_it_command(text, "TAKE"):
            return self._compile_take_node(text)
        if self._is_it_command(text, "DROP"):
            return self._compile_drop_node(text)
        if self._is_it_command(text, "DEL"):
            return self._compile_del_item_node(text)
        if self._is_it_command(text, "EXEC"):
            return self._compile_exec_node(text)
        if self._is_it_command(text, "BECOME"):
            return self._compile_become_node(text)
        if self._is_it_command(text, "MODIFY"):
            return self._compile_modify_node(text)
        if self._is_it_command(text, "DUMP"):
            return self._compile_dump_node(text)
        if self._is_it_command(text, "TRACE"):
            return self._compile_trace_node(text)
        raise error("Unknown command: '" + text + "'")
            
    def _is_it_command(self, command_text, command_name):
        if command_text.find(command_name) >= 0:
            return True
        else:
            return False
            
    def _check_no_parameters(self, command_text, keyword_text):
        if command_text != keyword_text:
            raise error(keyword_text + " command must stay alone. It does not accept parameters") 
    
    def _get_single_after_parameter(self, command_text, keyword_text):
        keyword_len = len(keyword_text)
        if command_text[0:keyword_len] != keyword_text:
            raise error(keyword_text + "  must start with " + keyword_text + " command.")
        return command_text[keyword_len:].strip()
    
    def _compile_exit_node(self, text):
        self._check_no_parameters(text, "EXIT") 
        return exit_node()
        
    def _compile_print_node(self, text):
        text = self._get_single_after_parameter(text, "PRINT")
        return print_text_node(text)
        
    def _compile_goto_node(self, text):
        text = self._get_single_after_parameter(text, "GOTO")
        return change_location_node(text)
        
    def _compile_look_around_node(self, text):
        self._check_no_parameters(text, "LOOK") 
        return look_around_node()
        
    def _compile_inventory_node(self, text):
        self._check_no_parameters(text, "POCKET") 
        return inventory_node()
        
    def _compile_examine_node(self, text):
        text = self._get_single_after_parameter(text, "EXAMINE")
        data_provider = self._compile_object_provider(text)
        return examine_node(data_provider)
        
    def _compile_take_node(self, text):
        text = self._get_single_after_parameter(text, "TAKE")
        data_provider = self._compile_object_provider(text)
        return take_item_node(data_provider)
        
    def _compile_drop_node(self, text):
        text = self._get_single_after_parameter(text, "DROP")
        data_provider = self._compile_object_provider(text)
        return drop_item_node(data_provider)
        
    def _compile_del_item_node(self, text):
        text = self._get_single_after_parameter(text, "DEL")
        data_provider = self._compile_object_provider(text)
        return delete_item_node(data_provider)
        
    def _compile_exec_node(self, text):
        text = self._get_single_after_parameter(text, "EXEC")
        return execute_command_node(text)
        
    def _compile_become_node(self, text):
        text = self._get_single_after_parameter(text, "BECOME")
        return become_node(text)
        
    def _compile_modify_node(self, text):
        text = self._get_single_after_parameter(text, "MODIFY")
        if self._is_it_command(text, "BY"):
            texts = text.split("BY")
            if len(texts) != 2:
                raise error("MODIFY must have format: <property> BY <expression>")
            property = self._compile_property_provider(texts[0].strip())
            expression = self._compile_single_expression(texts[1].strip())
            return advance_property_node(property, expression)
        if self._is_it_command(text, "TO"):
            texts = text.split("TO")
            if len(texts) != 2:
                raise error("MODIFY must have format: <property> TO <expression>")
            property = self._compile_property_provider(texts[0].strip())
            expression = self._compile_single_expression(texts[1].strip())
            return set_property_node(property, expression)
        else:
            raise error("MODIFY must have format: <property> BY/TO <expression>")
        
    def _compile_dump_node(self, text):
        text = self._get_single_after_parameter(text, "DUMP") 
        if text == "":
            raise error("DUMP need parameter - object to dump") 
        provider = self._compile_dump_object_provider(text)
        return dump_node(provider)
        
    def _compile_trace_node(self, text):
        text = self._get_single_after_parameter(text, "TRACE")
        if text == "":
            raise error("TRACE need parameter - value or expression") 
        expression = self._compile_single_expression(text)
        return set_trace_node(expression)
        
    def _compile_object_provider(self, text):
        if self._is_it_command(text, "NEW"):
            text = self._get_single_after_parameter(text, "NEW")
            subprovider = self._compile_object_provider(text)
            return new_object_provider(subprovider)
        elif self._is_it_command(text, "SUBJECT"):
            self._check_no_parameters(text, "SUBJECT")
            return subject_parameter_provider()
        elif self._is_it_command(text, "OBJECT"):
            self._check_no_parameters(text, "OBJECT")
            return object_parameter_provider()
        elif self._is_it_command(text, "ITEM"):
            self._check_no_parameters(text, "ITEM")
            return item_parameter_provider()
        else:
            return constant_provider(text)
    
    def _compile_dump_object_provider(self, text):
        if self._is_it_command(text, "LOCATION"):
            self._check_no_parameters(text, "LOCATION")
            return location_provider()
        if self._is_it_command(text, "PLAYER"):
            self._check_no_parameters(text, "PLAYER")
            return player_provider()
        if self._is_it_command(text, "REALM"):
            self._check_no_parameters(text, "REALM")
            return realm_provider()
        if self._is_it_command(text, "SUBJECT"):
            self._check_no_parameters(text, "SUBJECT")
            return subject_parameter_provider()
        if self._is_it_command(text, "OBJECT"):
            self._check_no_parameters(text, "OBJECT")
            return object_parameter_provider()
        return constant_provider(text)
    
    def _compile_single_condition(self, text):
        if self._is_it_command(text, "<="):
            return self._compare_less_or_equal(text)
        if self._is_it_command(text, ">="):
            return self._compare_greater_or_equal(text)
        if self._is_it_command(text, "!="):
            return self._compare_not_equal(text)
        if self._is_it_command(text, "<"):
            return self._compare_less(text)
        if self._is_it_command(text, ">"):
            return self._compare_greater(text)
        if self._is_it_command(text, "="):
            return self._compare_equal(text)
        raise error("'" + text + "' is not a condition")
       
    def _get_two_expressions(self, text, relation):
        expressions = text.split(relation)
        if len(expressions) != 2:
            raise error ("'" + text + "' cannot be separated into two expressions")
        if expressions[0] == "":
            raise error ("Left expression cannot be empty")
        if expressions[1] == "":
            raise error ("Right expression cannot be empty")
        return [self._compile_single_expression(expression.strip()) for expression in expressions]
        
    def _compare_less_or_equal(self, text):
        expressions = self._get_two_expressions(text, "<=")
        return comparision_less_or_equal_condition(expressions[0], expressions[1])
    
    def _compare_greater_or_equal(self, text):
        expressions = self._get_two_expressions(text, ">=")
        return comparision_greater_or_equal_condition(expressions[0], expressions[1])
    
    def _compare_not_equal(self, text):
        expressions = self._get_two_expressions(text, "!=")
        return comparision_not_equal_condition(expressions[0], expressions[1])
    
    def _compare_less(self, text):
        expressions = self._get_two_expressions(text, "<")
        return comparision_less_condition(expressions[0], expressions[1])
    
    def _compare_greater(self, text):
        expressions = self._get_two_expressions(text, ">")
        return comparision_greater_condition(expressions[0], expressions[1])
    
    def _compare_equal(self, text):
        expressions = self._get_two_expressions(text, "=")
        return comparision_equal_condition(expressions[0], expressions[1])
    
    def _split_on_operations(self, text, separator1, separator2):
        splitting = text
        result1 = []
        result2 = []
        while text != "":
            pos1 = text.rfind(separator1)
            pos2 = text.rfind(separator2)
            if pos1 > pos2:
                lpart = text[pos1+len(separator1):].strip()
                if lpart == "":
                    raise error("Expression '" + splitting + "' is not valid expression")
                result1.append( lpart )
                text = text[0:pos1].strip()
                if text == "" and separator1 != "-":
                    raise error("Expression '" + splitting + "' is not valid expression")
            elif pos1 < pos2:
                lpart = text[pos2+len(separator2):].strip()
                if lpart == "":
                    raise error("Expression '" + splitting + "' is not valid expression")
                result2.append( lpart )
                text = text[0:pos2].strip()
                if text == "" and separator2 != "-":
                    raise error("Expression '" + splitting + "' is not valid expression")
            else:
                result1.append(text)
                text = "";
        return (result1, result2);
    
    def _is_unit_after_split(self, result1, result2):
        if result2 != []:
            return False
        if len(result1) != 1:
            return False
        return True
    
    def _compile_single_expression(self, text):
        add, substract = self._split_on_operations(text, "+", "-")
        if self._is_unit_after_split(add, substract):
            return self._compile_multiplication(add[0])
        else:
            add = [self._compile_multiplication(part) for part in add]
            substract = [self._compile_multiplication(part) for part in substract]
            return sum_expression(add, substract)
            
    def _compile_multiplication(self, text):
        mul, div = self._split_on_operations(text, "*", "/")
        if self._is_unit_after_split(mul, div):
            return self._compile_simple_expression(mul[0])
        else:
            mul = [self._compile_multiplication(part) for part in mul]
            div = [self._compile_multiplication(part) for part in div]
            return product_expression(mul, div)
    
    def _compile_simple_expression(self, text):
        if text.find("DICE") == 0:
            if len(text) == 4:
                expr = constant_value_expression(6)
            else:
                expr = self._compile_simple_expression(text[4:].strip())
            return dice_expression(expr)
        try:
            if text == "":
                raise error("Expression cannot be empty")
            constant = int(text)
            return constant_value_expression(constant)
        except Exception as e:
            return self._compile_property_provider(text)
            
    def _compile_property_provider(self, text):
        if self._is_it_command(text, "OBJECT"):
            text = self._get_single_after_parameter(text, "OBJECT")
            if text == "":
                raise error("Property name must be specified.")
            return object_property_provider(text)
        if self._is_it_command(text, "SUBJECT"):
            text = self._get_single_after_parameter(text, "SUBJECT")
            if text == "":
                raise error("Property name must be specified.")
            return subject_property_provider(text)
        if self._is_it_command(text, "LOCATION"):
            text = self._get_single_after_parameter(text, "LOCATION")
            if text == "":
                raise error("Property name must be specified.")
            return location_property_provider(text)
        if self._is_it_command(text, "PLAYER"):
            text = self._get_single_after_parameter(text, "PLAYER")
            if text == "":
                raise error("Property name must be specified.")
            return player_property_provider(text)
        if self._is_it_command(text, "ITEM"):
            text = self._get_single_after_parameter(text, "ITEM")
            if text == "":
                raise error("Property name must be specified.")
            return item_property_provider(text)
        if text.find(" ") < 0:
            raise error("At least two words are needed to specify item nad property names.")
        return free_text_property_provider(text)
        
#-------------------------------------------------------------------------

