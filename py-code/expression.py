#-------------------------------------------------------------------------
# DREAM (C) WGan 2020
#-------------------------------------------------------------------------

""" Elements of expressions """

import                  random
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
            self._object = game._player._items.peek_item(name)
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
            self._object = game._player._items.get_item(name)
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

class item_parameter_provider(object_provider):

    """ provider allowing to act with an object mentioned in conditions as ITEM """
    
    def set_parameters(self, game, parameters):
        if not ("ITEM" in game._memo.keys()):
            raise error("ITEM was not selected. It must be specified in condition.")
        self._object = game._memo["ITEM"]
        self._name = self._object._name.get_name()
        
    def __str__(self):
        return "ITEM"
   
#-------------------------------------------------------------------------

class player_provider(object_provider):

    """ provider allowing to access to player object """
    
    def set_parameters(self, game, parameters):
        self._object = game._player
        self._name = "player"
        
    def __str__(self):
        return "PLAYER"
   
#-------------------------------------------------------------------------

class location_provider(object_provider):

    """ provider allowing to access to location object """
    
    def set_parameters(self, game, parameters):
        self._object = game._location
        self._name = "location"
        
    def __str__(self):
        return "LOCATION"
   
#-------------------------------------------------------------------------

class realm_provider(object_provider):

    """ provider allowing to access to realm object """
    
    def set_parameters(self, game, parameters):
        self._object = game._location._realm
        self._name = "realm"
        
    def __str__(self):
        return "REALM"
   
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

class expression_base(object):

    """ Base class for all nodes returning integer value """
    
    def value(self, game, parameters):
        return 0

#-------------------------------------------------------------------------

class constant_value_expression(expression_base):

    """ Just a simple integer value hold in the class to be used
        in expression calculation tree """
        
    def __init__(self, val):
        self._value = val
        
    def value(self, game, parameters):
        return self._value
        
    def __str__(self):
        return str(self._value)

#-------------------------------------------------------------------------

class sum_expression(expression_base):

    """ Sum of of its elements """
    
    def __init__(self, add, sub):
        self._add = add
        self._sub = sub
        
    def value(self, game, parameters):
        result = 0
        for val in self._add:
            result = result + val.value(game, parameters)
        for val in self._sub:
            result = result - val.value(game, parameters)
        return result
    
    def __str__(self):
        if self._add != []:
            result = str(self._add[0])
            if len(self._add) > 1:
                for i in range(1, len(self._add)):
                    result = result + " + " + str(self._add[i])
        else:
            result = ""
        for val in self._sub:
            result = result + " - " + str(val)
        return result.strip()

#-------------------------------------------------------------------------

class product_expression(expression_base):

    """ Product of its elements """
    
    def __init__(self, mul, div):
        self._mul = mul
        self._div = div
        
    def value(self, game, parameters):
        result = 1
        for val in self._mul:
            result = result * val.value(game, parameters)
        for val in self._div:
            result = result / val.value(game, parameters)
        return result
    
    def __str__(self):
        if self._mul == []:
            result = "1"
        else:
            result = str(self._mul[0])
        if len(self._mul) > 1:
            for i in range(1, len(self._mul)):
                result = result + " * " + str(self._mul[i])
        for val in self._div:
            result = result + " / " + str(val)
        return result
            
#-------------------------------------------------------------------------

class property_provider_base(expression_base):

    """ base class for all property providers. Stores name of the property """
    
    def __init__(self, name):
        self._property_name = name
        
    def _get_provider(self, game, parameters):
        return None
            
    def value(self, game, parameters):
        item = self._get_provider(game, parameters)
        if item is None:
            return 0
        return item._properties.get(self._property_name)
        
    def add(self, game, parameters, value):
        item = self._get_provider(game, parameters)
        if item is None:
            return
        item._properties.add(self._property_name, value)    
        
    def set(self, game, parameters, value):
        item = self._get_provider(game, parameters)
        if item is None:
            return
        item._properties.set(self._property_name, value)   
        
#-------------------------------------------------------------------------

class object_property_provider(property_provider_base):

    """ poperty provider of the item which was mentioned in user command """
    
    def _get_provider(self, game, parameters):
        provider = object_parameter_provider()
        provider.set_parameters(game, parameters)
        return provider.peek_object()  
    
    def __str__(self):
        return "OBJECT " + self._property_name
        
#-------------------------------------------------------------------------

class subject_property_provider(property_provider_base):

    """ poperty provider of the subject which was mentioned in user command """
    
    def _get_provider(self, game, parameters):
        provider = subject_parameter_provider()
        provider.set_parameters(game, parameters)
        return provider.peek_object()  
    
    def __str__(self):
        return "SUBJECT " + self._property_name
        
#-------------------------------------------------------------------------

class location_property_provider(property_provider_base):

    """ poperty provider of thecurrent location """
    
    def _get_provider(self, game, parameters):
        return game._location
        
    def __str__(self):
        return "LOCATION " + self._property_name
        
#-------------------------------------------------------------------------

class player_property_provider(property_provider_base):

    """ poperty provider of the player """
    
    def _get_provider(self, game, parameters):
        return game._player
        
    def __str__(self):
        return "PLAYER " + self._property_name
        
#-------------------------------------------------------------------------

class free_text_property_provider(property_provider_base):

    """ poperty provider of the subject which was mentioned in user command """
    
    def __init__(self, name):
        self._full_property_name = name
        self._property_name = name
            
    def _get_provider(self, game, parameters):
        object_name = self._full_property_name
        property_name = ""
        while True:
            # build name of the object and property
            pos = object_name.rfind(" ")
            if pos < 0:
                # raise error("Property '" + self._full_property_name + "' cannot be found. No matching object found around.")
                return None
            property_name = (object_name[pos:].strip() + " " + property_name).strip()
            object_name = object_name[0:pos].strip()
            obj = game._player._items.peek_item(object_name)
            if obj is None:
                obj = game._location._items.peek_item(object_name)
            if not (obj is None):
                self._property_name = property_name
                return obj
       
    def __str__(self):
        return self._full_property_name
        
#-------------------------------------------------------------------------

class item_property_provider(property_provider_base):

    """ poperty provider of the subject which was mentioned in user command """
    
    def _get_provider(self, game, parameters):
        if not ("ITEM" in game._memo.keys()):
            value = 0
            item = None
            for it in game._location._items._items:
                val = it._properties.get(self._property_name)
                if val > value:
                    item = it
                    value = val
            for it in game._player._items._items:
                val = it._properties.get(self._property_name)
                if val > value:
                    item = it
                    value = val
            if item is None:
                return None
            game._memo["ITEM"] = item
        return game._memo["ITEM"]
    
    def __str__(self):
        return "ITEM " + self._property_name
        
#-------------------------------------------------------------------------

class dice_expression(expression_base):

    """ Node returning integer value from the range 1..val, where val is 
        the result of inner expression """
        
    def __init__(self, inner_expression):
        self._inner_expression = inner_expression
        
    def value(self, game, parameters):
        val = self._inner_expression.value(game, parameters)
        val = random.randint(1, val)
        return val
        
    def __str__(self):
        if type(self._inner_expression) is constant_value_expression and self._inner_expression._value == 6:
            return "DICE"
        else:
            return "DICE " + str(self._inner_expression)
        
#-------------------------------------------------------------------------
