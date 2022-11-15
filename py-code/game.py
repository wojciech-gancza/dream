#-------------------------------------------------------------------------
# DREAM (C) WGan 2020
#-------------------------------------------------------------------------

from data        import items
from compiler    import change_location_node
from builder     import factory_realm_cache, \
                        factory_location_cache
from errors      import error, \
                        break_action

#-------------------------------------------------------------------------

class processor(object):

    """ main object of the game - combines all necessary objects to
        make game running """

    def __init__(self, object_provider, io_channel, location_name):
        self._factory = factory_location_cache(20, factory_realm_cache(object_provider))
        self._console = io_channel
        self._location = None
        self._pocket = items()
        self._continue_execution = True   
        init = change_location_node(location_name)
        init.run(self, "")

    def run(self):
        while self._continue_execution:
            command_text = self._console.read()
            if command_text is None:
                self.stop()
            else:
                command_text = command_text.strip()
                if command_text!= "":
                    try:
                        if command_text[0] == "_":
                            self._console.write("I cannot directly execute " + command_text)
                        elif not self.execute(command_text):
                            self._console.write("I do not know how to " + command_text)
                    except break_action:
                        pass
                    except error as err:
                        self._console.write("Processing command '" + command_text + "' raised error: '" + err._text + "'")

    def execute(self, command_text):
        if self._pocket.try_execute(command_text, self):
            return True
        if self._location.try_execute(command_text, self):
            return True
        return False      
                
    def stop(self):
        self._continue_execution = False

#-------------------------------------------------------------------------
