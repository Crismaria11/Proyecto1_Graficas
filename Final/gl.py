from obj import Obj, Texture
from mathlibrary import *
import math


class Render(object):
  def __init__(self, width, height):
    self.width = width
    self.height = height
    self.light = V3(0, 0, 1)
    self.current_color = color(0, 0, 0)
    self.glClear()
    self.active_vertex_array = []
    self.active_texture = None
    self.active_shader = None

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

  
  def glClear(self):
    self.framebuffer = [
      [color(0, 0, 0) for x in range(self.width)]
      for y in range(self.height)
    ]
    self.zbuffer = [
      [-float('inf') for x in range(self.width)]
      for y in range(self.height)
    ]


  def glColor(self, r=2, g=2, b=2):
    red = round(r * 255)
    green = round(g * 255)
    blue = round(b * 255)
  
    self.current_color = color(red, green, blue)


  def point(self, x, y, color = None):
    try: 
      # self.framebuffer[y][x] = color or self.foreground
      self.framebuffer[y][x] = color or self.current_color
    except:
      pass
  
  def set_color(self, color, r, g, b):
    self.current_color = color(r, g, b)


  # segunda entrega
  def glLine(self, x0, y0, x1, y1):
    x1, y1 = x0, y0
    x2, y2 = x1, y1

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
    for x in range(x1, x2 + 1):
      if steep:
        self.point(y, x)
      else:
        self.point(x, y)

      offset += dy * 2
      if offset >= threshold:
        y += 1 if y1 < y2 else -1
        threshold += 2 * dx

  def triangle(self):
    A = next(self.active_vertex_array)
    B = next(self.active_vertex_array)
    C = next(self.active_vertex_array)
    
    if self.active_texture:
      tA = next(self.active_vertex_array)
      tB = next(self.active_vertex_array)
      tC = next(self.active_vertex_array)

      nA = next(self.active_vertex_array)
      nB = next(self.active_vertex_array)
      nC = next(self.active_vertex_array)

    xmin, xmax, ymin, ymax = bbox(A, B, C)

    normal = norm(cross(sub(B, A), sub(C, A)))
    intensity = dot(normal, self.light)
    if intensity < 0:
      return

    for x in range(round(xmin), round(xmax) + 1):
      for y in range(round(ymin), round(ymax) + 1):
        P = V2(x, y)
        w, v, u = barycentric(A, B, C, P)
        if w < 0 or v < 0 or u < 0:
          # el punto esta afuera
          continue

        if self.active_texture:
          tx = tA.x * w + tB.x * u + tC.x * v
          ty = tA.y * w + tB.y * u + tC.y * v

          self.current_color = self.active_shader(
            self,
            triangle=(A, B, C),
            bar=(w, v, u),
            texture_coords=(tx, ty),
            varying_normals=(nA, nB, nC)
          )
        else:
          self.current_color = color(round(255 * intensity), 0, 0)

        z = A.z * w + B.z * v + C.z * u
        if x < 0 or y < 0:
          continue

        if x < len(self.zbuffer) and y < len(self.zbuffer[x]) and z > self.zbuffer[y][x]:
          self.point(x, y)
          self.zbuffer[y][x] = z



  def load(self, filename, translate=(0, 0, 0), scale=(1, 1, 1), rotate=(0, 0, 0)):
    self.loadModelMatrix(translate, scale, rotate)
    model = Obj(filename)
    vertex_buffer_object = []
    
    for face in model.faces:
      vcount = len(face)
      
      if vcount == 3:
        for facepart in face:
          vertex = self.transform(V3(*model.vertices[facepart[0]-1]))
          vertex_buffer_object.append(vertex)

          if self.active_texture:
            for facepart in face:
              tvertex = V2(*model.tvertices[facepart[1]-1])
              vertex_buffer_object.append(tvertex)

            for facepart in face:
              nvertex = V3(*model.normals[facepart[2]-1])
              vertex_buffer_object.append(nvertex)
        
      elif vcount == 4:
        for faceindex in [0,1,2]:
          facepart = face[faceindex]
          vertex = self.transform(V3(*model.vertices[facepart[0]-1]))
          vertex_buffer_object.append(vertex)
          try:
            if self.active_texture:
              for faceindex in range(0,3):
                facepart = face[faceindex]
                tvertex = V2(*model.tvertices[facepart[1]-1])
                vertex_buffer_object.append(tvertex)

              for faceindex in range(0,3):
                facepart = face[faceindex]
                nvertex = V3(*model.normals[facepart[2]-1])
                vertex_buffer_object.append(nvertex)

              #segundo triangulo que forma el cuadrado
              for faceindex in [3,0,2]:
                facepart = face[faceindex]
                vertex = self.transform(V3(*model.vertices[facepart[0]-1]))
                vertex_buffer_object.append(vertex)

              if self.active_texture:
                for faceindex in [3,0,2]:
                  facepart = face[faceindex]
                  tvertex = V2(*model.tvertices[facepart[1]-1])
                  vertex_buffer_object.append(tvertex)

                for faceindex in [3,0,2]:
                  facepart = face[faceindex]
                  nvertex = V3(*model.normals[facepart[2]-1])
                  vertex_buffer_object.append(nvertex)
          except:
            pass  
    self.active_vertex_array = iter(vertex_buffer_object)
        
      

  
  def transform(self, vertex):
    augmented_vertex = [
      [vertex.x],
      [vertex.y],
      [vertex.z],
      [1]
    ]
    transformed_vertex = multMatriz(self.Viewport, self.Projection)
    transformed_vertex = multMatriz(transformed_vertex, self.View)
    transformed_vertex = multMatriz(transformed_vertex, self.Model)
    transformed_vertex = multMatriz(transformed_vertex, augmented_vertex)

    transformed_vertex = [
      (transformed_vertex[0][0]),
      (transformed_vertex[1][0]),
      (transformed_vertex[2][0]),
    ]
    
    return V3(*transformed_vertex)

  def loadModelMatrix(self, translate=(0, 0, 0), scale=(1, 1, 1), rotate=(0, 0, 0)):
    translate = V3(*translate)
    scale = V3(*scale)
    rotate = V3(*rotate)

    translation_matrix = [
      [1, 0, 0, translate.x],
      [0, 1, 0, translate.y],
      [0, 0, 1, translate.z],
      [0, 0, 0, 1],
    ]


    a = rotate.x
    rotation_matrix_x = [
      [1, 0, 0, 0],
      [0, math.cos(a), -math.sin(a), 0],
      [0, math.sin(a),  math.cos(a), 0],
      [0, 0, 0, 1]
    ]

    a = rotate.y
    rotation_matrix_y = [
      [math.cos(a), 0,  math.sin(a), 0],
      [     0, 1,       0, 0],
      [-math.sin(a), 0,  math.cos(a), 0],
      [     0, 0,       0, 1]
    ]

    a = rotate.z
    rotation_matrix_z = [
      [math.cos(a), -math.sin(a), 0, 0],
      [math.sin(a),  math.cos(a), 0, 0],
      [0, 0, 1, 0],
      [0, 0, 0, 1]
    ]

    rotation_matrix = multMatriz(rotation_matrix_x, rotation_matrix_y)
    rotation_matrix = multMatriz(rotation_matrix, rotation_matrix_z)

    scale_matrix = [
      [scale.x, 0, 0, 0],
      [0, scale.y, 0, 0],
      [0, 0, scale.z, 0],
      [0, 0, 0, 1],
    ]

    multMatrizodelo = multMatriz(translation_matrix, rotation_matrix) 
    self.Model = multMatriz(multMatrizodelo, scale_matrix)

  def loadViewMatrix(self, x, y, z, center):
    M = [
      [x.x, x.y, x.z,  0],
      [y.x, y.y, y.z, 0],
      [z.x, z.y, z.z, 0],
      [0,     0,   0, 1]
    ]

    O = [
      [1, 0, 0, -center.x],
      [0, 1, 0, -center.y],
      [0, 0, 1, -center.z],
      [0, 0, 0, 1]
    ]

    self.View = multMatriz(M, O)

  def loadProjectionMatrix(self, coeff):
    self.Projection =  [
      [1, 0, 0, 0],
      [0, 1, 0, 0],
      [0, 0, 1, 0],
      [0, 0, coeff, 1]
    ]

  def loadViewportMatrix(self, x = 0, y = 0):
    self.Viewport =  [
      [self.width/2, 0, 0, x + self.width/2],
      [0, self.height/2, 0, y + self.height/2],
      [0, 0, 128, 128],
      [0, 0, 0, 1]
    ]

  def lookAt(self, eye, center, up):
    z = norm(sub(eye, center))
    x = norm(cross(up, z))
    y = norm(cross(z, x))
    self.loadViewMatrix(x, y, z, center)
    self.loadProjectionMatrix(-1 / length(sub(eye, center)))
    self.loadViewportMatrix()

  def draw_arrays(self, polygon):
    if polygon == 'TRIANGLES':
      try:
        while True:
          self.triangle()
      except StopIteration:
        print('Un modelo terminado.')

      
    


# aqui sucede la magia 
# bitmap = Render(800, 600)
# bitmap.light = V3(0, 0, 1)

# # un iconico background
# t = Texture('./Texturas/fondo.bmp')
# bitmap.framebuffer = t.pixels
# bitmap.active_shader = alfo
# bitmap.lookAt(V3(1, 0, 100), V3(0, 0, 0), V3(0, 1, 0))
# bitmap.glFinish('out.bmp')




# tonos excelentes para baby yoda
# bitmap.glCreateWindow(800, 800)
# bitmap.glClear()
# bitmap.glClearColor(0, 0, 0)
# bitmap.glColor(0.1, 1, 0.1)
# bitmap.glViewPort(0, 0, 100, 100)
# bitmap.glVertex(0,0)

# bitmap.line(10, 100, 30, 10)

# bitmap.load('./Modelos/0.obj', translate=[400, 200, 200], scale=[300, 300, 300])
# bitmap.load('./Modelos/BabyYoda.obj', translate=[400, 400, 400], scale=[200, 200, 200])
# bitmap.load('./Modelos/ig11.obj', translate=[400, 150, 100], scale=[300, 300, 300])
# bitmap.load('./Modelos/face.obj', translate=[400, 300, 30], scale=[10, 10, 10])

# bitmap.glFinish('out.bmp')