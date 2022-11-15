#-------------------------------------------------------------------------
# DREAM (C) WGan 2020
#-------------------------------------------------------------------------

""" Execution objects produces by compiler """

from errors      import error, \
                        break_action
from tools       import translator
from expression  import object_provider, \
                        object_parameter_provider, \
                        object_parameter_provider, \
                        subject_parameter_provider, \
                        constant_provider, \
                        new_object_provider, \
                        item_parameter_provider

#-------------------------------------------------------------------------

class dump_node(object):

    """ Execution element printing complete game state on the console """

    def __init__(self, provider):
        self._object_provider = provider
    
    def run(self, game, parameters):
        self._object_provider.set_parameters(game, parameters)
        object = self._object_provider.peek_object()
        game._console.dump(str(object).strip())
        
    def __str__(self):
        return "DUMP " + str(self._object_provider)
        
#-------------------------------------------------------------------------

class set_trace_node(object):

    """ Execution element switching on or off dumping execution trace 
        to console """

    def __init__(self, expression):
        self._expression = expression
        
    def run(self, game, parameters):
        val = self._expression.value(game, parameters)
        if val != 0:
            game._console.trace = True
            game._console.log("----- trace started")
        else:
            game._console.log("----- trace stopped")
            game._console.trace = False        
        
    def __str__(self):
        return "TRACE " + str(self._expression)
        
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
                raise break_action() # return
            text = text.replace("OBJECT", provider.get_name())
        if text.find("SUBJECT") >= 0:
            provider = subject_parameter_provider()
            provider.set_parameters(game, parameters)
            if provider._object is None:
                raise break_action() # return
            text = text.replace("SUBJECT", provider.get_name())
        if text.find("ITEM") >= 0:
            provider = item_parameter_provider()
            provider.set_parameters(game, parameters)
            if provider._object is None:
                raise break_action() # return
            text = text.replace("ITEM", provider.get_name())
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
        if game._player._items._items != []:
            game._console.write("You have:")
            for item in game._player._items._items:
                val = item._properties.get("value")
                if val > 0:
                    value = " (" + str(val) + ")"
                else:
                    value = ""
                game._console.write(" - " + item._description.get_short_text() + value)
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
        game._player._items.put_item(object)
        
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

class become_node(object):

    """ Immidatelly changes the player object to the specified one """
    
    def __init__(self, text):
        self._hero_type = text
    
    def run(self, game, parameters):
        hero = game._factory.get_object(self._hero_type)
        if type(hero).__name__ != "player":
            raise error("'" + self._hero_type + "' is not a character")
        game._player = hero
        
    def __str__(self):
        return "BECOME " + self._hero_type
        
#-------------------------------------------------------------------------

class modify_property_base(object):

    """ Execution node modyfying property of given object by the value provided
        by the expression. Base class fro both set and advance nodes """
        
    def __init__(self, property, expression):
        self._property = property
        self._expression = expression
          
#-------------------------------------------------------------------------

class advance_property_node(modify_property_base):

    """ Execution node modyfying property of given object by the value provided
        by the expression. """
        
    def run(self, game, parameters):
        val = self._expression.value(game, parameters)
        self._property.add(game, parameters, val)
        
    def __str__(self):
        return "MODIFY " + str(self._property) + \
               " BY " + str(self._expression)

#-------------------------------------------------------------------------

class set_property_node(modify_property_base):

    """ Execution node modyfying property of given object to the value provided
        by the expression. """
        
    def run(self, game, parameters):
        val = self._expression.value(game, parameters)
        self._property.set(game, parameters, val)
        
    def __str__(self):
        return "MODIFY " + str(self._property) + \
               " TO " + str(self._expression)

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
    
    def __init__(self, name, conditions, executables):
        self._name = name
        self._conditions = conditions
        self._executables = executables
        
    def try_execute(self, user_command, game):
        # check command text
        command_len = self._name.length_of_a_command_if_match(user_command)
        if command_len > 0:
            game._console.log(" - action '" + str(self) + "' match user command")
            parameters = user_command[command_len:].strip()
            # check command conditions
            for condition in self._conditions:
                if not condition.is_satisfied(game, parameters):
                    game._console.log("   - condition '" + str(condition) + "' faliled; command not executed")
                    return False
            # execute all orders
            game._console.log("   - all conditions satisfied;")
            for executable in self._executables:
                game._console.log("   - executing: " + str(executable))  
                executable.run(game, parameters)
            return True
        return False
        
    def __str__(self):
        ret = str(self._name)
        if self._conditions != []:
            conditions = "; ".join( [ str(condition) for condition in self._conditions ] )
            ret = ret + " WHEN " + conditions
        execs = "; ".join( [ str(command) for command in self._executables ] )
        ret = ret + " THEN " + execs
        return ret

#-------------------------------------------------------------------------

