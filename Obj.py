#Universidad del Valle
#Sara Zavala
#18893
#Graficas- SR3MODELS

class Obj(object):
    def __init__(self,filename):
        with open(filename) as f:
            self.lines = f.read().splitlines()
        self.vertex = []
        self.faces = []
        self.read()
            
    def read(self):
        for line in self.lines:
            splitable = len(line.split(' ')) > 1
            if splitable:
                prefix, value = line.split(' ', 1)
                
            if prefix == 'v':
                temp_vertex = []
                for v in value.split(' '):
                    if v != '':
                        temp_vertex.append(float(v))
                self.vertex.append(temp_vertex)
             
            elif prefix == 'f':
                temp_face = []
                for face in value.split(' '):
                    f = face.split('/')
                    if f != '':
                        temp_face.append(f)
                self.faces.append(temp_face)