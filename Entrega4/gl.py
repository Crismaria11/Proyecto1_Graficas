import struct
from obj import Obj
from collections import namedtuple

# ================================
# Vertex classes
# ================================
Vertex2 = namedtuple('Vertex2', ['x', 'y'])
Vertex3 = namedtuple('Vertex3', ['x', 'y', 'z'])


def char(c):
  return struct.pack('=c', c.encode('ascii'))

def word(c):
  return struct.pack('=h', c)

def dword(c):
  return struct.pack('=l', c)

def color(r, g, b):
  return bytes([b, g, r])

def sum(v0, v1):
  return Vertex3(v0.x + v1.x, v0.y + v1.y, v0.z + v1.z)

def sub(v0, v1):
  return Vertex3(v0.x - v1.x, v0.y - v1.y, v0.z - v1.z)

def mul(v0, k):
  return Vertex3(v0.x * k, v0.y * k, v0.z * k)

def dot(v0, v1):
  return v0.x * v1.x + v0.y * v1.y + v0.z * v1.z

def length(v0):
  return (v0.x**2 + v0.y**2 + v0.z**2)**0.5

def norm(v0):
  v0length = length(v0)
  if not v0length:
    return Vertex3(0, 0, 0)

  return Vertex3(v0.x/v0length, v0.y/v0length, v0.z/v0length)

def bbox(*vertices):
  xs = [vertex.x for vertex in vertices]
  ys = [vertex.y for vertex in vertices]

  xs.sort()
  ys.sort()

  return xs[0], xs[-1], ys[0], ys[-1]

def cross(v1, v2):
  return Vertex3(
    v1.y * v2.z - v1.z * v2.y,
    v1.z * v2.x - v1.x * v2.z,
    v1.x * v2.y - v1.y * v2.x
  )


def barycentric(A, B, C, P):
  cx, cy, cz = cross(
    Vertex3(B.x - A.x, C.x - A.x, A.x - P.x),
    Vertex3(B.y - A.y, C.y - A.y, A.y - P.y)
  )

  if abs(cz) < 1:
    return -1, -1, -1

  u = cx / cz
  v = cy / cz
  w = 1 - (cx + cy) / cz

  return w, v, u  



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
    self.zbuffer = [
      [-float('inf') for x in range(self.width)]
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


  def point(self, x, y, color = None):
    try: 
      self.framebuffer[y][x] = color or self.foreground
      # self.framebuffer[y][x] = color or self.current_color
    except:
      pass
  
  def set_color(self, color, r, g, b):
    self.current_color = color(r, g, b)


  # segunda entrega
  def glLine(self, A, B):
    x1 = A.x
    x2 = B.x
    y1 = A.y
    y2 = B.y

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
    light = Vertex3(0, 0, 1)
    for face in model.faces:
      vcount = len(face)
      
      if vcount == 3:
        f1 = face[0][0] - 1
        f2 = face[1][0] - 1
        f3 = face[2][0] - 1

        v1 = Vertex3(model.vertices[f1][0], model.vertices[f1][1], model.vertices[f1][2])
        v2 = Vertex3(model.vertices[f2][0], model.vertices[f2][1], model.vertices[f2][2])
        v3 = Vertex3(model.vertices[f3][0], model.vertices[f3][1], model.vertices[f3][2])

        x1 = round((v1.x * scale[0]) + translate[0])
        y1 = round((v1.y * scale[1]) + translate[1])
        z1 = round((v1.z * scale[2]) + translate[2])

        x2 = round((v2.x * scale[0]) + translate[0])
        y2 = round((v2.y * scale[1]) + translate[1])
        z2 = round((v2.z * scale[2]) + translate[2])

        x3 = round((v3.x * scale[0]) + translate[0])
        y3 = round((v3.y * scale[1]) + translate[1])
        z3 = round((v3.z * scale[2]) + translate[2])

        A = Vertex3(x1, y1, z1)
        B = Vertex3(x2, y2, z2)
        C = Vertex3(x3, y3, z3)

        normal = cross(sub(B, A), sub(C, A))
        intensity = dot(norm(normal), light)
        grey = round(255 * intensity)
        if grey < 0:
          continue
        intensity_color = color(grey, grey, grey)
        self.triangle(A, B, C, intensity_color)

      if vcount == 4:
        f1 = face[0][0] - 1
        f2 = face[1][0] - 1
        f3 = face[2][0] - 1
        f4 = face[3][0] - 1

        v1 = Vertex3(model.vertices[f1][0], model.vertices[f1][1], model.vertices[f1][2])
        v2 = Vertex3(model.vertices[f2][0], model.vertices[f2][1], model.vertices[f2][2])
        v3 = Vertex3(model.vertices[f3][0], model.vertices[f3][1], model.vertices[f3][2])
        v4 = Vertex3(model.vertices[f4][0], model.vertices[f4][1], model.vertices[f4][2])

        x1 = round((v1.x * scale[0]) + translate[0])
        y1 = round((v1.y * scale[1]) + translate[1])
        z1 = round((v1.z * scale[2]) + translate[2])

        x2 = round((v2.x * scale[0]) + translate[0])
        y2 = round((v2.y * scale[1]) + translate[1])
        z2 = round((v2.z * scale[2]) + translate[2])

        x3 = round((v3.x * scale[0]) + translate[0])
        y3 = round((v3.y * scale[1]) + translate[1])
        z3 = round((v3.z * scale[2]) + translate[2])

        x4 = round((v4.x * scale[0]) + translate[0])
        y4 = round((v4.y * scale[1]) + translate[1])
        z4 = round((v4.z * scale[2]) + translate[2])

        A = Vertex3(x1, y1, z1)
        B = Vertex3(x2, y2, z2)
        C = Vertex3(x3, y3, z3)
        D = Vertex3(x4, y4, z4)

        normal = cross(sub(B, A), sub(C, A))
        intensity = dot(norm(normal), light)
        grey = round(255 * intensity)
        if grey < 0:
          continue
        intensity_color = color(grey, grey, grey)

        # A, B, C, D = vertices
        
        self.triangle(A, B, C, intensity_color)
        self.triangle(A, C, D, intensity_color)
      
        
  
  # parte opcional
  def triangleInicial(self, A, B, C, color = (0, 244, 0)):
    if A.y > B.y:
      A, B = B, A
    if A.y > C.y:
      A, C = C, A
    if B.y > C.y:
      B, C = C, B

    dx_ac = C.x - A.x
    dy_ac = C.y - A.y
    if dy_ac == 0:
      return
    mi_ac = dx_ac / dy_ac

    
    dx_ab = B.x - A.x
    dy_ab = B.y - A.y


    if dy_ab != 0:
      mi_ab = dx_ab / dy_ab

      for y in range(A.y, B.y + 1):
        xi = round(A.x - mi_ac * (A.y - y))
        xf = round(A.x - mi_ab * (A.y - y))

        if xi > xf:
          xi, xf = xf, xi

        # linea entre xi y xf
        for x in range(xi, xf + 1):
          self.point(x, y, color)

    dx_bc = C.x - B.x
    dy_bc = C.y - B.y
    

    if dy_bc != 0:
      mi_bc = dx_bc / dy_bc

      for y in range(B.y, C.y + 1):
        xi = round(A.x - mi_ac * (A.y - y))
        xf = round(B.x - mi_bc * (B.y - y))

        if xi > xf:
          xi, xf = xf, xi 

        # linea entre xi y xf
        for x in range(xi, xf + 1):
          self.point(x, y, color)


  def triangle(self, A, B, C, color = (0, 244, 0)):
    xmin, xmax, ymin, ymax = bbox(A, B, C)

    for x in range(xmin, xmax + 1):
      for y in range(ymin, ymax + 1):
        P = Vertex2(x, y)
        w, v, u = barycentric(A, B, C, P)
        if w < 0 or v < 0 or u < 0:
          # el punto esta afuera
          continue

        z = A.z * w + B.z * v + C.z * u

        try:
          if z > self.zbuffer[x][y]:
            self.point(x, y, color)
            self.zbuffer[x][y] = z 
        except:
          pass

  def transform(self, vertex, translate=(0, 0, 0), scale=(1, 1, 1)):
    return Vertex3(
      round((vertex[0] + translate[0]) * scale[0]),
      round((vertex[1] + translate[1]) * scale[1]),
      round((vertex[2] + translate[2]) * scale[2])
    )
    
bitmap = Render()

# tonos excelentes para baby yoda
bitmap.glCreateWindow(800, 800)
bitmap.glClear()
bitmap.glClearColor(0, 0, 0)
bitmap.glColor(0.1, 1, 0.1)
bitmap.glViewPort(0, 0, 100, 100)
# bitmap.glVertex(0,0)

# bitmap.line(10, 100, 30, 10)

# bitmap.load('./Modelos/0.obj', translate=[400, 200, 200], scale=[300, 300, 300])
bitmap.load('./Modelos/BabyYoda.obj', translate=[400, 400, 400], scale=[200, 200, 200])
# bitmap.load('./Modelos/ig11.obj', translate=[400, 150, 100], scale=[300, 300, 300])
# bitmap.load('./Modelos/face.obj', translate=[400, 300, 30], scale=[10, 10, 10])

bitmap.glFinish('out.bmp')