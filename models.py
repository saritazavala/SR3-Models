import struct 

def char(c):
    return struct.pack('=c', c.encode('ascii'))

# 2 bytes
def word(c):
    return struct.pack('=h', c)

# 4 bytes
def dword(c):
    return struct.pack('=l', c)

def color(r, g, b):
    return bytes([round(b * 255), round(g * 255), round(r * 255)])


class Render(object):

    def __init__(self, width, height):
 
        self.width = width
        self.height = height
        self.framebuffer = []
        self.clear_color = color(0.5,1,0.7)
        self.glClear()

    def glClear(self):
        self.framebuffer = [
            [self.clear_color for x in range(self.width)]
            for y in range(self.height)
        ]
    
    def glClearColor(self, r,g,b):
        self.current_color = color(r, g, b)


    def glCreateWindow(self, width, height):
        self.height = height
        self.width = width

    def glColor(self, r, g, b):
        self.current_color = color(r, g, b)

    def glViewPort(self, x, y, width, height):
        self.xViewPort = x
        self.yViewPort = y
        self.widthViewPort = width
        self.heightViewPort = height
    
    def glVertex(self, x, y):
        x_temp = round(self.widthViewPort/2 + x * self.widthViewPort/2)
        y_temp = round(self.heightViewPort/2 + y * self.heightViewPort/2)
        x_point = self.xViewPort + x_temp
        y_point = self.yViewPort + y_temp
        self.point(round(x_point),round(y_point))
        

    def point(self,x,y):
        self.framebuffer[x][y] = color(0,0,0)



    def glLine(self, x0, y0, x1, y1):
        x0 = round(self.widthViewPort/2 + x0 * self.widthViewPort/2)
        y0 = round(self.heightViewPort/2 + y0 * self.heightViewPort/2)
        x1 = round(self.widthViewPort/2 + x1 * self.widthViewPort/2)
        y1 = round(self.heightViewPort/2 + y1 * self.heightViewPort/2)
 
        #diferenciales
        dy = abs(y1 - y0)
        dx = abs(x1 - x0)
        steep = dy > dx
        
        if steep:
            x0, y0 = y0, x0
            x1, y1 = y1, x1
            dy = abs(y1 - y0)
            dx = abs(x1 - x0)
        
        if x0 > x1:
            x0, x1 = x1, x0
            y0, y1 = y1, y0
            
        offset = 0
        threshold = 1
        y = y0
        for x in range(x0, x1):
            if steep:
                self.point(y, x)
            else:
                self.point(x, y)
                
            offset += dy * 2
            
            if offset >= threshold:
                y += 1 if y0 < y1 else -1
                threshold += 2 * dx
            



    def write(self, filename):
        f = open(filename, 'bw')
        #File header
        f.write(char('B'))
        f.write(char('M'))
        f.write(dword(14+40+self.width+self.height*3))
        f.write(dword(0))
        f.write(dword(14 + 40))

        #info header
        f.write(dword(40))
        f.write(dword(self.width))
        f.write(dword(self.height))
        f.write(word(1))
        f.write(word(24))
        f.write(dword(0))
        f.write(dword(self.width * self.height * 3))
        f.write(dword(0))
        f.write(dword(0))
        f.write(dword(0))
        f.write(dword(0))

        #Pixel data
        for x in range(self.height):
            for y in range(self.width):
                f.write(self.framebuffer[x][y])
        f.close()


render = Render(800,600)
render.glCreateWindow(800, 600)
render.glViewPort(0, 0, 10, 10)
render.glClear()
render.glColor(1, 0, 0)
render.glColor(0,0,0)
render.glLine(-1, -1, 0, 0)

render.write("alooo.bmp")