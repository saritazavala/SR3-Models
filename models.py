#SR3-MODELS
#Graficas 
#Sara Zavala 18893
#Universidad del Valle

import struct 
from Obj import Obj

def char(c):
    return struct.pack('=c', c.encode('ascii'))

# 2 bytes
def word(c):
    return struct.pack('=h', c)

# 4 bytes
def dword(c):
    return struct.pack('=l', c)

def color(red, green, blue):
     return bytes([round(blue * 255), round(green * 255), round(red * 255)])


class Render(object):

    #Initial values -------------------------------

    def __init__(self, filename):
        self.width = 0
        self.height = 0
        self.framebuffer = []
        self.change_color = color(1,1,1)
        self.filename = filename
        self.x_position = 0
        self.y_position = 0
        self.ViewPort_height = 0
        self.ViewPort_width = 0
        self.glClear()

    
    #File Header ----------------------------------

    def header(self):
        doc = open(self.filename,'bw')
        doc.write(char('B'))
        doc.write(char('M'))
        doc.write(dword(54 + self.width * self.height * 3))
        doc.write(dword(0))
        doc.write(dword(54))
        self.info(doc)
        
        
    #Info header ---------------------------------------

    def info(self, doc):
        doc.write(dword(40))
        doc.write(dword(self.width))
        doc.write(dword(self.height))
        doc.write(word(1))
        doc.write(word(24))
        doc.write(dword(0))
        doc.write(dword(self.width * self.height * 3))
        doc.write(dword(0))
        doc.write(dword(0))
        doc.write(dword(0))
        doc.write(dword(0))
        
        #Image ----------------------------------
        for x in range(self.height):
            for y in range(self.width):
                doc.write(self.framebuffer[x][y])
        doc.close()

    #Cleans a full image with the color defined in "change_color"
    def glClear(self):
        self.framebuffer = [
            [self.change_color for x in range(self.width)]
            for y in range(self.height)
        ]

    #Takes a new color  
    def glClearColor(self, red,blue,green):
        self.change_color = color(red,blue,green)

    #Writes all the doc
    def glFinish(self):
        self.header()
    
    def glColor(self, red, green, blue):
        self.change_color = color(red, green, blue)

    #Draws a point according ot frameBuffer
    def glpoint(self, x, y):
        self.framebuffer[y][x] = self.change_color


    #Creates a window 
    def glCreateWindow(self, width, height):
        self.width = width
        self.height = height

    #Defines the area where will be able to draw
    def glViewPort(self, x_position, y_position,  ViewPort_width, ViewPort_height):
        self.x_position = x_position
        self.y_position = y_position
        self.ViewPort_height = ViewPort_height
        self.ViewPort_width = ViewPort_width
    
    #Compuse el vertex por que me daba error el range
    def glVertex(self, x, y):
        x_temp  = round((x + 1) * (self.ViewPort_width/ 2) + self.x_position)
        y_temp  = round((y + 1) * (self.ViewPort_height/2) + self.y_position)
        self.glpoint(round(x_temp ), round(y_temp ))


    #Codigo basado en codigo visto en clase
    #Dennis Aldana 2020

    def glLine(self, x1, y1, x2, y2):
        
        dy = abs(y2 - y1)
        dx = abs(x2 - x1)
        steep = dy > dx
        
        if steep:
            x1, y1 = y1, x1
            x2, y2 = y2, x2
            dy = abs(y2 - y1)
            dx = abs(x2 - x1)
        
        if x1 > x2:
            x1, x2 = x2, x1
            y1, y2 = y2, y1
            
        offset = 0
        threshold = 1
        y = y1
        for x in range(x1, x2):
            if steep:
                self.glpoint(y, x)
            else:
                self.glpoint(x, y)
                
            offset += dy * 2
            
            if offset >= threshold:
                y += 1 if y1 < y2 else -1
                threshold += 2 * dx
    
    #MODELS --------------------------------------

    def load_model(self, filename, scale, translate):
        model = Obj(filename)
        
        for face in model.faces:
            vcount = len(face)
            for position in range(vcount):
                vi_1 = int(face[position][0]) - 1
                vi_2 = int(face[(position + 1) % vcount][0]) - 1
                
                v1 = model.vertex[vi_1] 
                v2 = model.vertex[vi_2]
                
                x1 = round(v1[0] * scale[0] + translate[0])
                y1 = round(v1[1] * scale[1] + translate[1])
                x2 = round(v2[0] * scale[0] + translate[0])
                y2 = round(v2[1] * scale[1] + translate[1])
                
                self.glLine(x1, y1, x2, y2)
    

#Crear Render
r = Render('IronMan.bmp')
#Crear pantalla
r.glCreateWindow(1920, 1080)
#Tomo el bote de pintura de este color
r.glClearColor(0.75,0.13,0.13)
#Echo el bote de pintura y pinto todo
r.glClear()
#Amarillito
r.glColor(0.9,0.7,0.13)
r.load_model('./ironman.obj', scale=[3, 3], translate=[960, 100 ])
r.glFinish()


