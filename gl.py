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
  def glInit(self, width, height):
    self.width = width
    self.height = height
    self.framebuffer = []
    self.clear()


  def clear(self):
    self.framebuffer = [
      [color(0, 0, 0) for x in range(self.width)]
      for y in range(self.height)
    ]


  def write(self, filename):
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
    f.write(dword(1))
    f.write(dword(24))
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

  def point(self, x, y):
    self.framebuffer[x][y] = color(123, 123, 123)

bitmap = Render(1000, 1000)
bitmap.point(2, 3)
bitmap.point(5, 5)
bitmap.write('out.bmp')