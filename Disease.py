"""
Defines a Disease class with transformation methods (translate, rotate, shear, scale).
"""

import math


# Represents a disease with transformation parameters for translation, rotation, shear, and scale.
class Disease:
    def __init__(self, action, infectivity, ):
        self.action = action
        self.infectivity = infectivity

    def run(self):    
        if self.action == 'run':
            return('run')

