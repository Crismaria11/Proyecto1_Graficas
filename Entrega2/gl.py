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
    red = round(r * 255)
    green = round(g * 255)
    blue = round(b * 255)
    self.background = color(red, green, blue)

  def glVertex(self, x, y):
    xVertex = round(((x + 1) * (self.widthVPort/2)) + self.xVPort)
    yVertex = round(((y + 1) * (self.heightVPort/2)) + self.yVPort)
    self.framebuffer[xVertex][yVertex] = self.foreground

  def glColor(self, r=2, g=2, b=2):
    red = round(r * 255)
    green = round(g * 255)
    blue = round(b * 255)
    # imitamos la funcion color
    self.foreground = color(red, green, blue)


  def point(self, x, y):
    self.framebuffer[x][y] = color(150, 75, 150)


bitmap = Render()

bitmap.glCreateWindow(200, 200)
bitmap.glClear()
bitmap.glClearColor(0, 0, 0)
bitmap.glColor(0.1, 1, 0.1)
bitmap.glViewPort(100, 100, 100, 100)
bitmap.glVertex(0,0)



# bitmap.point(2, 3)
# bitmap.point(5, 5)
bitmap.glFinish('out.bmp')