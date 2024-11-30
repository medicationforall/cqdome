import cadquery as cq
from cqdome.greeble import make_hexagon

hexagon = make_hexagon(
    radius = 30,
    height = 3,
    z_rotate = 30
)

#show_object(hexagon)

cq.exporters.export(hexagon, 'dome_make_hexagon.stl')
