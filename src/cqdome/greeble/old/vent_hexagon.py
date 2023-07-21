import cadquery as cq
from cadqueryhelper import series
import math

def vent_hexagon(
        radius=58,
        height=4,
        frame_size = 9,
        vent_width = 2,
        vent_space = 0.6,
        vent_rotate=45
    ):
    hexagon = (
        cq.Workplane("XY")
        .polygon(6, radius)
        .extrude(height)
        .translate((0,0,-1*(height/2)))
    )

    hexagon_cut = (
        cq.Workplane("XY")
        .polygon(6, radius-frame_size)
        .extrude(height)
        .translate((0,0,-1*(height/2)))
    )

    vent = (
        cq.Workplane("XY")
        .box(radius-frame_size,vent_width ,height)
        .rotate((1,0,0),(0,0,0),vent_rotate)
    )

    vent_size = math.floor(
        (radius - frame_size * 2) / (vent_space + vent_width)
    )

    # replace with series
    vents = series(
        shape = vent,
        length_offset=None,
        width_offset=vent_space,
        height_offset=None,
        size=vent_size
    )

    return (
        hexagon
        .cut(hexagon_cut)
        .union(vents.intersect(hexagon_cut))
    )
