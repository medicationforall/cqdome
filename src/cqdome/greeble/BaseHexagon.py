import cadquery as cq
from .. import Base

def make_hexagon(radius, height, z_rotate = 30):
    hexagon = (
        cq.Workplane("XY")
        .polygon(6, radius)
        .extrude(height)
        .translate((0,0,-1 * (height/2)))
        .rotate((0,0,1), (0,0,0), z_rotate)
        #.rotate((1,0,0),(0,0,0),-58)
    )
    return hexagon

class BaseHexagon(Base):
    def __init__(self):
        super().__init__()
        self.radius = 58
        self.height = 4
