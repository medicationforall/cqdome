import cadquery as cq
from cqdome import greeble

vent = greeble.vent_hexagon(
    radius=58,
    height=4,
    frame_size = 9,
    vent_width = 2,
    vent_space = 0.6,
    vent_rotate=45
)

cq.exporters.export(vent,'stl/vent_hexagon.stl')
