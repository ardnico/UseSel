from .handler.use_selenium import use_selenium

class Usesel(use_selenium):
    def __init__(self,**kwargs) ->None:
        super().__init__(**kwargs)
