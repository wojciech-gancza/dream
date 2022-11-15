#-------------------------------------------------------------------------
# DREAM (C) WGan 2020
#-------------------------------------------------------------------------

""" Main data structures of RPG environment. """

from tools       import translator
from compiler    import command, \
                        exit_node, \
                        command_name

#-------------------------------------------------------------------------

class description(object):

    """ Description of game element. Description consist on long and
        short description. Long description is shown when player
        examines object. Short is used when elements are enumerated
        or when item is recalled """

    def __init__(self):
        self._short_text = translator.make_nonempty_string("")
        self._long_text = translator.make_nonempty_string("")

    def get_short_text(self):
        return self._short_text

    def get_long_text(self):
        return self._long_text

    def set_description(self, short_text, long_text):
        self._short_text = translator.make_nonempty_string(short_text)
        self._long_text = translator.make_nonempty_string(long_text)
        
    def __str__(self):
        return "[description]\n" + self.get_short_text() + "\n" + self.get_long_text() + "\n"

#-------------------------------------------------------------------------

class name(object):

    """ Name os the game name of an object. It has main name and set of
        alternative names which could also be used in orders """
    
    def __init__(self):
        self._main_name = translator.make_nonempty_string("")
        self._alternative_names = []
        
    def set_names(self, all_names):
        if all_names == []:
            self._main_name = translator.make_nonempty_string("")
            self._alternative_names = []
        else:
            self._main_name = all_names[0]
            self._alternative_names = all_names[1:]
            
    def get_name(self):
        return self._main_name
        
    def __str__(self):
        text = "[name]\n" + self._main_name + "\n";
        for name in self._alternative_names:
            text = text + name + "\n"
        return text
        
#-------------------------------------------------------------------------

class property(object):
    
    """ Property is a value which is used in the game for various purposes 
        like stats, current scores, health-like properties and any other 
        which can be changed 
        Each property is integer number from range 0..9999. Properties cannot
        be set, but can be changed by given integer value. When property
        value after modification is out of bound - it is set to the bound.
        Uninitialized properties have value = 0 """
        
    MAXIMAL_VALUE = 9999
    MINIMAL_VALUE = 0
    DEFAULT_VALUE = 0
    
    def __init__(self):
        self._value = property.DEFAULT_VALUE
        
    def add(self, value):
        self._value = self._value + value;
        if self._value < property.MINIMAL_VALUE:
            self._value = property.MINIMAL_VALUE
        elif self._value > property.MAXIMAL_VALUE:
            self._value = property.MAXIMAL_VALUE
       
    def get(self):
        return self._value
        
    def __str__(self):
        return str(self._value)

#-------------------------------------------------------------------------
        
class properties(object):
    
    """ Properties is a set of named properties implemented in dictionary.
        Uninitialized properties have default value """
        
    def __init__(self):
        self._properties = { }
        
    def add(self, name, value):
        if not name in self._properties.keys():
            self._properties[name] = property()
        self._properties[name].add(value)
        
    def get(self, name):
        if name in self._properties.keys():
            return self._properties[name].get()
        else:
            return property().get()
        
    def __str__(self):
        text = "[properties]\n"
        for key, value in self._properties.items():
            text = text + key + " = " + str(value) + "\n"
        return text
        
#-------------------------------------------------------------------------

class actions(object):
    
    """ group of possible orders which can be attached to any game 
        entity to make this command available """
    
    def __init__(self):
        self._actions = []
        
    def add_action(self, action):
        self._actions.append(action)
        
    def try_execute(self, command_text, game):
        for action in self._actions:
            if action.try_execute(command_text, game):
                return True
        return False
        
    def __str__(self):
        text = "[actions]\n"
        for action in self._actions:
            text = text + str(action) + "\n"
        return text
        
#-------------------------------------------------------------------------

class item(object):

    """ Item. This is the abstraction of objects which could be found, 
        taken, crafted, carried, transformed, traded or used during the 
        game Item must have:
      - name - because it must be possibility to mention it in command
      - properties - makes item usefull. Some stats can be cumulated by 
        carrying given items, 
      - description - containing a view and hints to figure out how it
        cab ne used
      - special actions - actions typical for this item, or actions in 
        which it might be used with special, different result """

    def __init__(self):
        self._name = name()
        self._properties = properties()
        self._description = description()

    def __str__(self):
        return "[type]\nlocation\n\n" + \
            str(self._name) + "\n" + \
            str(self._properties) + "\n" + \
            str(self._description)

#-------------------------------------------------------------------------

class realm(object):

    """ Common behaviour of group of location. Allow to define common
        actions not repeating them each time the ne locations is 
        developed """

    def __init__(self):
        self._name = name()
        self._actions = actions()

    def __str__(self):
        return "[type]\nrealm\n\n" + \
            str(self._name) + "\n" + \
            str(self._actions)
            
#-------------------------------------------------------------------------

class location(object):

    """ Location where the player can be.  """

    def __init__(self):
        self._name = name()
        self._realm = None
        self._properties = properties()
        self._description = description()
        self._actions = actions()

    def __str__(self):
        result = "[type]\nlocation\n\n" + \
            str(self._name) + "\n"
        if not self._realm is None:
            result = result + "[realm]\n" + self._realm._name.get_name() + "\n\n"
        return result + \
            str(self._properties) + "\n" + \
            str(self._description) + "\n" + \
            str(self._actions)
            
    def try_execute(self, command_text, game):
        if not self._actions.try_execute(command_text, game):
            if not self._realm is None:
                return self._realm._actions.try_execute(command_text, game)
        return True
            
#-------------------------------------------------------------------------
       

