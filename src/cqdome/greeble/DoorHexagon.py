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

def _check_chamfer(height, chamfer):
    if not (chamfer < height):
        raise Exception(f"chamfer \"{chamfer}\" greater than or equal to height provided \"{height}\"")



class DoorHexagon(Base):
    def __init__(self):
        super().__init__()
        self.radius = 58
        self.height = 4

        self.frame_inset = 9

        # door
        self.door_padding = .5
        self.door_chamfer = 1.5
        self.door_height = 4

        #hinge
        self.hinge_length = 4
        self.hinge_width = 16
        self.hinge_height = 5
        self.hinge_cylinder_height = 20
        self.hinge_cylinder_radius = 2.5
        self.hinge_x_translate= -3.5

        # handle
        self.handle_x_translate = 8.5
        self.handle_length = 5
        self.handle_width = 7

        # parts
        self.hexagon = None
        self.hexagon_cut = None
        self.frame = None
        self.hinge = None
        self.door_body = None
        self.handle_outline = None
        self.handle_detail = None


    def make(self):
        super().make()
        cut_radius = self.radius - self.frame_inset
        self.hexagon = _make_hexagon(self.radius, self.height)
        self.hexagon_cut = _make_hexagon(cut_radius, self.height)
        self.__make_frame()
        self.__make_door_body()
        self.__make_hinge()
        self.__make_handle()


    def __make_frame(self):
        self.frame = (
            cq.Workplane("XY")
            .union(self.hexagon)
            .cut(self.hexagon_cut)
        )


    def __make_door_body(self):
        _check_chamfer(self.door_height/2, self.door_chamfer)
        door_radius = self.radius - (self.frame_inset - self.door_padding)
        door = (
            _make_hexagon(door_radius, self.door_height)
            .chamfer(self.door_chamfer)
        )

        self.door_body = door


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
        ).translate((0.5,0,0))


    def __make_handle(self):
        self.handle_outline = (
            cq.Workplane("XY")
            .box(5,7,5.5)
            #.translate((16,0,0))
        )

        handle = cq.Workplane("XY").box(self.handle_length, self.handle_width,self.door_height+1.5)
        handle_cut = cq.Workplane("XY").box(self.handle_length-2,self.handle_width-3,self.door_height+2)
        handle_interier = cq.Workplane("XY").box(self.handle_length,self.handle_width,self.door_height-1)

        handle_detail = (
            handle
            .cut(handle_cut)
            .add(handle_interier)
            #.translate((16,0,0))
        )
        self.handle_detail = handle_detail


    def build(self):
        super().build()
        cut_radius = self.radius - self.frame_inset
        assembly = (
            cq.Workplane("XY")
            .union(self.frame.translate((0,0,0)))
            .union(self.door_body)
            .union(
                self.hinge
                .translate((-1*(cut_radius/2) - self.hinge_x_translate,0,0))
            )
            .cut(self.handle_outline.translate(((cut_radius/2) - self.handle_x_translate,0,0)))
            .union(self.handle_detail.translate(((cut_radius/2) - self.handle_x_translate,0,0)))
        )
        return assembly
