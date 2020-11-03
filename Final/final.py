from gl import *
from shader import *
from obj import *


r = Render(1300, 702)
r.light = V3(0, 1, 1)

#Fondo
print('Un dia como cualquier otro en el bello zoologico de Central Park, sucedio algo que nadie se esperaba')
t = Texture('./textures/fondo.bmp')
r.framebuffer = t.pixels
r.active_texture = t
r.active_shader = sombra
r.lookAt(V3(1, 0, 100), V3(0, 0, 0), V3(0, 1, 0))
r.glFinish('scene.bmp')
print('Fondo creado')


# Avion
print('Un grupo de estudiantes volaban un avion a control remoto sobre el zoologico')
print('Esos estudiantes son tan pilas que lograron hacer uno mas grande que el tamaño usual')
t = Texture('./textures/plane.bmp')
r.active_texture = t
r.active_shader = sombra
r.lookAt(V3(1, 0, 3), V3(0, 0, 0), V3(0, 1, 0))
r.load('./models/plane.obj', translate=(-0.3, -0.1, 0), scale=(0.02,0.02,0.02), rotate=(0, 0, 0))
r.draw_arrays('TRIANGLES')
r.glFinish('scene.bmp')

#Pinguino1
print('Los pinguinos lindos como siempre en su lugar especial, ')
print('Luego uno sale de su escondite a tomar el sol')
t = Texture('./textures/Penguin.bmp')
r.active_texture = t
r.active_shader = sombra
r.lookAt(V3(1, 0, 3), V3(0, 0, 0), V3(0, 1, 0))
r.load('./models/Penguin.obj', translate=(-0.1, -0.65, 0), scale=(0.08,0.08,0.08), rotate=(0, -1.5, 0))
r.draw_arrays('TRIANGLES')
r.glFinish('scene.bmp')

#Pinguino2
print('Otro se tiro al agua, para refrescarse, sin duda el verano no es su temporada favorita')
t = Texture('./textures/Penguin.bmp')
r.active_texture = t
r.active_shader = sombra
r.lookAt(V3(1, 0, 3), V3(0, 0, 0), V3(0, 1, 0))
r.load('./models/Penguin.obj', translate=(-0.32, -0.74, 0), scale=(0.07,0.07,0.07), rotate=(1, -1, 0))
r.draw_arrays('TRIANGLES')
r.glFinish('scene.bmp')

# Nave Espacial
print('En cuestion de un segundo aparecio una gran nave espacial')
t = Texture('./textures/nave.bmp')
r.active_texture = t
r.active_shader = sombra
r.lookAt(V3(1, 0, 3), V3(0, 0, 0), V3(0, 1, 0))
r.load('./models/nave.obj', translate=(-0.5, 0.7, 0), scale=(0.08,0.08,0.08), rotate=(0, 0, 0))
r.draw_arrays('TRIANGLES')
r.glFinish('scene.bmp')

# Nave Espacial
print('Seguida por otras dos pequeñas')
t = Texture('./textures/nave.bmp')
r.active_texture = t
r.active_shader = sombra
r.lookAt(V3(1, 0, 3), V3(0, 0, 0), V3(0, 1, 0))
r.load('./models/nave.obj', translate=(-1, 0.4, 0), scale=(0.06,0.06,0.06), rotate=(0, 0, 0))
r.draw_arrays('TRIANGLES')
r.glFinish('scene.bmp')

# Nave Espacial
print('Una de cada lado')
t = Texture('./textures/nave.bmp')
r.active_texture = t
r.active_shader = sombra
r.lookAt(V3(1, 0, 3), V3(0, 0, 0), V3(0, 1, 0))
r.load('./models/nave.obj', translate=(-0.2, 0.44, 0), scale=(0.06,0.06,0.06), rotate=(0, 0, 0))
r.draw_arrays('TRIANGLES')
r.glFinish('scene.bmp')

# Oveja
print('La pobre oveja perdida se desmayo del gran susto')
t = Texture('./textures/sheep.bmp')
r.active_texture = t
r.active_shader = sombra
r.lookAt(V3(1, 0, 3), V3(0, 0, 0), V3(0, 1, 0))
r.load('./models/sheep.obj', translate=(-0.28, -0.88, 0), scale=(0.04,0.04,0.04), rotate=(-1, -1, 0))
r.draw_arrays('TRIANGLES')
r.glFinish('scene.bmp')

#Otra nave espacial
print('Oh no! Otras naves espaciales esta robando los pinguinos')
print('Muy probablemente piensen que son muy adorables por eso se los quieren llevar a su planeta')
t = Texture('./textures/ufo.bmp')
r.active_texture = t
r.active_shader = sombra
r.lookAt(V3(1, 0, 5), V3(0, 0, 0), V3(0, 1, 0))
r.load('./models/ufo.obj', translate=(-0.13, -0.26, 0), scale=(0.1,0.1,0.1), rotate=(0, 0.5, 0))
r.draw_arrays('TRIANGLES')
r.glFinish('scene.bmp')

#Otra nave espacial
print('Una nave más pequeña se lleva al piguino que esta sumergido')
print('Muy probablemente piensen que son muy adorables por eso se los quieren llevar a su planeta')
t = Texture('./textures/ufo.bmp')
r.active_texture = t
r.active_shader = sombra
r.lookAt(V3(1, 0, 5), V3(0, 0, 0), V3(0, 1, 0))
r.load('./models/ufo.obj', translate=(-0.3, -0.55, 0), scale=(0.04,0.04,0.04), rotate=(0, 0.5, 0))
r.draw_arrays('TRIANGLES')
r.glFinish('scene.bmp')

print('Escena terminada')
