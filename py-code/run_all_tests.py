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
                            Test_realm

from builder_test    import Test_array_tokenizer, \
                            Test_buffered_token_source, \
                            Test_file_data_source, \
                            Test_data_reader, \
                            Test_object_builder, \
                            Test_object_factory, \
                            Test_realm_cache, \
                            Test_location_cache

from compiler_test   import Test_object_provider, \
                            Test_object_parameter_provider, \
                            Test_subject_parameter_provider, \
                            Test_constant_provider, \
                            Test_new_provider, \
                            Test_exit_node, \
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
                            Test_command_name, \
                            Test_command, \
                            Test_compiler

from game_test       import Test_of_the_processor

#-------------------------------------------------------------------------

if __name__ == '__main__':
    
    unittest.main()

