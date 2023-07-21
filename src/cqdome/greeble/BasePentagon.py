import cadquery as cq
from .. import Base

def make_pentagon(radius, height, z_rotate = 30):
    hexagon = (
        cq.Workplane("XY")
        .polygon(5, radius)
        .extrude(height)
        .translate((0,0,-1 * (height/2)))
        .rotate((0,0,1), (0,0,0), z_rotate)
        #.rotate((1,0,0),(0,0,0),-58)
    )
    return hexagon

class BasePentagon(Base):
    def __init__(self):
        super().__init__()
        self.radius = 51
        self.height = 4