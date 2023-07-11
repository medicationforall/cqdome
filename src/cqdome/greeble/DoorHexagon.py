import cadquery as cq
from cqdome import Base

def _make_hexagon(radius, height, z_rotate = 30):
    hexagon = (
        cq.Workplane("XY")
        .polygon(6, radius)
        .extrude(height)
        .translate((0,0,-1 * (height/2)))
        .rotate((0,0,1), (0,0,0), z_rotate)
        #.rotate((1,0,0),(0,0,0),-58)
    )
    return hexagon

def __make_hinge_cylinder(height=20, radius=2.5):
    hinge_cylinder = (
        cq.Workplane("XY")
        .cylinder(height,radius)
        .rotate((1,0,0),(0,0,0),90)
    )
    return hinge_cylinder

class DoorHexagon(Base):
    def __init__(self):
        super().__init__()
        self.radius = 58
        self.height = 4

        self.frame_inset = 9

        self.door_padding = .5
        self.door_chamfer = 1.5

        #hinge
        self.hinge_length = 4
        self.hinge_width = 16
        self.hinge_height = 5
        self.hinge_cylinder_height = 20
        self.hinge_cylinder_radius = 2.5

        # parts
        self.hexagon = None
        self.hexagon_cut = None
        self.frame = None
        self.hinge = None

    def make(self):
        super().make()
        cut_radius = self.radius - self.frame_inset
        self.hexagon = _make_hexagon(self.radius, self.height)
        self.hexagon_cut = _make_hexagon(cut_radius, self.height)
        self.__make_frame()
        self.__make_hinge()

    def __make_frame(self):
        self.frame = (
            cq.Workplane("XY")
            .union(self.hexagon)
            .cut(self.hexagon_cut)
        )

    def __make_hinge(self):
        hinge_box = (
            cq.Workplane("XY")
            .box(self.hinge_length, self.hinge_width, self.hinge_height)
        )

        hinge_cylinder = (
            cq.Workplane("XY")
            .cylinder(self.hinge_cylinder_height,self.hinge_cylinder_radius)
            .rotate((1,0,0),(0,0,0),90)
        )

        self.hinge = (
            cq.Workplane("XY")
            .union(hinge_box)
            .union(hinge_cylinder.translate((-1,0,0)))
        )

    def build(self):
        super().build()
        assembly = (
            cq.Workplane("XY")
            .union(self.frame)
            .union(self.hinge)
        )
        return assembly
