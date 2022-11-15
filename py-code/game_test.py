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
        factory = object_factory("../dream/tests")
        game    = processor(factory, io, "dark cave")
        game.run()
        self.assertEqual(game._console._buffer, \
                    "You are in dark cave\n" \
                    "The cave is really dark\n" \
                    "I do not know how to hello\n" )

    def test_of_immidate_exit(self):
        orders  = [ "wake up" ]
        io      = testing_console(orders)
        factory = object_factory("../dream/tests")
        game    = processor(factory, io, "dark cave")
        game.run()
        self.assertEqual(game._console._buffer, \
                    "You are in dark cave\n" \
                    "The cave is really dark\n" \
                    "You woke up from the dream.\n" )
        
    def test_of_traweling_between_location(self):
        orders  = [ "west", "north", "south", "east" ]
        io      = testing_console(orders)
        factory = object_factory("../dream/tests")
        game    = processor(factory, io, "mansion hall")
        game.run()
        self.assertEqual(game._console._buffer, \
                    "You are in mansion hall\n" \
                    "You see doors around however main door located on " \
                    "south looks not real.\n" \
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
        
    def test_of_looking_around(self):
        orders  = [ "look" ]
        io      = testing_console(orders)
        factory = object_factory("../dream/tests")
        game    = processor(factory, io, "mansion kitchen")
        game.run()
        self.assertEqual(game._console._buffer, \
                    "You are in mansion kitchen\n" \
                    "Mansion kitchen look abadoned years ago\n" \
                    "This is mansion kitchen. It was plundered many times and " \
                    "anything which was not nailed to the floor was already " \
                    "taken. Rest was demolished. You see nothing interested. " \
                    "On  the north you see dining room door. On the west you " \
                    "see hall door.\n" \
                    "You notice:\n" \
                    " - Lockpick made of thin shiny wire.\n" )
        
    def test_of_examining_inventory(self):
        orders  = [ "pocket" ]
        io      = testing_console(orders)
        factory = object_factory("../dream/tests")
        game    = processor(factory, io, "mansion kitchen")
        game._pocket.put_item( factory.get_object("lockpick made from wire") )
        game._pocket.put_item( factory.get_object("unisolated wire") )
        game.run()
        self.assertEqual(game._console._buffer, \
                    "You are in mansion kitchen\n" \
                    "Mansion kitchen look abadoned years ago\n" \
                    "You have:\n" \
                    " - Lockpick made of thin shiny wire.\n" \
                    " - Short piece of shiny wire.\n" )
        
    def test_of_examining_existing_item(self):
        orders  = [ "examine", "examine something", "examine wire", "examine lockpick", "examine bended wire" ]
        io      = testing_console(orders)
        factory = object_factory("../dream/tests")
        game    = processor(factory, io, "test dark cave")
        game._pocket.put_item( factory.get_object("lockpick made from wire") )
        game.run()
        self.assertEqual(game._console._buffer, \
                    "You are in dark cave\n" \
                    "The cave is really dark\n" \
                    "Be more specific\nI see no something\n" \
                    "This is a piece of wire. It is about 20cm long and it looks like " \
                    "made of aluminium. It is preety hard to bend, but bendable in bare " \
                    "fingers.\n" \
                    "Maybe it does not look like profesional tool, however " \
                    "it could cheat older locks when you have a little experience with " \
                    "its construction.\n" \
                    "Maybe it does not look like profesional tool, however it could cheat " \
                    "older locks when you have a little experience with its " \
                    "construction.\n" )    
    
    def test_of_taking_and_dropping_item(self):
        orders  = [ "look", "i", "take wire", "i", "look", "drop wire", "drop lockpick", "i", \
                    "look", "del lockpick", "del wire", "look", "i" ]
        io      = testing_console(orders)
        factory = object_factory("../dream/tests")
        game    = processor(factory, io, "test dark cave")
        game._pocket.put_item( factory.get_object("lockpick made from wire") )
        game.run()
        self.assertEqual(game._console._buffer, \
                    "You are in dark cave\n" \
                    "The cave is really dark\n" \
                    "You see barly nothing. The cave is really dark. After a while you " \
                    "seem to see a shadows in the darkness but you cannot realize what " \
                    "it can be. You see no way out and no possiblility to move safely.\n" \
                    "You notice:\n" \
                    " - Short piece of shiny wire.\n" \
                    "You have:\n" \
                    " - Lockpick made of thin shiny wire.\n" \
                    "You take wire\nYou have:\n" \
                    " - Lockpick made of thin shiny wire.\n" \
                    " - Short piece of shiny wire.\n" \
                    "You see barly nothing. The cave is really dark. After a while you " \
                    "seem to see a shadows in the darkness but you cannot realize what " \
                    "it can be. You see no way out and no possiblility to move safely.\n" \
                    "You drop wire\n" \
                    "You drop lockpick\n" \
                    "You have nothing.\n" \
                    "You see barly nothing. The cave is really dark. After a while you " \
                    "seem to see a shadows in the darkness but you cannot realize what " \
                    "it can be. You see no way out and no possiblility to move safely.\n" \
                    "You notice:\n" \
                    " - Short piece of shiny wire.\n" \
                    " - Lockpick made of thin shiny wire.\n" \
                    "You destroy lockpick\nYou destroy wire\n" \
                    "You see barly nothing. The cave is really dark. After a while you " \
                    "seem to see a shadows in the darkness but you cannot realize what " \
                    "it can be. You see no way out and no possiblility to move safely.\n" \
                    "You have nothing.\n" )

    def test_of_execution_of_items_actions(self):
        orders  = [ "mumble", "summon", "mumble" ]
        io      = testing_console(orders)
        factory = object_factory("../dream/tests")
        game    = processor(factory, io, "test dark cave")
        game.run()
        self.assertEqual(game._console._buffer, \
                    "You are in dark cave\n" \
                    "The cave is really dark\n" \
                    "I do not know how to mumble\n" \
                    "A gizmo appears in your pocket!\n" \
                    "Hogo-fogo.\n" )

    def test_of_location_cache(self):
        orders  = [ "w", "look", "take lockpick", "e", "w", "look" ]
        io      = testing_console(orders)
        factory = object_factory("../dream/tests")
        game    = processor(factory, io, "mansion hall")
        game.run()
        self.assertEqual(game._console._buffer, \
                    "You are in mansion hall\n" \
                    "You see doors around however main door located on south looks not real.\n" \
                    "You are in mansion kitchen\nMansion kitchen look abadoned years ago\n" \
                    "This is mansion kitchen. It was plundered many times and anything which " \
                    "was not nailed to the floor was already taken. Rest was demolished. You " \
                    "see nothing interested. On  the north you see dining room door. On the " \
                    "west you see hall door.\n" \
                    "You notice:\n" \
                    " - Lockpick made of thin shiny wire.\n" \
                    "You are in mansion hall\nYou see doors around however main door located " \
                    "on south looks not real.\nYou are in mansion kitchen\n" \
                    "Mansion kitchen look abadoned years ago\n" \
                    "This is mansion kitchen. It was plundered many times and anything which " \
                    "was not nailed to the floor was already taken. Rest was demolished. You " \
                    "see nothing interested. On  the north you see dining room door. On the " \
                    "west you see hall door.\n" )

    def test_of_command_name_comparing(self):
        orders  = [ "ne" ]
        io      = testing_console(orders)
        factory = object_factory("../dream/examples/lession_01/03-map-2a")
        game    = processor(factory, io, "entrance")
        game.run()
        self.assertEqual(game._console._buffer, \
                    "You are in entrance\n" \
                    "You see dark cave entrance on the east\n" \
                    "It is not possible to go northeast\n" )

    def test_of_reaction_on_empty_command(self):
        orders  = [ "" ]
        io      = testing_console(orders)
        factory = object_factory("../dream/examples/lession_01/03-map-2a")
        game    = processor(factory, io, "entrance")
        game.run()
        self.assertEqual(game._console._buffer, \
                    "You are in entrance\n" \
                    "You see dark cave entrance on the east\n" )

    def test_of_error_handling(self):
        orders  = [ "z" ]
        io      = testing_console(orders)
        factory = object_factory("../dream/tests")
        game    = processor(factory, io, "test dark cave")
        game.run()
        self.assertEqual(game._console._buffer, \
                    "You are in dark cave\n" \
                    "The cave is really dark\n" \
                    "Processing command 'z' raised error: 'Cannot create object named 'hell''\n" )

    def test_of_exec(self):
        orders  = [ "take shovel", "ne", "n", "take map", "ne", "dig", "i" ]
        io      = testing_console(orders)
        factory = object_factory("../dream/examples/lession_02/01-map-2b")
        game    = processor(factory, io, "cave")
        game.run()
        #print
        #print("<obtaining treasure>")
        #print(io._buffer)
        self.assertEqual(game._console._buffer, \
                    "You are in cave\n" \
                    "You see a cave walls around\n" \
                    "You grab the shovel\n" \
                    "You pass the opening on northeast. On the other side, you see...\n" \
                    "You are in tunnel\n" \
                    "You are in stone tunnel\n" \
                    "You go deeper into the cave tunnels\n" \
                    "You are in labirynth\n" \
                    "You see the cave room looking like labirynth chamber.\n" \
                    "You grab the treasure map\n" \
                    "You go stright to northwest\n" \
                    "You are in sand cave\n" \
                    "You see a cave with floor formed from shiny sand emmiting delicate luminescence.\n" \
                    "You dig in the ground.\n" \
                    "(because you looked at the treasure map and found where the treasure is hidden)\n" \
                    "You found a treasure\n" \
                    "You have:\n" \
                    " - Ordinary shovel.\n" \
                    " - A piece of map with red 'x' on it.\n" \
                    " - A valuable terasure\n" )

    def test_of_exec_fail_1(self):
        orders  = [ "take shovel", "ne", "n", "ne", "dig", "i" ]
        # dig in proper place but having no map
        io      = testing_console(orders)
        factory = object_factory("../dream/examples/lession_02/01-map-2b")
        game    = processor(factory, io, "cave")
        game.run()
        #print
        #print("<1 dig in proper place but having no map>")
        #print(io._buffer)
        self.assertEqual(game._console._buffer, \
                    "You are in cave\n" \
                    "You see a cave walls around\n" \
                    "You grab the shovel\n" \
                    "You pass the opening on northeast. On the other side, you see...\n" \
                    "You are in tunnel\n" \
                    "You are in stone tunnel\n" \
                    "You go deeper into the cave tunnels\n" \
                    "You are in labirynth\n" \
                    "You see the cave room looking like labirynth chamber.\n" \
                    "You go stright to northwest\nYou are in sand cave\n" \
                    "You see a cave with floor formed from shiny sand emmiting delicate luminescence.\n" \
                    "You dig in the ground.\n" \
                    "You have:\n" \
                    " - Ordinary shovel.\n" )
    
    def test_of_exec_fail_2(self):
        # dig in wrong place having all items
        orders  = [ "take shovel", "ne", "n", "take map", "dig", "i" ]
        io      = testing_console(orders)
        factory = object_factory("../dream/examples/lession_02/01-map-2b")
        game    = processor(factory, io, "cave")
        game.run()
        #print
        #print("<2 dig in wrong place having all items>")
        #print(io._buffer)
        self.assertEqual(game._console._buffer, \
                    "You are in cave\n" \
                    "You see a cave walls around\n" \
                    "You grab the shovel\n" \
                    "You pass the opening on northeast. On the other side, you see...\n" \
                    "You are in tunnel\n" \
                    "You are in stone tunnel\n" \
                    "You go deeper into the cave tunnels\n" \
                    "You are in labirynth\n" \
                    "You see the cave room looking like labirynth chamber.\n" \
                    "You grab the treasure map\n" \
                    "You dig in the ground.\n" \
                    "You have:\n" \
                    " - Ordinary shovel.\n" \
                    " - A piece of map with red 'x' on it.\n" )
                    
    def test_of_exec_fail_3(self):
        orders  = [ "ne", "n", "take map", "ne", "dig", "i" ]
        # try to dig without a shovel
        io      = testing_console(orders)
        factory = object_factory("../dream/examples/lession_02/01-map-2b")
        game    = processor(factory, io, "cave")
        game.run()
        #print
        #print("<3 try to dig without a shovel>")
        #print(io._buffer)
        self.assertEqual(game._console._buffer, \
                    "You are in cave\n" \
                    "You see a cave walls around\n" \
                    "You pass the opening on northeast. On the other side, you see...\n" \
                    "You are in tunnel\n" \
                    "You are in stone tunnel\nYou go deeper into the cave tunnels\n" \
                    "You are in labirynth\n" \
                    "You see the cave room looking like labirynth chamber.\n" \
                    "You grab the treasure map\n" \
                    "You go stright to northwest\n" \
                    "You are in sand cave\n" \
                    "You see a cave with floor formed from shiny sand emmiting delicate luminescence.\n" \
                    "I do not know how to dig\n" \
                    "You have:\n" \
                    " - A piece of map with red 'x' on it.\n" )

    def test_of_failing_private_commands(self):
        orders  = [ "ne", "n", "take map", "_ check treasure map" ]
        io      = testing_console(orders)
        factory = object_factory("../dream/examples/lession_02/01-map-2b")
        game    = processor(factory, io, "cave")
        game.run()
        self.assertEqual(game._console._buffer, \
                    "You are in cave\n" \
                    "You see a cave walls around\n" \
                    "You pass the opening on northeast. On the other side, you see...\n" \
                    "You are in tunnel\n" \
                    "You are in stone tunnel\nYou go deeper into the cave tunnels\n" \
                    "You are in labirynth\n" \
                    "You see the cave room looking like labirynth chamber.\n" \
                    "You grab the treasure map\n" \
                    "I cannot directly execute _ check treasure map\n" )
                    
#-------------------------------------------------------------------------
