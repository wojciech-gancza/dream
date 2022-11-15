#-------------------------------------------------------------------------
# DREAM (C) WGan 2020
#-------------------------------------------------------------------------

""" Processor is a module which process and changes state of the game, by
    processing commands on given items """

from errors      import error, \
                        break_action
from tools       import translator

#-------------------------------------------------------------------------

class object_provider(object):

    """ object provider is used as parameter of dL command. It can be 
        attached to execution node which need object as its parameter.
        Because it can be differenly used, it can contain object (if 
        mentioned object is available, however it can also keep possible 
        object names """

    def __init__(self):
        self._name = ""
        self._object = None
        self._already_taken = False
        
    def set_accessible_object_name(self, name, game):
        self._already_taken = False
        if type(name) == list:
            for single_name in name:
                self.set_accessible_object_name(single_name, game)
                if not self._object is None:
                    return
            if self._object is None:
                self._name = name
        else:
            self._object = game._pocket.peek_item(name)
            if self._object is None:
                self._object = game._location._items.peek_item(name)
            if self._object is None:
                self._name = name
            else:
                self._name = self._object._name.get_name()
       
    def get_name(self):
        if type(self._name) is list:
            return self._name[0]
        return self._name

    def peek_object(self):
        return self._object

    def take_object(self, game):
        if not self._already_taken:
            name = self.get_name()
            self._object = game._pocket.get_item(name)
            if self._object is None:
                self._object = game._location._items.get_item(name)
            self._already_taken = True
        return self._object

#-------------------------------------------------------------------------

class object_parameter_provider(object_provider):
    
    """ Provider taking object from the user command parameters
        This provider takes object located at the end of the 
        command. If parameters contain more words, all possiblities
        of command names will be used. Possiblities are taken 
        cutting begin of parameterts """
    
    def set_parameters(self, game, parameters):
        names = [parameters]
        pos = parameters.find(" ")
        while pos >= 0:
            parameters = parameters[pos:].strip()
            names.append(parameters)
            pos = parameters.find(" ")
        self.set_accessible_object_name(names, game)
        
    def __str__(self):
        return "OBJECT"
        
#-------------------------------------------------------------------------

class subject_parameter_provider(object_provider):

    """ Provider taking subject from the user command parameters
        This provider takes subject located at the begining of the 
        command. If parameters contain more words, all possiblities
        of command names will be used. Possiblities are taken 
        cutting end of parameterts """
    
    def set_parameters(self, game, parameters):
        names = [parameters]
        pos = parameters.rfind(" ")
        while pos >= 0:
            parameters = parameters[0:pos].strip()
            names.append(parameters)
            pos = parameters.rfind(" ")
        self.set_accessible_object_name(names, game)
        
    def __str__(self):
        return "SUBJECT"
        
#-------------------------------------------------------------------------

class constant_provider(object_provider):
    
    """ provider returning object wirh selected name """
    
    def __init__(self, name):
        self._constant_name = name
    
    def set_parameters(self, game, parameters):
        self.set_accessible_object_name(self._constant_name, game)

    def __str__(self):
        return self._constant_name
        
#-------------------------------------------------------------------------

class new_object_provider(object_provider):

    """ provider decorator always returining new object """

    def __init__(self, subprovider):
        self._child_provider = subprovider
        
    def set_parameters(self, game, parameters):
        self._child_provider.set_parameters(game, parameters)
        self._name = self._child_provider.get_name()
        try:
            self._object = game._factory.get_object(self._name)
        except:
            self._object = None
        self._already_taken = True

    def __str__(self):
        return "NEW " + str(self._child_provider)
        
#-------------------------------------------------------------------------

class exit_node(object):

    """ Execution element stopping the execution """

    def run(self, game, parameters):
        game.stop()
        
    def __str__(self):
        return "EXIT"
        
#-------------------------------------------------------------------------

class translating_text_node(object):

    """ node with text where keywords are translated """
    
    def __init__(self, text):
        self._text = text
        
    def _get_text(self, game, parameters):
        text = self._text
        if text.find("OBJECT") >= 0:
            provider = object_parameter_provider()
            provider.set_parameters(game, parameters)
            if provider._object is None:
                return
            text = text.replace("OBJECT", provider.get_name())
        if text.find("SUBJECT") >= 0:
            provider = subject_parameter_provider()
            provider.set_parameters(game, parameters)
            if provider._object is None:
                return
            text = text.replace("SUBJECT", provider.get_name())
        return text

#-------------------------------------------------------------------------

class print_text_node(translating_text_node):

    """ Execution element printing constant text """
   
    def run(self, game, parameters):
        game._console.write( self._get_text(game, parameters ) )
        
    def __str__(self):
        return "PRINT " + self._text
       
#-------------------------------------------------------------------------

class look_around_node(object):

    """ Execution element printing long description of the location """
    
    def run(self, game, parameters):
        game._console.write( game._location._description.get_long_text() )
        if game._location._items._items != []:
            game._console.write("You notice:")
            for item in game._location._items._items:
                game._console.write(" - " + item._description.get_short_text())
        
    def __str__(self):
        return "LOOK"

#-------------------------------------------------------------------------

class change_location_node(object):

    """ Execution element changes current location """
    
    def __init__(self, location_name):
        self._location_name = location_name
    
    def run(self, game, parametrs):
        game._location = game._factory.get_object( self._location_name )
        game._console.write("You are in " + game._location._name.get_name())
        game._console.write(game._location._description.get_short_text())
        
    def __str__(self):
        return "GOTO " + self._location_name

#-------------------------------------------------------------------------

class inventory_node(object):

    """ Lists all items in player inventory """
    
    def run(self, game, parametrs):       
        if game._pocket._items != []:
            game._console.write("You have:")
            for item in game._pocket._items:
                game._console.write(" - " + item._description.get_short_text())
        else:
            game._console.write("You have nothing.")
            
    def __str__(self):
        return "POCKET"

#-------------------------------------------------------------------------

class object_manipulating_node(object):

    """ Base class fot operations working on single item. This
        class have common code for TAKE, DROP, INVENTORY and other
        similar nodes """

    def __init__(self, object_provider):
        self._object_provider = object_provider
        
    def run(self, game, parameters):
        self._object_provider.set_parameters(game, parameters)
        object = self._object_provider.peek_object()
        if object is None:
            name = self._object_provider._name
            if type(name) is list: 
                name = name[0]
            if name == "":
                game._console.write("Be more specific")
            else:
                game._console.write("I see no " + self._object_provider.get_name())
            return
        self.process_object(game)
   
#-------------------------------------------------------------------------

class examine_node(object_manipulating_node):

    """ Shows description of an item available at location of players pocket """
    
    def process_object(self, game):
        object = self._object_provider.peek_object()
        game._console.write(object._description.get_long_text())
        
    def __str__(self):
        return "EXAMINE " + str(self._object_provider)

#-------------------------------------------------------------------------

class take_item_node(object_manipulating_node):

    """ gets available item and places it in player inventory """
    
    def process_object(self, game):
        object = self._object_provider.take_object(game)
        game._pocket.put_item(object)
        
    def __str__(self):
        return "TAKE " + str(self._object_provider)
            
#-------------------------------------------------------------------------

class drop_item_node(object_manipulating_node):

    """ gets available item and places it in player inventory """
    
    def process_object(self, game):
        object = self._object_provider.take_object(game)
        game._location._items.put_item(object)

    def __str__(self):
        return "DROP " + str(self._object_provider)
        
#-------------------------------------------------------------------------

class delete_item_node(object_manipulating_node):

    """ gets available item and places it in player inventory """
    
    def process_object(self, game):
        object = self._object_provider.take_object(game)

    def __str__(self):
        return "DEL " + str(self._object_provider)       
        
#-------------------------------------------------------------------------

class execute_command_node(translating_text_node):

    """ executes the text which is parameter """
    
    def run(self, game, parameters):
        if not game.execute( self._get_text(game, parameters ) ):
            raise break_action()
        
    def __str__(self):
        return "EXEC " + self._text
        
#-------------------------------------------------------------------------

class command_name(object):

    """ The name set of command. """
    
    def __init__(self, names):
        self._possibilities = names
        
    def length_of_a_command_if_match(self, command_text):
        for possibility in self._possibilities:
            possibility_len = len(possibility)
            command_len = len(command_text)
            if command_text[0:possibility_len] == possibility:
                if command_len == possibility_len or command_text[possibility_len] == " ":
                    return possibility_len
        return 0
        
    def __str__(self):
        return "; ".join(self._possibilities)

#-------------------------------------------------------------------------

class command(object):
    
    """ Command ready to execute. Contain all elements needed to execute 
        command including check of user command match. """
    
    def __init__(self, name, executables):
        self._name = name
        self._executables = executables
        
    def try_execute(self, user_command, game):
        command_len = self._name.length_of_a_command_if_match(user_command)
        if command_len > 0:
            parameters = user_command[command_len:].strip()
            for executable in self._executables:
                executable.run(game, parameters)
            return True
        return False
        
    def __str__(self):
        ret = str(self._name)
        execs = "; ".join( [ str(command) for command in self._executables ] )
        ret = ret + " THEN " + execs
        return ret

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
        commands = [ self._compile_single_order(single_order) for single_order in elements[2] ]
        return command(names, commands)

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
        else:
            return constant_provider(text)
        
#-------------------------------------------------------------------------

