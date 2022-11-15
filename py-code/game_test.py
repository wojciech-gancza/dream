#-------------------------------------------------------------------------
# DREAM (C) WGan 2020
#-------------------------------------------------------------------------

import                  unittest

from builder     import object_factory
from channel     import console
from tools_test  import testing_console
from game        import processor

#-------------------------------------------------------------------------

class Test_of_the_processor(unittest.TestCase):

    def test_of_unknown_command(self):
        orders  = [ "hello" ]
        io      = testing_console(orders)
        factory = object_factory("test-dream")
        game    = processor(factory, io, "dark cave")
        game.run()
        self.assertEqual(game._console._buffer, \
                    "You see barly nothing. The cave is really dark. " \
                    "After a while you seem to see a shadows in the " \
                    "darkness but you cannot realize what it can be. " \
                    "You see no way out and no possiblility to move safely.\n" \
                    "I do not know how to hello\n" )

    def test_of_immidate_exit(self):
        orders  = [ "wake up" ]
        io      = testing_console(orders)
        factory = object_factory("test-dream")
        game    = processor(factory, io, "dark cave")
        game.run()
        self.assertEqual(game._console._buffer, \
                    "You see barly nothing. The cave is really dark. " \
                    "After a while you seem to see a shadows in the " \
                    "darkness but you cannot realize what it can be. " \
                    "You see no way out and no possiblility to move safely.\n" \
                    "You woke up from the dream.\n" )
        
    def test_of_traweling_between_location(self):
        orders  = [ "west", "north", "south", "east" ]
        io      = testing_console(orders)
        factory = object_factory("test-dream")
        game    = processor(factory, io, "mansion hall")
        game.run()
        self.assertEqual(game._console._buffer, \
                    "This is for sure a hall. Main door located on south " \
                    "are not real - they are painted on solid wall. It " \
                    "looks strange. Maybe other ways lead to somewhere.\n" \
                    "You are in mansion kitchen\nMansion kitchen look " \
                    "abadoned years ago\n" \
                    "You are in mansion dining room\n" \
                    "Mansion dining room looks sad and a little scary.\n" \
                    "You are in mansion hall\n" \
                    "You see doors around however main door located on " \
                    "south looks not real.\n" \
                    "You are in mansion storage\n" \
                    "Mansion storage looks empty. You see some rubich on " \
                    "the floor.\n" )
        
#-------------------------------------------------------------------------
