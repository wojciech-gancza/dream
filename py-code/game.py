#-------------------------------------------------------------------------
# DREAM (C) WGan 2020
#-------------------------------------------------------------------------

class processor(object):

    """ main object of the game - combines all necessary objects to
        make game running """

    def __init__(self, object_provider, io_channel, location_name):
        self._factory = object_provider
        self._console = io_channel
        self._location = self._factory.get_object(location_name)
        self._continue_execution = True

    def run(self):
        self._console.write(self._location._description.get_long_text())
        while self._continue_execution:
            command_text = self._console.read()
            if command_text is None:
                self.stop()
            elif not self._location.try_execute(command_text, self):
                self._console.write("I do not know how to " + command_text)

    def stop(self):
        self._continue_execution = False

#-------------------------------------------------------------------------
