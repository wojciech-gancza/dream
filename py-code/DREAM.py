#-------------------------------------------------------------------------
# DREAM (C) WGan 2020
#-------------------------------------------------------------------------

import                  unittest
import                  sys
import                  os

from builder     import object_factory
from channel     import console
from tools_test  import testing_console
from game        import processor
from data        import items

#-------------------------------------------------------------------------

if __name__ == '__main__':

    parameters_read = False
    if len(sys.argv) == 3:
        factory_path = sys.argv[1].replace('\\', '/')
        startup_location = sys.argv[2].strip()
        if os.path.isdir(factory_path):
            if os.path.isfile(factory_path + "/" + startup_location + ".def"):
                parameters_read = True
    if parameters_read:
        io      = console()
        factory = object_factory(factory_path)
        game    = processor(factory, io, startup_location)

        game.run()
    else:
        print("Program must be run with two parameters:")
        print(" - path to the set of files describing elements of the game")
        print(" - name of the startup location")

#-------------------------------------------------------------------------


