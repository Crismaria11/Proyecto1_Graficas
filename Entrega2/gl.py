import struct
from collections import namedtuple

def char(c):
  return struct.pack('=c', c.encode('ascii'))

def word(c):
  return struct.pack('=h', c)

def dword(c):
  return struct.pack('=l', c)

def color(r, g, b):
  return bytes([b, g, r])


V2 = namedtuple('Vertex2', ['x', 'y'])
V3 = namedtuple('Vertex3', ['x', 'y'])



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
        f.write(self.framebuffer[y][x])


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

  def glColor(self, r, g, b):
    red = round(r * 255)
    green = round(g * 255)
    blue = round(b * 255)
    self.foreground = color(red, green, blue)


  def point(self, x, y):
    self.framebuffer[y][x] = self.foreground


  # segunda entrega
  def glLine(self, x1, y1, x2, y2):
    x1 = round(((x1 + 1) * (self.widthVPort/2)) + self.xVPort)
    x2 = round(((x2 + 1) * (self.widthVPort/2)) + self.xVPort)
    y1 = round(((y1 + 1) * (self.heightVPort/2)) + self.yVPort)
    y2 = round(((y2 + 1) * (self.heightVPort/2)) + self.yVPort)

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

  


  

    
bitmap = Render()

bitmap.glCreateWindow(200, 100)
bitmap.glClear()
bitmap.glClearColor(0.1, 0.3, 0.8)
bitmap.glColor(1, 0.2, 1)
bitmap.glViewPort(50, 0, 50, 30)
# bitmap.glVertex(0,0)

bitmap.glLine(0.25, 0.9, 0.25, -1)

bitmap.glFinish('out.bmp')