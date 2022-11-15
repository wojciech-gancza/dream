#-------------------------------------------------------------------------
# DREAM (C) WGan 2020
#-------------------------------------------------------------------------

""" Processor is a module which process and changes state of the game, by
    processing commands on given items """

from errors      import error

#-------------------------------------------------------------------------

class exit_node(object):

    """ Execution element stopping the execution """

    def run(self, game):
        game.stop()
        
    def __str__(self):
        return "EXIT"
        
#-------------------------------------------------------------------------

class print_text_node(object):

    """ Execution element printing constant text """
   
    def __init__(self, text):
        self._text = text

    def run(self, game):
        game._console.write( self._text )
        
    def __str__(self):
        return "PRINT " + self._text
       
#-------------------------------------------------------------------------

class look_around_node(object):

    """ Execution element printing long description of the location """
    
    def run(self, game):
        game._console.write( game._location._description.get_long_text() )
        
    def __str__(self):
        return "LOOK"

#-------------------------------------------------------------------------

class change_location_node(object):

    """ Execution element changes current location """
    
    def __init__(self, location_name):
        self._location_name = location_name
    
    def run(self, game):
        game._location = game._factory.get_object( self._location_name )
        game._console.write("You are in " + game._location._name.get_name())
        game._console.write(game._location._description.get_short_text())
        
    def __str__(self):
        return "GOTO " + self._location_name;

#-------------------------------------------------------------------------

class command_name(object):

    """ The name set of command. """
    
    def __init__(self, names):
        self._possibilities = names
        
    def is_that_a_command(self, command_text):
        for possibility in self._possibilities:
            if command_text == possibility:
                return True
        return False
        
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
        if self._name.is_that_a_command(user_command):
            for executable in self._executables:
                executable.run(game)
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
        if elements[3] == []:
            raise error("At least one statement should be attached to action")
        names = command_name( elements[0] )
        commands = [ self._compile_single_order(single_order) for single_order in elements[3] ]
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
        result = [[],[],[],[]]
        parts = self._split_on_word(text, "THEN")
        result[3] = self._decompose_list(parts[1])
        parts = self._split_on_word(parts[0], "WHEN")
        result[2] = self._decompose_list(parts[1])
        parts = self._split_on_word(parts[0], "WITH")
        result[0] = self._decompose_list(parts[0])
        result[1] = self._decompose_list(parts[1])
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
        
#-------------------------------------------------------------------------

