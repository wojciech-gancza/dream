#-------------------------------------------------------------------------
# DREAM (C) WGan 2020
#-------------------------------------------------------------------------

""" Tests of condition calculations """

import                      unittest

from condition      import  condition_base, \
                            comparison_condition, \
                            comparision_equal_condition, \
                            comparision_not_equal_condition, \
                            comparision_greater_condition, \
                            comparision_greater_or_equal_condition, \
                            comparision_less_condition, \
                            comparision_less_or_equal_condition
from expression     import  constant_value_expression

#-------------------------------------------------------------------------

class Test_condition_base(unittest.TestCase):

    def test_of_is_satisfied(self):
        cond = condition_base()
        self.assertFalse(cond.is_satisfied(None, None))

#-------------------------------------------------------------------------

class Test_comparison_condition(unittest.TestCase):

    def test_of_is_satisfied(self):
        cond = comparison_condition(constant_value_expression(5), constant_value_expression(7))
        self.assertEqual(cond._left.value(None, None), 5)
        self.assertEqual(cond._right.value(None, None), 7)
        
#-------------------------------------------------------------------------

class Test_comparision_equal_condition(unittest.TestCase):

    def test_of_is_satisfied(self):
        val1 = constant_value_expression(314)
        val2 = constant_value_expression(271)
        val3 = constant_value_expression(314)
        cond1 = comparision_equal_condition(val1, val2)
        self.assertFalse(cond1.is_satisfied(None, None))
        cond2 = comparision_equal_condition(val1, val3)
        self.assertTrue(cond2.is_satisfied(None, None))
        cond3 = comparision_equal_condition(val2, val3)
        self.assertFalse(cond3.is_satisfied(None, None))
        
    def test_of_converting_to_string(self):
        val1 = constant_value_expression(314)
        val2 = constant_value_expression(271)
        cond = comparision_equal_condition(val1, val2)
        self.assertEqual(str(cond), "314 = 271")

#-------------------------------------------------------------------------

class Test_comparision_not_equal_condition(unittest.TestCase):

    def test_of_is_satisfied(self):
        val1 = constant_value_expression(314)
        val2 = constant_value_expression(271)
        val3 = constant_value_expression(314)
        cond1 = comparision_not_equal_condition(val1, val2)
        self.assertTrue(cond1.is_satisfied(None, None))
        cond2 = comparision_not_equal_condition(val1, val3)
        self.assertFalse(cond2.is_satisfied(None, None))
        cond3 = comparision_not_equal_condition(val2, val3)
        self.assertTrue(cond3.is_satisfied(None, None))
        
    def test_of_converting_to_string(self):
        val1 = constant_value_expression(314)
        val2 = constant_value_expression(271)
        cond = comparision_not_equal_condition(val1, val2)
        self.assertEqual(str(cond), "314 != 271")

#-------------------------------------------------------------------------

class Test_comparision_greater_condition(unittest.TestCase):

    def test_of_is_satisfied(self):
        val1 = constant_value_expression(314)
        val2 = constant_value_expression(271)
        val3 = constant_value_expression(314)
        cond1 = comparision_greater_condition(val1, val2)
        self.assertTrue(cond1.is_satisfied(None, None))
        cond2 = comparision_greater_condition(val1, val3)
        self.assertFalse(cond2.is_satisfied(None, None))
        cond3 = comparision_greater_condition(val2, val3)
        self.assertFalse(cond3.is_satisfied(None, None))
        
    def test_of_converting_to_string(self):
        val1 = constant_value_expression(314)
        val2 = constant_value_expression(271)
        cond = comparision_greater_condition(val1, val2)
        self.assertEqual(str(cond), "314 > 271")

#-------------------------------------------------------------------------

class Test_comparision_greater_or_equal_condition(unittest.TestCase):

    def test_of_is_satisfied(self):
        val1 = constant_value_expression(314)
        val2 = constant_value_expression(271)
        val3 = constant_value_expression(314)
        cond1 = comparision_greater_or_equal_condition(val1, val2)
        self.assertTrue(cond1.is_satisfied(None, None))
        cond2 = comparision_greater_or_equal_condition(val1, val3)
        self.assertTrue(cond2.is_satisfied(None, None))
        cond3 = comparision_greater_or_equal_condition(val2, val3)
        self.assertFalse(cond3.is_satisfied(None, None))
        
    def test_of_converting_to_string(self):
        val1 = constant_value_expression(314)
        val2 = constant_value_expression(271)
        cond = comparision_greater_or_equal_condition(val1, val2)
        self.assertEqual(str(cond), "314 >= 271")

#-------------------------------------------------------------------------

class Test_comparision_less_condition(unittest.TestCase):

    def test_of_is_satisfied(self):
        val1 = constant_value_expression(314)
        val2 = constant_value_expression(271)
        val3 = constant_value_expression(314)
        cond1 = comparision_less_condition(val1, val2)
        self.assertFalse(cond1.is_satisfied(None, None))
        cond2 = comparision_less_condition(val1, val3)
        self.assertFalse(cond2.is_satisfied(None, None))
        cond3 = comparision_less_condition(val2, val3)
        self.assertTrue(cond3.is_satisfied(None, None))
        
    def test_of_converting_to_string(self):
        val1 = constant_value_expression(314)
        val2 = constant_value_expression(271)
        cond = comparision_less_condition(val1, val2)
        self.assertEqual(str(cond), "314 < 271")

#-------------------------------------------------------------------------

class Test_comparision_less_or_equal_condition(unittest.TestCase):

    def test_of_is_satisfied(self):
        val1 = constant_value_expression(314)
        val2 = constant_value_expression(271)
        val3 = constant_value_expression(314)
        cond1 = comparision_less_or_equal_condition(val1, val2)
        self.assertFalse(cond1.is_satisfied(None, None))
        cond2 = comparision_less_or_equal_condition(val1, val3)
        self.assertTrue(cond2.is_satisfied(None, None))
        cond3 = comparision_less_or_equal_condition(val2, val3)
        self.assertTrue(cond3.is_satisfied(None, None))
        
    def test_of_converting_to_string(self):
        val1 = constant_value_expression(314)
        val2 = constant_value_expression(271)
        cond = comparision_less_or_equal_condition(val1, val2)
        self.assertEqual(str(cond), "314 <= 271")

#-------------------------------------------------------------------------

