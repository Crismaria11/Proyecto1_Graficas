from gl import *
from utils import *

def sombra(render, **kwargs):
  w, v, u = kwargs['bar']
  # textura
  tx, ty = kwargs['texture_coords']
  tcolor = render.active_texture.get_color(tx, ty)
  # normales
  nA, nB, nC = kwargs['varying_normals']

  # intensidad
  iA, iB, iC = [ dot(n, render.light) for n in (nA, nB, nC) ]
  intensity = w*iA + u*iB + v*iC
  r, g, b = tcolor[2] * intensity, tcolor[1] * intensity, tcolor[0] * intensity
  if r < 0:
    r = 0
  if r > 256:
    r = 255

  if b < 0:
    b = 0
  if b > 256:
    b = 255

  if g < 0:
    g = 0
  if g > 256:
    g = 255

  return color(
      int(r),
      int(g),
      int(b)
    )