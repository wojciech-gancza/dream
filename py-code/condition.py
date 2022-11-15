#-------------------------------------------------------------------------
# DREAM (C) WGan 2020
#-------------------------------------------------------------------------

""" conditions - usually a relation between two expressions """

#-------------------------------------------------------------------------

class condition_base(object):

    """ base of conditions - just interface to all condition nodes """
    
    def is_satisfied(self, game, parameters):
        return False

#-------------------------------------------------------------------------

class comparison_condition(condition_base):

    """ base of conditions - just interface to all condition nodes """
    
    def __init__(self, left, right):
        self._left = left
        self._right = right
    
    def is_satisfied(self, game, parameters):
        return False
        
#-------------------------------------------------------------------------

class comparision_equal_condition(comparison_condition):

    def is_satisfied(self, game, parameters):
        return self._left.value(game, parameters) == self._right.value(game, parameters)
        
    def __str__(self):
        return str(self._left) + " = " + str(self._right)

#-------------------------------------------------------------------------

class comparision_not_equal_condition(comparison_condition):

    def is_satisfied(self, game, parameters):
        return self._left.value(game, parameters) != self._right.value(game, parameters)
        
    def __str__(self):
        return str(self._left) + " != " + str(self._right)

#-------------------------------------------------------------------------

class comparision_greater_condition(comparison_condition):

    def is_satisfied(self, game, parameters):
        return self._left.value(game, parameters) > self._right.value(game, parameters)
        
    def __str__(self):
        return str(self._left) + " > " + str(self._right)

#-------------------------------------------------------------------------

class comparision_greater_or_equal_condition(comparison_condition):

    def is_satisfied(self, game, parameters):
        return self._left.value(game, parameters) >= self._right.value(game, parameters)
        
    def __str__(self):
        return str(self._left) + " >= " + str(self._right)

#-------------------------------------------------------------------------

class comparision_less_condition(comparison_condition):

    def is_satisfied(self, game, parameters):
        return self._left.value(game, parameters) < self._right.value(game, parameters)
        
    def __str__(self):
        return str(self._left) + " < " + str(self._right)

#-------------------------------------------------------------------------

class comparision_less_or_equal_condition(comparison_condition):

    def is_satisfied(self, game, parameters):
        return self._left.value(game, parameters) <= self._right.value(game, parameters)
         
    def __str__(self):
        return str(self._left) + " <= " + str(self._right)
       
#-------------------------------------------------------------------------
