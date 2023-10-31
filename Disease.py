import math
class Disease:
    def __init__(self, trans_type, trans_param, rect_width, rect_height):
        self.trans_type = trans_type
        self.trans_param = trans_param

        self.rectangle = {'width': rect_width, 'height': rect_height}
        self.pointA = [0, 0]
        self.pointB = [0, self.rectangle['height']]
        self.pointC = [self.rectangle['width'], self.rectangle['height']]
        self.pointD = [self.rectangle['width'], 0]
        #print("Starting Rectangle Width:",self.rectangle['width'],"Height:", self.rectangle['height'])
        print(f"Rectangle Coordinates BEFORE run:", self.pointA, self.pointB, self.pointC, self.pointD)

    def beefus(self):
        print("beefus")
        
    def translate(self):    
        if self.trans_type == 'translation':
            self.pointA[0] += self.trans_param
            self.pointB[0] += self.trans_param
            self.pointC[0] += self.trans_param
            self.pointD[0] += self.trans_param
            #print(f"Rectangle AFTER X Translation: Width = {abs(self.pointC[0]-self.pointB[0])}, Height = {self.pointC[1]}")
            print(f"Rectangle Coordinates AFTER translation:", self.pointA, self.pointB, self.pointC, self.pointD)
            return(self.pointA, self.pointB, self.pointC, self.pointD)

    def rotate(self):
        if self.trans_type == 'rotation':
            xb, yb = self.pointB
            xc, yc = self.pointC
            xd, yd = self.pointD
            radians = self.trans_param * 3.141592653589793/180
            nxb = (math.cos(radians) * (xb)) - (math.sin(radians) * (yb))
            nxc = math.cos(radians) * (xc) - math.sin(radians) * (yc)
            nxd = math.cos(radians) * (xd) - math.sin(radians) * (yd)
            self.pointB[0] = round(nxb)
            self.pointC[0] = round(nxc)
            self.pointD[0] = round(nxd)
            #print(f"Rectangle AFTER X Rotation: Width = {abs(self.pointC[0]-self.pointB[0])}, Height = {self.pointC[1]}")
            print(f"Rectangle Coordinates AFTER rotation:", self.pointA, self.pointB, self.pointC, self.pointD)
            return(self.pointA, self.pointB, self.pointC, self.pointD)

    def shear(self):
        if self.trans_type == 'shear':
            nxa = self.pointA[0] + self.trans_param * self.pointA[1]
            nxb = self.pointB[0] + self.trans_param * self.pointB[1]
            nxc = self.pointC[0] + self.trans_param * self.pointC[1]
            nxd = self.pointD[0] + self.trans_param * self.pointD[1]
            self.pointA[0] = round(nxa)
            self.pointB[0] = round(nxb)
            self.pointC[0] = round(nxc)
            self.pointD[0] = round(nxd)

            #print(f"Rectangle AFTER X Shear: Width = {abs(self.pointC[0]-self.pointB[0])}, Height = {self.pointC[1]}")
            print(f"Rectangle Coordinates AFTER shear:", self.pointA, self.pointB, self.pointC, self.pointD)
            return(self.pointA, self.pointB, self.pointC, self.pointD)

    def scale(self):
        if self.trans_type == 'scale':
            nxa = self.pointA[0] * self.trans_param 
            nxb = self.pointB[0] * self.trans_param 
            nxc = self.pointC[0] * self.trans_param
            nxd = self.pointD[0] * self.trans_param
            self.pointA[0] = round(nxa)
            self.pointB[0] = round(nxb)
            self.pointC[0] = round(nxc)
            self.pointD[0] = round(nxd)
            #print(f"Rectangle AFTER X Translation: Width = {abs(self.pointC[0]-self.pointB[0])}, Height = {self.pointC[1]}")
            print(f"Rectangle Coordinates AFTER scale:", self.pointA, self.pointB, self.pointC, self.pointD)
            return(self.pointA, self.pointB, self.pointC, self.pointD)


if __name__ == "__main__":

    #information to be changed as needed:

    #Rectangle size defs
    rect_width = 60
    rect_height = 40

    #by x units
    translation_param = 2
    #by degrees
    rotation_param = 60
    #by shear factor
    shear_param = 4
    #by scale factor
    scale_param = 1.5


    #Enter in the format trans_type, trans_param, rect_width, rect_height
    disease = Disease('translation', translation_param, rect_width, rect_height)
    disease.translate()

    disease = Disease('rotation', rotation_param, rect_width, rect_height)
    disease.rotate()
    
    disease = Disease('shear', shear_param, rect_width, rect_height)
    disease.shear()

    disease = Disease('scale', scale_param, rect_width, rect_height)
    disease.scale()
