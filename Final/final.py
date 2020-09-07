from gl import *
from shader import *
from obj import *

# aqui sucede la magia 
bitmap = Render(1200, 800)
bitmap.light = V3(0, 0, 1)

# un iconico background
print("Creando fondo")
t = Texture('./Texturas/fondo.bmp')
bitmap.framebuffer = t.pixels
bitmap.active_shader = alfo
bitmap.lookAt(V3(1, 0, 100), V3(0, 0, 0), V3(0, 1, 0))
bitmap.glFinish('out.bmp')
print("Fondo creado")

# un personaje
print("Personaje malo y luego bueno")
t = Texture('./Texturas/mando.bmp')
bitmap.active_shader = t
bitmap.active_shader = alfo
bitmap.lookAt(V3(1, 0, 3), V3(0, 0, 0), V3(0, 1, 0))
bitmap.load('./Modelos/mando.obj', translate=(-0.5, 0.5, 0), scale=(0.03, 0.03, 0.03), rotate=(0, 0.9, 0))
bitmap.draw_arrays('TRIANGLES')
bitmap.glFinish('out.bmp')
print("personaje finalizado")
