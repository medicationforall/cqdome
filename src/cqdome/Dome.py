import cadquery as cq
from cqdome import Base, greeble

def _make_pentagon(pen_radius, hex_height):
    pentagon = (
        cq.Workplane("XY")
        .polygon(5, pen_radius)
        .extrude(hex_height)
        .translate((0,0,-1*(hex_height/2)))

    )
    return pentagon

def _make_hexagon(hex_radius, hex_height):
    hexagon = (
        cq.Workplane("XY")
        .polygon(6, hex_radius)
        .extrude(hex_height)
        .translate((0,0,-1*(hex_height/2)))
    )
    return hexagon

def _rotate(shape, x_rotate=0, z_rotate=0):
    if shape:
        shape = (
            cq.Workplane("XY")
            .union(shape) #clone the shape
            .rotate((0,0,1),(0,0,0),z_rotate)
            .rotate((1,0,0),(0,0,0),x_rotate)
        )
    return shape


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

        # greebles
        self.r1_greeble = [1]
        self.r2_greeble_hex = [0,2]

        # render flags
        self.render_cut_keys = True

        #--- shapes
        self.pentagon = None
        self.pentagon_cut = None
        self.hexagon = None
        self.hexagon_cut = None
        self.box_cut = None

        self.hexagon_cut_key = None
        self.pentagon_cut_key = None
        self.vent_greeble = None
        self.door_greeble = None


    def make(self):
        super().make()
        self.__make_base_shapes()
        self.box_cut = cq.Workplane("XY").box(153,160,150)

        if self.render_cut_keys:
            self.__make_hexagon_cut_key()
            self.__make_pentagon_cut_key()

        self.vent_greeble = greeble.vent_hexagon(
            radius = self.hex_radius - self.hex_radius_cut
        )

        door_bp = greeble.DoorHexagon()
        door_bp.radius = self.hex_radius - self.hex_radius_cut
        door_bp.frame_inset = 4
        door_bp.hinge_x_translate = -4.3
        door_bp.make()

        self.door_greeble = door_bp.build()


    def __make_base_shapes(self):
        self.pentagon = _make_pentagon(self.pen_radius, self.hex_height)
        self.hexagon = _make_hexagon(self.hex_radius, self.hex_height)

        self.pentagon_cut = _make_pentagon(
            self.pen_radius - self.pen_radius_cut,
            self.hex_height
        )
        self.hexagon_cut = _make_hexagon(
            self.hex_radius - self.hex_radius_cut,
            self.hex_height
        )



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
        self.hexagon_cut_key = (
            hexagon_cut
            .union(logo_text)
            .cut(cut_hole)
            .translate((0,0,2/2))
        )

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
        self.pentagon_cut_key = (
            pentagon_cut
            .union(logo_text)
            .cut(cut_hole)
            .translate((0,0,2/2))
            )

    def build(self):
        super().build()
        dome = self.build_frame()

        if self.render_cut_keys:
            dome = (
                dome
                .union(self.hexagon_cut_key)
                .union(self.pentagon_cut_key.translate((43,0,0)))
            )

        #greebles
        if self.vent_greeble:
            greebled_r1 = self.__build_ring1(
                self.vent_greeble,
                None,
                keep_hex = self.r1_greeble
            )

        if self.vent_greeble:
            greebled_r2 = self.__build_ring2(
                self.door_greeble.rotate((0,0,1),(0,0,0),-30),
                None,
                keep_hex = self.r2_greeble_hex
            )

        dome = (
            dome
            .add(greebled_r1.translate((0,0,60)))
            .add(greebled_r2.translate((0,0,60)))
        )

        return dome

    def build_frame(self):
        dome = cq.Workplane("XY")

        solid_dome = self.__build_ring1(self.hexagon, self.pentagon)
        cut_dome = self.__build_ring1(self.hexagon_cut, self.pentagon_cut)
        ring_2 = self.__build_ring2(self.hexagon, self.pentagon)
        ring_2_cut = self.__build_ring2(self.hexagon_cut, self.pentagon_cut)
        ring_3 = self.__build_ring_3(self.hexagon)

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

        return dome


    def build_plate(self):
        dome = self.build_frame()

        if self.render_cut_keys:
            dome = (
                dome
                .union(self.hexagon_cut_key)
                .union(self.pentagon_cut_key.translate((43,0,0)))
            )

        if self.vent_greeble:
            dome = (
                dome
                .add(
                    self.vent_greeble
                    .translate((
                        0,
                        -1*(self.hex_radius - self.hex_radius_cut)+5,
                        self.hex_height/2
                    ))
                )
            )

        if self.door_greeble:
            dome = (
                dome
                .add(
                    self.door_greeble
                    .rotate((0,0,1),(0,0,0),90)
                    .rotate((1,0,0),(0,0,0),90)
                    .translate((
                        0,
                        1*(self.hex_radius - self.hex_radius_cut)-5,
                        self.hex_height/2
                    ))
                )
            )

        return dome

    def build_plate_parts(self):
        dome = self.build_frame()

        if self.render_cut_keys:
            keys = (
                cq.Workplane("XY")
                .union(self.hexagon_cut_key)
                .union(self.pentagon_cut_key.translate((43,0,0)))
            )

        if self.vent_greeble:
            vent = (
                cq.Workplane("XY")
                .add(
                    self.vent_greeble
                    .translate((
                        0,
                        -1*(self.hex_radius - self.hex_radius_cut)+5,
                        self.hex_height/2
                    ))
                )
            )
        else:
            vent = None

        if self.door_greeble:
            door = (
                cq.Workplane("XY")
                .add(
                    self.door_greeble
                    .rotate((0,0,1),(0,0,0),90)
                    .rotate((1,0,0),(0,0,0),90)
                    .translate((
                        0,
                        1*(self.hex_radius - self.hex_radius_cut)-5,
                        self.hex_height/2
                    ))
                )
            )

        return dome, vent, door, keys

    def __build_ring1(self, hex_shape, pen_shape, keep_hex=None):
        h =  _rotate(hex_shape,self.r1_x_rotate,0)
        p =  _rotate(pen_shape,0,0)
        dome = (
            cq.Workplane("XY")
        )

        #center
        if p:
            dome = dome.union(
                p
                .translate((0,0,12.2))
                .rotate((0,0,1),(0,0,0),18)
            )

        #ring 1
        if h:
            for i in range(5):
                if keep_hex == None or i in  keep_hex:
                    dome = (
                        dome
                        .union(
                            h
                            .translate((0,38.5,0))
                            .rotate((0,0,1),(0,0,0), 72*i)
                        )
                    )

        return dome


    def __build_ring2(self, hex_shape, pen_shape, keep_hex = None, keep_pen = None):
        h =  _rotate(hex_shape,self.r2_x_rotate,self.r2_z_rotate)
        p =  _rotate(pen_shape,self.r2_pen_x_rotate,self.r2_pen_z_rotate)
        r2_p_y = 65.6
        ring = (
            cq.Workplane("XY")
        )

        if h:
            for i in range(5):
                if keep_hex == None  or i in  keep_hex:
                    ring = (
                        ring
                        .union(
                            h
                            .translate((0,-61.5,-23))
                            .rotate((0,0,1),(0,0,0),72*i)
                        )
                    )
        if p:
            for i in range(5):
                if keep_pen == None  or i in  keep_pen:
                    ring = (
                        ring
                        .union(
                            p
                            .translate((0,r2_p_y,-28.3))
                            .rotate((0,0,1),(0,0,0),72*i)
                        )
                    )

        return ring


    def __build_ring_3(self, hex_shape):
        h =  _rotate(hex_shape,self.r3_x_rotate,self.r3_z_rotate)
        r3_y=-73
        r3_z=-1
        ring_3 = (cq.Workplane("XY"))

        for i in range(10):
            ring_3 = (
                ring_3
                .union(
                    h
                    .translate((0,r3_y,r3_z))
                    .rotate((0,0,1),(0,0,0),36*i)
                )
            )
        return ring_3
