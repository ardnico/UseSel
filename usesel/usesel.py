from .handler.handle_webelement import handle_webelement

class EasySelenium(handle_webelement):
    def __init__(self,**kwargs) ->None:
        super().__init__(**kwargs)
    
        
        