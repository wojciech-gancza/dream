#-------------------------------------------------------------------------
# DREAM (C) WGan 2020
#-------------------------------------------------------------------------

""" Processor is a module which process and changes state of the game, by
    processing commands on given items """

import                  unittest

from errors      import error
from expression  import object_provider, \
                        object_parameter_provider, \
                        subject_parameter_provider, \
                        constant_provider, \
                        new_object_provider, \
                        item_parameter_provider, \
                        realm_provider, \
                        location_provider, \
                        player_provider, \
                        expression_base, \
                        constant_value_expression, \
                        sum_expression, \
                        product_expression, \
                        property_provider_base, \
                        object_property_provider, \
                        subject_property_provider, \
                        location_property_provider, \
                        player_property_provider, \
                        item_property_provider, \
                        free_text_property_provider, \
                        dice_expression
from data        import item
from tools_test  import _game_mock 

#-------------------------------------------------------------------------

class Test_object_provider(unittest.TestCase):

    def test_unitialized_object(self):
        node = object_provider()
        self.assertEqual(node._name, "")
        self.assertTrue(node._object is None)
        self.assertFalse(node._already_taken)
        
    def test_initialization_with_existing_object(self):
        node = object_provider()
        game = _game_mock()
        node.set_accessible_object_name("unisolated wire", game)
        self.assertEqual(node._name, "wire")
        self.assertTrue(node.peek_object() is game._player._items.peek_item("wire"))
        
    def test_initialization_with_non_existing_object(self):
        node = object_provider()
        game = _game_mock()
        node.set_accessible_object_name("unwired isolation", game)
        self.assertEqual(node._name, "unwired isolation")
        self.assertTrue(node.peek_object() is None)
        
    def test_taking_existing_object(self):
        node = object_provider()
        game = _game_mock()
        node.set_accessible_object_name("unisolated wire", game)
        self.assertEqual(node._name, "wire")
        wire = game._player._items.peek_item("wire")
        self.assertTrue(node.take_object(game) is wire)
        self.assertTrue(game._player._items.peek_item("wire") is None)
        
    def test_taking_non_existing_object(self):
        node = object_provider()
        game = _game_mock()
        node.set_accessible_object_name("unwired isolation", game)
        self.assertEqual(node._name, "unwired isolation")
        self.assertTrue(node.take_object(game) is None)
        
#-------------------------------------------------------------------------

class Test_object_parameter_provider(unittest.TestCase):

    def test_object_parameter_provider_found(self):
        node = object_parameter_provider()
        game = _game_mock()
        node.set_parameters(game, "wire connector")
        self.assertEqual(node.get_name(), "wire connector")
        self.assertTrue(node.peek_object() is None)

    def test_object_parameter_provider_not_found(self):
        node = object_parameter_provider()
        game = _game_mock()
        node.set_parameters(game, " connecting wire")
        self.assertEqual(node.get_name(), "wire")
        self.assertTrue(type(node.peek_object()) is item)

    def test_object_parameter_provider_to_string(self):
        node = object_parameter_provider()
        self.assertEqual(str(node), "OBJECT")

#-------------------------------------------------------------------------

class Test_subject_parameter_provider(unittest.TestCase):

    def test_subject_parameter_provider_found(self):
        node = subject_parameter_provider()
        game = _game_mock()
        node.set_parameters(game, "wire connector")
        self.assertEqual(node.get_name(), "wire")
        self.assertTrue(type(node.peek_object()) is item)

    def test_subject_parameter_provider_not_found(self):
        node = subject_parameter_provider()
        game = _game_mock()
        node.set_parameters(game, "connecting wire")
        self.assertEqual(node.get_name(), "connecting wire")
        self.assertTrue(node.peek_object() is None)

    def test_subject_parameter_provider_to_string(self):
        node = subject_parameter_provider()
        self.assertEqual(str(node), "SUBJECT")

#-------------------------------------------------------------------------

class Test_item_parameter_provider(unittest.TestCase):

    def test_item_parameter_provider_found(self):
        node = item_parameter_provider()
        game = _game_mock()
        it = item()
        it._name._main_name = "gizmo"
        game._memo["ITEM"] = it
        node.set_parameters(game, "")
        self.assertEqual(node.get_name(), "gizmo")
        self.assertTrue(type(node.peek_object()) is item)
        self.assertTrue(node.peek_object() is it)

    def test_subject_parameter_provider_not_found(self):
        node = item_parameter_provider()
        game = _game_mock()
        try:
            node.set_parameters(game, "")
            self.assertTrue(False)
        except error as err:
            self.assertEqual(str(err), "ERROR: ITEM was not selected. It must be specified in condition.")
        except Exception:
            self.assertTrue(False)        

    def test_subject_parameter_provider_to_string(self):
        node = item_parameter_provider()
        self.assertEqual(str(node), "ITEM")

#-------------------------------------------------------------------------

class Test_constant_provider(unittest.TestCase):

    def test_constant_provider_found(self):
        node = constant_provider("wire")
        game = _game_mock()
        node.set_parameters(game, "strange connector")
        self.assertEqual(node.get_name(), "wire")
        self.assertTrue(type(node.peek_object()) is item)

    def test_constant_provider_not_found(self):
        node = constant_provider("gizmo")
        game = _game_mock()
        node.set_parameters(game, "wire wire wire")
        self.assertEqual(node.get_name(), "gizmo")
        self.assertTrue(node.peek_object() is None)

    def test_constant_provider_to_string(self):
        node = constant_provider("some text")
        self.assertEqual(str(node), "some text")

#-------------------------------------------------------------------------

class Test_new_provider(unittest.TestCase):

    def test_new_provider_found(self):
        game = _game_mock()
        game._player._items.put_item( game._factory.get_object("box of matches") )
        obj = new_object_provider(constant_provider("mathes"))
        obj.set_parameters(game, "")
        self.assertEqual(obj.get_name(), "box of matches")
        self.assertTrue(type(obj.peek_object()) is item)
    
    def test_new_provider_not_found(self):
        node = new_object_provider(constant_provider("gizmo"))
        game = _game_mock()
        node.set_parameters(game, "wire wire wire")
        self.assertEqual(node.get_name(), "gizmo")
        self.assertTrue(type(node.peek_object()) is item)
    
    def test_new_provider_nonexisting_object(self):
        node = new_object_provider(constant_provider("gizmolada"))
        game = _game_mock()
        node.set_parameters(game, "wire wire wire")
        self.assertEqual(node.get_name(), "gizmolada")
        self.assertTrue(node.peek_object() is None)
    
    def test_new_provider_copies_item(self):
        game = _game_mock()
        game._player._items.put_item( game._factory.get_object("box of matches") )
        obj = new_object_provider(constant_provider("mathes"))
        obj.set_parameters(game, "")
        self.assertEqual(obj.get_name(), "box of matches")
        self.assertTrue(type(obj.take_object(game)) is item)
        self.assertFalse(game._player._items.peek_item("box of matches") is None)

    def test_new_creating_item_to_string(self):
        obj = new_object_provider(constant_provider("box of matches"))
        self.assertEqual(str(obj), "NEW box of matches")

#-------------------------------------------------------------------------

class Test_of_player_provider(unittest.TestCase):

    def test_of_execution(self):
        node = player_provider()
        game = _game_mock()
        node.set_parameters(game, "")
        object = node.peek_object()
        self.assertTrue(object is game._player)
        
    def test_of_seralization(self):
        node = player_provider()
        self.assertEqual(str(node), "PLAYER")

#-------------------------------------------------------------------------

class Test_of_location_provider(unittest.TestCase):

    def test_of_execution(self):
        node = location_provider()
        game = _game_mock()
        node.set_parameters(game, "")
        object = node.peek_object()
        self.assertTrue(object is game._location)
        
    def test_of_seralization(self):
        node = location_provider()
        self.assertEqual(str(node), "LOCATION")

#-------------------------------------------------------------------------

class Test_of_realm_provider(unittest.TestCase):

    def test_of_execution(self):
        node = realm_provider()
        game = _game_mock()
        node.set_parameters(game, "")
        object = node.peek_object()
        self.assertTrue(object is game._location._realm)
        
    def test_of_seralization(self):
        node = realm_provider()
        self.assertEqual(str(node), "REALM")

#-------------------------------------------------------------------------

class Test_expression_base_class(unittest.TestCase):

    def test_of_interface(self):
        expr = expression_base()
        self.assertEqual(expr.value(1,2), 0)

#-------------------------------------------------------------------------

class Test_of_constant_expression(unittest.TestCase):

    def test_of_value(self):
        expr = constant_value_expression(123)
        self.assertEqual(expr._value, 123)

    def test_of_serialization(self):
        expr = constant_value_expression(123)
        self.assertEqual(str(expr), "123")

#-------------------------------------------------------------------------

class Test_of_sum_expression(unittest.TestCase):

    def test_of_calculations_1(self):
        expr = sum_expression([constant_value_expression(123), constant_value_expression(321)], [constant_value_expression(44)])
        self.assertEqual( expr.value(None, None), 400)

    def test_of_calculations_2(self):
        expr = sum_expression([ ], [constant_value_expression(44)])
        self.assertEqual( expr.value(None, None), -44)
        
    def test_of_serialization_1(self):
        expr = sum_expression([constant_value_expression(123), constant_value_expression(321)], [constant_value_expression(44)])
        self.assertEqual( str(expr), "123 + 321 - 44" )
 
    def test_of_serialization_2(self):
        expr = sum_expression([ ], [constant_value_expression(44)])
        self.assertEqual( str(expr), "- 44" )
 
#-------------------------------------------------------------------------

class Test_of_product_expression(unittest.TestCase):

    def test_of_calculations_1(self):
        expr = product_expression([constant_value_expression(5), constant_value_expression(4)], [constant_value_expression(2)])
        self.assertEqual( expr.value(None, None), 10)

    def test_of_calculations_2(self):
        expr = product_expression([ ], [constant_value_expression(2)])
        self.assertEqual( expr.value(None, None), 1/2)
        
    def test_of_serialization_1(self):
        expr = product_expression([constant_value_expression(5), constant_value_expression(4)], [constant_value_expression(2)])
        self.assertEqual( str(expr), "5 * 4 / 2" )
 
    def test_of_serialization_2(self):
        expr = product_expression([ ], [constant_value_expression(2)])
        self.assertEqual( str(expr), "1 / 2" )

#-------------------------------------------------------------------------

class test_property_provider(property_provider_base):

    def __init__(self):
        property_provider_base.__init__(self, "test")
        self._item = item()
        
    def _get_provider(self, game, parameters):
        return self._item

class Test_of_property_provider_base(unittest.TestCase):

    def test_of_seeing_value(self):
        expr = test_property_provider()
        self.assertEqual(expr._property_name, "test")
        
    def test_of_taking_value(self):
        expr = test_property_provider()
        expr._item._properties.set("test", 123)
        self.assertEqual(expr.value(None, None), 123)

    def test_of_advancing_value(self):
        expr = test_property_provider()
        expr.add(None, None, 100)
        expr.add(None, None, 110)
        expr.add(None, None, 111)
        self.assertEqual(expr.value(None, None), 321)

    def test_of_setting_value(self):
        expr = test_property_provider()
        expr.set(None, None, 100)
        expr.set(None, None, 110)
        expr.set(None, None, 111)
        self.assertEqual(expr.value(None, None), 111)
    
#-------------------------------------------------------------------------

class Test_of_object_property_provider(unittest.TestCase):

    def test_of_returning_property(self):
        expr = object_property_provider("weight")
        game = _game_mock()
        it = item()
        it._name.set_names( ["gizmo"] )
        it._properties.add("weight", 1001)
        game._location._items.put_item(it)
        val = expr.value(game, "just a gizmo")
        self.assertEqual(val, 1001)

    def test_of_failing_returning_property_1(self):
        expr = object_property_provider("weight")
        game = _game_mock()
        it = item()
        it._name.set_names( ["gizmo"] )
        it._properties.add("length", 1001)
        game._location._items.put_item(it)
        val = expr.value(game, "just a gizmo")
        self.assertEqual(val, 0)

    def test_of_failing_returning_property_2(self):
        expr = object_property_provider("weight")
        game = _game_mock()
        it = item()
        it._name.set_names( ["gizmo"] )
        it._properties.add("weight", 1001)
        game._location._items.put_item(it)
        val = expr.value(game, "just a dynks")
        self.assertEqual(val, 0)

    def test_of_serialization(self):
        expr = object_property_provider("weight")
        self.assertEqual(str(expr), "OBJECT weight")

#-------------------------------------------------------------------------

class Test_of_subject_property_provider(unittest.TestCase):

    def test_of_returning_property(self):
        expr = subject_property_provider("weight")
        game = _game_mock()
        it = item()
        it._name.set_names( ["gizmo"] )
        it._properties.add("weight", 1001)
        game._location._items.put_item(it)
        val = expr.value(game, "gizmo i great")
        self.assertEqual(val, 1001)

    def test_of_failing_returning_property_1(self):
        expr = subject_property_provider("weight")
        game = _game_mock()
        it = item()
        it._name.set_names( ["gizmo"] )
        it._properties.add("length", 1001)
        game._location._items.put_item(it)
        val = expr.value(game, "gizmo i great")
        self.assertEqual(val, 0)

    def test_of_failing_returning_property_2(self):
        expr = subject_property_provider("weight")
        game = _game_mock()
        it = item()
        it._name.set_names( ["gizmo"] )
        it._properties.add("weight", 1001)
        game._location._items.put_item(it)
        val = expr.value(game, "just a dynks")
        self.assertEqual(val, 0)

    def test_of_serialization(self):
        expr = subject_property_provider("weight")
        self.assertEqual(str(expr), "SUBJECT weight")

#-------------------------------------------------------------------------

class Test_of_location_property_provider(unittest.TestCase):

    def test_of_returning_property(self):
        expr = location_property_provider("weight")
        game = _game_mock()
        game._location._properties.add("weight", 1001)
        val = expr.value(game, "")
        self.assertEqual(val, 1001)

    def test_of_failing_returning_property_1(self):
        expr = subject_property_provider("weight")
        game = _game_mock()
        game._location._properties.add("length", 1001)
        val = expr.value(game, "")
        self.assertEqual(val, 0)

    def test_of_failing_returning_property_2(self):
        expr = subject_property_provider("weight")
        game = _game_mock()
        it = item()
        it._name.set_names( ["gizmo"] )
        it._properties.add("weight", 1001)
        game._location._items.put_item(it)
        val = expr.value(game, "")
        self.assertEqual(val, 0)

    def test_of_serialization(self):
        expr = location_property_provider("weight")
        self.assertEqual(str(expr), "LOCATION weight")

#-------------------------------------------------------------------------

class Test_of_player_property_provider(unittest.TestCase):

    def test_of_returning_property(self):
        expr = player_property_provider("weight")
        game = _game_mock()
        game._player._properties.add("weight", 1001)
        val = expr.value(game, "")
        self.assertEqual(val, 1001)

    def test_of_failing_returning_property_1(self):
        expr = player_property_provider("weight")
        game = _game_mock()
        game._player._properties.add("length", 1001)
        val = expr.value(game, "")
        self.assertEqual(val, 0)

    def test_of_failing_returning_property_2(self):
        expr = player_property_provider("weight")
        game = _game_mock()
        it = item()
        it._name.set_names( ["gizmo"] )
        it._properties.add("weight", 1001)
        game._location._items.put_item(it)
        game._location._properties.add("weight", 1001)
        val = expr.value(game, "")
        self.assertEqual(val, 0)

    def test_of_serialization(self):
        expr = player_property_provider("weight")
        self.assertEqual(str(expr), "PLAYER weight")

#-------------------------------------------------------------------------

class Test_of_free_text_property_provider(unittest.TestCase):

    def test_of_returning_property(self):
        expr = free_text_property_provider("gizmo weight")
        game = _game_mock()
        it = item()
        it._name.set_names( ["gizmo"] )
        it._properties.add("weight", 1001)
        game._location._items.put_item(it)
        val = expr.value(game, "")
        self.assertEqual(val, 1001)

    def test_of_failing_returning_property_1(self):
        expr = free_text_property_provider("gizmo weight")
        game = _game_mock()
        it = item()
        it._name.set_names( ["gizmo"] )
        it._properties.add("length", 1001)
        game._location._items.put_item(it)
        val = expr.value(game, "")
        self.assertEqual(val, 0)

    def test_of_failing_returning_property_2(self):
        expr = free_text_property_provider("gizmo weight")
        game = _game_mock()
        it = item()
        it._name.set_names( ["dynks"] )
        it._properties.add("weight", 1001)
        game._location._items.put_item(it)
        game._location._properties.add("weight", 1001)
        try:
            val = expr.value(game, "")
            self.assertEqual(val, 0)
        except error as err:
            self.assertTrue(False)
        except Exception as ex:
            self.assertTrue(False)

    def test_of_failing_returning_property_4(self):
        expr = free_text_property_provider("weight")
        game = _game_mock()
        it = item()
        it._name.set_names( ["dynks"] )
        it._properties.add("weight", 1001)
        game._location._items.put_item(it)
        game._location._properties.add("weight", 1001)
        try:
            val = expr.value(game, "")
            self.assertEqual(val, 0)
        except error as err:
            self.assertTrue(False)
        except Exception:
            self.assertTrue(False)

    def test_of_serialization(self):
        expr = free_text_property_provider("gizmo weight")
        self.assertEqual(str(expr), "gizmo weight")

#-------------------------------------------------------------------------

class Test_of_item_property_provider(unittest.TestCase):
    
    def test_of_returning_obiect_1(self):
        expr1 = item_property_provider("length")
        expr2 = item_property_provider("width")
        game = _game_mock()
        it1 = item()
        it1._name.set_names(["gizmo"])
        it1._properties.add("length", 1000)
        it1._properties.add("width", 7000)
        game._location._items.put_item(it1)
        it2 = item()
        it2._name.set_names(["dynks"])
        it2._properties.add("length", 2000)
        it2._properties.add("width", 3000)
        game._location._items.put_item(it2)
        val1 = expr1.value(game, "")
        self.assertEqual(val1, 2000) # first search sets the object
        val2 = expr2.value(game, "")
        self.assertEqual(val2, 3000)
        self.assertTrue(game._memo["ITEM"] is it2)
        
    def test_of_obiect_not_found(self):
        expr1 = item_property_provider("volume")
        game = _game_mock()
        it1 = item()
        it1._name.set_names(["gizmo"])
        it1._properties.add("length", 1000)
        it1._properties.add("width", 7000)
        game._location._items.put_item(it1)
        it2 = item()
        it2._name.set_names(["dynks"])
        it2._properties.add("length", 2000)
        it2._properties.add("width", 3000)
        game._location._items.put_item(it2)
        val1 = expr1.value(game, "")
        self.assertEqual(val1, 0)
        self.assertFalse("ITEM" in game._memo.keys())

    def test_of_serialization(self):
        expr = item_property_provider("weight")
        self.assertEqual(str(expr), "ITEM weight")

#-------------------------------------------------------------------------

class Test_of_dice_value(unittest.TestCase):

    def test_of_dice_range(self):
        expr = dice_expression(constant_value_expression(6))
        hit = [0] * 7
        for i in range(1, 1000):
            val = expr.value(None, None)
            self.assertTrue(val >= 1 and val <= 6)
            hit[val] = hit[val]+1
        for i in range(1, 7):
            self.assertTrue(hit[i] > 0)
            
    def test_of_cast_to_string_1(self):
        expr = dice_expression(constant_value_expression(6))
        self.assertEqual(str(expr), "DICE")
        
    def test_of_cast_to_string_2(self):
        expr = dice_expression(constant_value_expression(20))
        self.assertEqual(str(expr), "DICE 20")
        
#-------------------------------------------------------------------------

