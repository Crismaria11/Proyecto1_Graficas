import struct
from obj import Obj

def char(c):
  return struct.pack('=c', c.encode('ascii'))

def word(c):
  return struct.pack('=h', c)

def dword(c):
  return struct.pack('=l', c)

def color(r, g, b):
  return bytes([b, g, r])



class Render(object):
  def __init__(self):
    self.framebuffer = []

  def glFinish(self, filename):
    f = open(filename, 'bw')

    #file header
    f.write(char('B'))
    f.write(char('M'))
    f.write(dword(14 + 40 + self.width * self.height * 3))
    f.write(dword(0))
    f.write(dword(14 + 40))


    # image loader
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


    # pixel data
    for x in range(self.width):
      for y in range(self.height):
        f.write(self.framebuffer[x][y])


    f.close()

  def glInit(self):
    pass

  def glCreateWindow(self, width, height):
    self.width = width
    self.height = height

  def glViewPort(self, x, y, width, height):
    self.xVPort = x
    self.yVPort = y
    self.widthVPort = width
    self.heightVPort = height

  def glClear(self):
    self.framebuffer = [
      [color(0, 0, 0) for x in range(self.width)]
      for y in range(self.height)
    ]

  def glClearColor(self, r, g, b):
    self.framebuffer = [
      [color(round(r * 255), round(g * 255), round(b * 255)) for x in range(self.width)]
      for y in range(self.height)
    ]

  def glVertex(self, x, y):
    xVertex = round(((x + 1) * (self.widthVPort/2)) + self.xVPort)
    yVertex = round(((y + 1) * (self.heightVPort/2)) + self.yVPort)
    self.framebuffer[xVertex][yVertex] = self.foreground

  def glColor(self, r=2, g=2, b=2):
    red = round(r * 255)
    green = round(g * 255)
    blue = round(b * 255)
  
    self.foreground = color(red, green, blue)


  def point(self, x, y):
    try: 
      self.framebuffer[y][x] = self.foreground
    except:
      pass


  # segunda entrega
  def line(self, x1, y1, x2, y2):
    dy = abs(y2 - y1)
    dx = abs(x2 - x1)

    steep = dy > dx
    
    if steep: 
      x1, y1 = y1, x1
      x2, y2 = y2, x2

    if x1 > x2:
      x1, x2 = x2, x1
      y1, y2 = y2, y1

    dy = abs(y2 - y1)
    dx = abs(x2 - x1)

    offset = 0
    threshold = dx

    y = y1
    for x in range(x1, x2):
      if steep:
        self.point(y, x)
      else:
        self.point(x, y)

      offset += dy * 2
      if offset >= threshold:
        y += 1 if y1 < y2 else -1
        threshold += 2 * dx

  def load(self, filename, translate, scale):
    model = Obj(filename)
    for face in model.faces:
      vcount = len(face)

      for j in range(vcount):
        vertexIndex1 = face[j][0] - 1
        vertexIndex2 = face[(j + 1) % vcount][0] - 1

        vertice1 = model.vertices[vertexIndex1]
        vertice2 = model.vertices[vertexIndex2]

        x1 = round((vertice1[0] * scale[0]) + translate[0])
        y1 = round((vertice1[1] * scale[1]) + translate[1])
        x2 = round((vertice2[0] * scale[0]) + translate[0])
        y2 = round((vertice2[1] * scale[1]) + translate[1])
      

        self.line(x1, y1, x2, y2)




    
bitmap = Render()

# tonos excelentes para baby yoda
bitmap.glCreateWindow(600,600)
bitmap.glClear()
bitmap.glClearColor(0, 0, 0)
bitmap.glColor(0.1, 1, 0.1)
bitmap.glViewPort(100, 100, 100, 100)
# bitmap.glVertex(0,0)

# bitmap.line(10, 100, 30, 10)

bitmap.load('./Modelos/baby-yoda-phone-stand/baby-yoda-phone-stand.obj', translate=[300, 100], scale=[3,3])
# bitmap.load('./Modelos/tigre_sumatra_sketchfab.obj', translate=[300, 300], scale=[500,500])


bitmap.glFinish('out.bmp')