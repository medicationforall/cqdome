import cadquery as cq
from cqdome import Base

def _make_pentagon(
        pen_radius,
        hex_height,
        x_rotate=0,
        z_rotate=0
    ):
    pentagon = (
        cq.Workplane("XY")
        .polygon(5, pen_radius)
        .extrude(hex_height)
        .translate((0,0,-1*(hex_height/2)))
        .rotate((0,0,1),(0,0,0),z_rotate)
        .rotate((1,0,0),(0,0,0),x_rotate)
    )
    return pentagon

def _make_hexagon(
        hex_radius,
        hex_height,
        x_rotate=0,
        z_rotate=0
    ):
    hexagon = (
        cq.Workplane("XY")
        .polygon(6, hex_radius)
        .extrude(hex_height)
        .translate((0,0,-1*(hex_height/2)))
        .rotate((0,0,1),(0,0,0),z_rotate)
        .rotate((1,0,0),(0,0,0),x_rotate)
    )
    return hexagon

class Dome(Base):

    def __init__(self):
        super().__init__()
        self.hex_radius = 58
        self.hex_pen_diff = 7
        self.hex_height = 4
        self.hex_radius_cut = 9

        self.pen_radius = self.hex_radius - self.hex_pen_diff
        self.pen_radius_cut = 10

        # rotates
        self.r1_x_rotate = 32

        self.r2_x_rotate = -58
        self.r2_z_rotate = 30

        self.r2_pen_x_rotate = 63
        self.r2_pen_z_rotate = 54

        self.r3_x_rotate = 92
        self.r3_z_rotate = 30

        # render flags
        self.render_cut_keys = True

        #--- shapes
        self.center_pentagon = None
        self.center_pentagon_cut = None

        self.r1_hex = None
        self.r1_hex_cut = None

        self.r2_hex = None
        self.r2_hex_cut = None

        self.r2_pen = None
        self.r2_pen_cut = None

        self.r3_hex = None
        self.box_cut = None

        self.hexagon_cut_key = None
        self.pentagon_cut_key = None


    def make(self):
        super().make()

        self.__make_center()
        self.__make_r1_shapes()
        self.__make_r2_shapes()
        self.__make_r3_shapes()
        self.__make_box_cut()

        if self.render_cut_keys:
            self.__make_hexagon_cut_key()
            self.__make_pentagon_cut_key()


    def __make_center(self):
        self.center_pentagon = _make_pentagon(
            self.pen_radius,
            self.hex_height
        )

        self.center_pentagon_cut = _make_pentagon(
            self.pen_radius - self.pen_radius_cut,
            self.hex_height
        )


    def __make_r1_shapes(self):
        self.r1_hex = _make_hexagon(
            self.hex_radius,
            self.hex_height,
            self.r1_x_rotate
        )

        self.r1_hex_cut = _make_hexagon(
            self.hex_radius - self.hex_radius_cut,
            self.hex_height,
            self.r1_x_rotate
        )


    def __make_r2_shapes(self):
        self.r2_hex = _make_hexagon(
            self.hex_radius,
            self.hex_height,
            self.r2_x_rotate,
            self.r2_z_rotate
        )

        self.r2_hex_cut = _make_hexagon(
            self.hex_radius - self.hex_radius_cut,
            self.hex_height,
            self.r2_x_rotate,
            self.r2_z_rotate
        )

        self.r2_pen = _make_pentagon(
            self.pen_radius,
            self.hex_height,
            self.r2_pen_x_rotate,
            self.r2_pen_z_rotate
        )

        self.r2_pen_cut = _make_pentagon(
            self.pen_radius - self.pen_radius_cut,
            self.hex_height,
            self.r2_pen_x_rotate,
            self.r2_pen_z_rotate
        )

    def __make_r3_shapes(self):
        self.r3_hex = _make_hexagon(
            self.hex_radius,
            self.hex_height,
            self.r3_x_rotate,
            self.r3_z_rotate
        )


    def __make_box_cut(self):
        self.box_cut = cq.Workplane("XY").box(153,160,150)

    def __make_hexagon_cut_key(self):
        hexagon_cut = _make_hexagon(
            self.hex_radius-9.225-1,
            2
        )

        logo_text = (
            cq.Workplane("XY")
            .text("MiniForAll",10, 2)
            #.rotate((0,1,0),(0,0,0),180)
            .translate((-.5,0,0))
        )

        cut_hole = cq.Workplane("XY").cylinder(3,1.5).translate((0,17,0))
        self.hexagon_cut_key = hexagon_cut.union(logo_text).cut(cut_hole)

    def __make_pentagon_cut_key(self):

        pentagon_cut = _make_pentagon(
            self.pen_radius-10.225-1,
            2
        )

        logo_text = (
            cq.Workplane("XY")
            .text("MiniForAll",7, 2)
            #.rotate((0,1,0),(0,0,0),180)
            .translate((-.5,0,0))
        )

        cut_hole = cq.Workplane("XY").cylinder(3,1.5).translate((0,12,0))
        self.pentagon_cut_key = pentagon_cut.union(logo_text).cut(cut_hole)

    def build(self):
        super().build()
        '''
        dome = (
            cq.Workplane("XY")
            .union(self.center_pentagon)
            .cut(self.center_pentagon_cut)

            .union(self.r1_hex)
            .cut(self.r1_hex_cut)

            .union(self.r2_hex)
            .cut(self.r2_hex_cut)

            .union(self.r2_pen)
            .cut(self.r2_pen_cut)

            .union(self.r3_hex)
            .cut(self.r3_hex_cut)

            #.union(self.box_cut)
        )
        '''

        dome = cq.Workplane("XY")

        solid_dome = (
            cq.Workplane("XY")
            #center
            .union(self.center_pentagon.translate((0,0,12.2)).rotate((0,0,1),(0,0,0),18))

            #ring 1
            .union(self.r1_hex.translate((0,38.5,0))) #right
            .union(self.r1_hex.translate((0,38.5,0)).rotate((0,0,1),(0,0,0), 72))
            .union(self.r1_hex.translate((0,38.5,0)).rotate((0,0,1),(0,0,0), 72*2))
            .union(self.r1_hex.translate((0,38.5,0)).rotate((0,0,1),(0,0,0), 72*3))
            .union(self.r1_hex.translate((0,38.5,0)).rotate((0,0,1),(0,0,0), 72*4))
        )

        cut_dome = (
            cq.Workplane("XY")
            #center
            .union(self.center_pentagon_cut.translate((0,0,12.2)).rotate((0,0,1),(0,0,0),18))

            #ring 1
            .union(self.r1_hex_cut.translate((0,38.5,0))) #right
            .union(self.r1_hex_cut.translate((0,38.5,0)).rotate((0,0,1),(0,0,0), 72))
            .union(self.r1_hex_cut.translate((0,38.5,0)).rotate((0,0,1),(0,0,0), 72*2))
            .union(self.r1_hex_cut.translate((0,38.5,0)).rotate((0,0,1),(0,0,0), 72*3))
            .union(self.r1_hex_cut.translate((0,38.5,0)).rotate((0,0,1),(0,0,0), 72*4))
        )

        r2_p_y = 65.6
        ring_2 = (
            cq.Workplane("XY")
            .union(self.r2_hex.translate((0,-61.5,-23)))
            .union(self.r2_hex.translate((0,-61.5,-23)).rotate((0,0,1),(0,0,0),72))
            .union(self.r2_hex.translate((0,-61.5,-23)).rotate((0,0,1),(0,0,0),72*2))
            .union(self.r2_hex.translate((0,-61.5,-23)).rotate((0,0,1),(0,0,0),72*3))
            .union(self.r2_hex.translate((0,-61.5,-23)).rotate((0,0,1),(0,0,0),72*4))

            .union(self.r2_pen.translate((0,r2_p_y,-28.3)))
            .union(self.r2_pen.translate((0,r2_p_y,-28.3)).rotate((0,0,1),(0,0,0),72))
            .union(self.r2_pen.translate((0,r2_p_y,-28.3)).rotate((0,0,1),(0,0,0),72*2))
            .union(self.r2_pen.translate((0,r2_p_y,-28.3)).rotate((0,0,1),(0,0,0),72*3))
            .union(self.r2_pen.translate((0,r2_p_y,-28.3)).rotate((0,0,1),(0,0,0),72*4))
        )

        ring_2_cut = (
            cq.Workplane("XY")
            .union(self.r2_hex_cut.translate((0,-61.5,-23)))
            .union(self.r2_hex_cut.translate((0,-61.5,-23)).rotate((0,0,1),(0,0,0),72))
            .union(self.r2_hex_cut.translate((0,-61.5,-23)).rotate((0,0,1),(0,0,0),72*2))
            .union(self.r2_hex_cut.translate((0,-61.5,-23)).rotate((0,0,1),(0,0,0),72*3))
            .union(self.r2_hex_cut.translate((0,-61.5,-23)).rotate((0,0,1),(0,0,0),72*4))

            .union(self.r2_pen_cut.translate((0,r2_p_y,-28.3)))
            .union(self.r2_pen_cut.translate((0,r2_p_y,-28.3)).rotate((0,0,1),(0,0,0),72))
            .union(self.r2_pen_cut.translate((0,r2_p_y,-28.3)).rotate((0,0,1),(0,0,0),72*2))
            .union(self.r2_pen_cut.translate((0,r2_p_y,-28.3)).rotate((0,0,1),(0,0,0),72*3))
            .union(self.r2_pen_cut.translate((0,r2_p_y,-28.3)).rotate((0,0,1),(0,0,0),72*4))
        )

        r3_y=-73
        r3_z=-1
        ring_3 = (
            cq.Workplane("XY")
            .union(self.r3_hex.translate((0,r3_y,r3_z)))
            .union(self.r3_hex.translate((0,r3_y,r3_z)).rotate((0,0,1),(0,0,0),36))
            .union(self.r3_hex.translate((0,r3_y,r3_z)).rotate((0,0,1),(0,0,0),36*2))
            .union(self.r3_hex.translate((0,r3_y,r3_z)).rotate((0,0,1),(0,0,0),36*3))
            .union(self.r3_hex.translate((0,r3_y,r3_z)).rotate((0,0,1),(0,0,0),36*4))
            .union(self.r3_hex.translate((0,r3_y,r3_z)).rotate((0,0,1),(0,0,0),36*5))
            .union(self.r3_hex.translate((0,r3_y,r3_z)).rotate((0,0,1),(0,0,0),36*6))
            .union(self.r3_hex.translate((0,r3_y,r3_z)).rotate((0,0,1),(0,0,0),36*7))
            .union(self.r3_hex.translate((0,r3_y,r3_z)).rotate((0,0,1),(0,0,0),36*8))
            .union(self.r3_hex.translate((0,r3_y,r3_z)).rotate((0,0,1),(0,0,0),36*9))
        )


        dome = (
            dome
            .union(solid_dome)
            .union(ring_2)
            .union(ring_3.translate((0,0,-60)).rotate((0,0,1),(0,0,0),18))
            .cut(cut_dome)
            .cut(ring_2_cut)
        )

        dome = (
            dome
            .translate((0,0,60))
            .cut(self.box_cut.translate((0,0,-1*(150/2))))
        )

        if self.render_cut_keys:
            dome = (
                dome.union(self.hexagon_cut_key)
                .union(self.pentagon_cut_key.translate((43,0,0)))
            )

        return dome
    
