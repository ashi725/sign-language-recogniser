from abc import ABC, abstractmethod

'''
All tabs should implement this interface. It defines an abstract method that is called
whenever the tab is pressed.
'''
class TabBaseAbstractClass():
    '''
    This method would be called if the user presses on a tab. This allows
    user to update the GUI on load.
    '''
    @abstractmethod
    def refreshWindowOnLoad(self):
        pass