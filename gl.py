import struct

def char(c):
  return struct.pack('=c', c.encode('ascii'))

def word(c):
  return struct.pack('=h', c)

def dword(c):
  return struct.pack('=l', c)

def color(r, g, b):
  return bytes([b, g, r])



class Render(object):
  def __init__(self, width, height):
    self.width = width
    self.height = height
    self.framebuffer = []
    self.glClear()
    self.glCreateWindow(width, height)



  def glClear(self):
    self.framebuffer = [
      [color(0, 0, 0) for x in range(self.width)]
      for y in range(self.height)
    ]

  def glInit():
    pass

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

  def point(self, x, y):
    self.framebuffer[x][y] = color(40, 100, 40)

  def glCreateWindow(self, width, height):
    self.width = width
    self.height = height

  def glViewPort(self, x, y, width, height):
    self.x = x
    self.y = y
    self.width = width
    self.height = height

  def glClearColor(self, r, g, b):
    self.r = r
    self.g = g
    self.b = b


bitmap = Render(800, 800)
bitmap.point(2, 3)
bitmap.point(5, 5)
bitmap.glFinish('out.bmp')