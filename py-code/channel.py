#-------------------------------------------------------------------------
# DREAM (C) WGan 2020
#-------------------------------------------------------------------------

""" Command line input/output - output goes directly to screen, reading
    keyboard commands and test classes used to mock them in tests """

from errors  import error

#-------------------------------------------------------------------------

class console(object):

    """ Console input/output adapter """

    def __init__(self):
        self.trace = False

    def write(self, text):
        print(text)
        
    def dump(self, text):
        print("# " + text.replace("\n", "\n# "))
    
    def log(self, text):
        if self.trace:
            print("# " + text.replace("\n", "\n# "))
        
    def read(self):
        try:
            return raw_input("??? > ")
        except:
            return input("??? > ")
     
#-------------------------------------------------------------------------

class ansi_console(object):

    """ Console input/output adapter with colors """
    
    def __init__(self):
        from platform import system
        if "win" in system().lower(): #works for Win7, 8, 10 ...
            from ctypes import windll
            k=windll.kernel32
            k.SetConsoleMode(k.GetStdHandle(-11),7)
        self.trace = False

    def write(self, text):
        print("\033[33;1;40m\033[0K" + text + "\033[0K\033[0m")
        
    def dump(self, text):
        print("\033[36;40m\033[0K # " + text.replace("\n", "\n # ") + "\033[0K\033[0m")
    
    def log(self, text):
        if self.trace:
            print("\033[31;1;40m\033[0K # " + text.replace("\n", "\n # ") + "\033[0K\033[0m")
        
    def read(self):
        print("\033[37;1;40m\033[0K")
        try:
            command = raw_input("??? > ")
        except:
            command = input("??? > ")
        print("\033[0K\033[0m")
        return command
        
#-------------------------------------------------------------------------

