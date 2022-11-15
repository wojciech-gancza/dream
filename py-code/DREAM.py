#-------------------------------------------------------------------------
# DREAM (C) WGan 2020
#-------------------------------------------------------------------------

import                  unittest

from builder     import object_factory
from channel     import console
from tools_test  import testing_console
from game        import processor

#-------------------------------------------------------------------------

if __name__ == '__main__':
    
    io      = console()
    factory = object_factory("test-dream")
    game    = processor(factory, io, "mansion hall")

    game.run()

#-------------------------------------------------------------------------


