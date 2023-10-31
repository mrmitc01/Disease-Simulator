import math
class Disease:
    def __init__(self, trans_type, trans_param, rect_width, rect_height):
        self.trans_type = trans_type
        self.trans_param = trans_param

    def translate(self):    
        if self.trans_type == 'translation':
            return(self.pointA, self.pointB, self.pointC, self.pointD)

    def rotate(self):
        if self.trans_type == 'rotation':
            
            return(self.pointA, self.pointB, self.pointC, self.pointD)

    def shear(self):
            if self.trans_type == 'shear':
                return(self.pointA, self.pointB, self.pointC, self.pointD)

    def scale(self):
        if self.trans_type == 'scale':
            return(self.pointA, self.pointB, self.pointC, self.pointD)