#-------------------------------------------------------------------------
# DREAM (C) WGan 2020
#-------------------------------------------------------------------------

import                      unittest

#-------------------------------------------------------------------------

from errors_test     import Test_error, \
                            Test_break_action

from tools_test      import Test_translator, \
                            Test_testing_console

from data_test       import Test_name, \
                            Test_description, \
                            Test_property, \
                            Test_properties, \
                            Test_location, \
                            Test_actions, \
                            Test_item, \
                            Test_inventory, \
                            Test_realm, \
                            Test_player

from builder_test    import Test_array_tokenizer, \
                            Test_buffered_token_source, \
                            Test_file_data_source, \
                            Test_data_reader, \
                            Test_object_builder, \
                            Test_object_factory, \
                            Test_realm_cache, \
                            Test_location_cache

from expression_test import Test_object_provider, \
                            Test_object_parameter_provider, \
                            Test_subject_parameter_provider, \
                            Test_item_parameter_provider, \
                            Test_constant_provider, \
                            Test_new_provider, \
                            Test_expression_base_class, \
                            Test_of_constant_expression, \
                            Test_of_sum_expression, \
                            Test_of_product_expression, \
                            Test_of_property_provider_base, \
                            Test_of_object_property_provider, \
                            Test_of_subject_property_provider, \
                            Test_of_location_property_provider, \
                            Test_of_player_property_provider, \
                            Test_of_free_text_property_provider, \
                            Test_of_item_property_provider, \
                            Test_of_dice_value, \
                            Test_of_property_provider_base, \
                            Test_of_player_provider, \
                            Test_of_location_provider, \
                            Test_of_realm_provider

from execution_test  import Test_exit_node, \
                            Test_translating_text_node, \
                            Test_print_text_node, \
                            Test_look_around_node, \
                            Test_change_location_node, \
                            Test_inventory_node, \
                            Test_examine_node, \
                            Test_take_item_node, \
                            Test_drop_item_node, \
                            Test_delete_item_node, \
                            Test_execute_command_node, \
                            Test_of_become_node, \
                            Test_command_name, \
                            Test_command, \
                            Test_modify_property_base, \
                            Test_advance_property_node, \
                            Test_set_property_node, \
                            Test_trace_node, \
                            Test_dump_node

from condition_test  import Test_condition_base, \
                            Test_comparison_condition, \
                            Test_comparision_equal_condition, \
                            Test_comparision_not_equal_condition, \
                            Test_comparision_greater_condition, \
                            Test_comparision_greater_or_equal_condition, \
                            Test_comparision_less_condition, \
                            Test_comparision_less_or_equal_condition

from compiler_test   import Test_compiler

from game_test       import Test_of_the_processor

#-------------------------------------------------------------------------

if __name__ == '__main__':
    
    unittest.main()

