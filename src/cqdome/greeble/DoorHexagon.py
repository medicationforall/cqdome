import cadquery as cq
from . import BaseHexagon, make_hexagon

def _check_chamfer(height, chamfer):
    if not (chamfer < height):
        raise Exception(f"chamfer \"{chamfer}\" greater than or equal to height provided \"{height}\"")


class DoorHexagon(BaseHexagon):
    def __init__(self):
        super().__init__()
        self.radius = 58
        self.height = 4

        self.frame_inset = 4

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
        self.hinge_x_translate= -4.3 #-3.5

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


    def _calc_radius(self):
        radius = self.radius

        if self.parent and hasattr(self.parent, "hex_radius") and hasattr(self.parent, "hex_radius_cut"):
            radius = self.parent.hex_radius - self.parent.hex_radius_cut
            print(f'door _calc_radius set calculated radius {radius}, {self.parent.hex_radius}, {self.parent.hex_radius_cut}')
        return radius

    def make(self,parent=None):
        super().make(parent)

        radius = self._calc_radius()
        cut_radius = radius - self.frame_inset

        self.hexagon = make_hexagon(radius, self.height, 30)
        self.hexagon_cut = make_hexagon(cut_radius, self.height, 30)
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
        radius = self._calc_radius()
        _check_chamfer(self.door_height/2, self.door_chamfer)
        door_radius = radius - (self.frame_inset - self.door_padding)
        door = (
            make_hexagon(door_radius, self.door_height, 30)
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
        radius = self._calc_radius()
        cut_radius = radius - self.frame_inset
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
        return assembly.rotate((0,0,1),(0,0,0), -30)
