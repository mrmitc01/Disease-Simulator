import math
class Disease:
    def __init__(self, action, infectivity, ):
        self.action = action
        self.infectivity = infectivity

    def run(self):    
        if self.action == 'run':
            return('run')
