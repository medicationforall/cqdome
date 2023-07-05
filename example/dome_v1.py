import cadquery as cq
import math

hex_radius = 58
pen_radius = hex_radius-7
hex_height = 4
#dome_radius = 50

def make_hexagon_cut():
    hexagon_cut = (
        cq.Workplane("XY")
        .polygon(6, hex_radius-9.225-1)
        .extrude(2)
        .translate((0,0,-1*(2/2)))
    )

    logo_text = (
        cq.Workplane("XY")
        .text("MiniForAll",10, 2)
        #.rotate((0,1,0),(0,0,0),180)
        .translate((-.5,0,0))
    )

    cut_hole = cq.Workplane("XY").cylinder(3,1.5).translate((0,17,0))
    return hexagon_cut.union(logo_text).cut(cut_hole)

def make_pentagon_cut():
    pentagon_cut = (
        cq.Workplane("XY")
        .polygon(5, pen_radius-10.225-1)
        .extrude(2)
        .translate((0,0,-1*(2/2)))
    )

    logo_text = (
        cq.Workplane("XY")
        .text("MiniForAll",7, 2)
        #.rotate((0,1,0),(0,0,0),180)
        .translate((-.5,0,0))
    )

    cut_hole = cq.Workplane("XY").cylinder(3,1.5).translate((0,12,0))
    return pentagon_cut.union(logo_text).cut(cut_hole)


def make_center_pentagon():
    pentagon = (
        cq.Workplane("XY")
        .polygon(5, pen_radius)
        .extrude(hex_height)
        .translate((0,0,-1*(hex_height/2)))
    )

    pentagon_cut = (
        cq.Workplane("XY")
        .polygon(5, pen_radius-10)
        .extrude(hex_height)
        .translate((0,0,-1*(hex_height/2)))
    )

    pentagon = pentagon.cut(pentagon_cut)
    return pentagon

def make_ring1_hexagon():
    hexagon2 = (
        cq.Workplane("XY")
        .polygon(6, hex_radius)
        .extrude(hex_height)
        .translate((0,0,-1*(hex_height/2)))
        .rotate((1,0,0),(0,0,0),32)
    )

    hexagon_cut = (
        cq.Workplane("XY")
        .polygon(6, hex_radius-9)
        .extrude(hex_height)
        .translate((0,0,-1*(hex_height/2)))
        .rotate((1,0,0),(0,0,0),32)
    )
    return hexagon2.cut(hexagon_cut)

def make_ring1_vent():
    hexagon2 = (
        cq.Workplane("XY")
        .polygon(6, hex_radius)
        .extrude(hex_height)
        .translate((0,0,-1*(hex_height/2)))
        #.rotate((1,0,0),(0,0,0),32)
    )

    hexagon_cut = (
        cq.Workplane("XY")
        .polygon(6, hex_radius-9)
        .extrude(hex_height)
        .translate((0,0,-1*(hex_height/2)))
    )

    vent = (
        cq.Workplane("XY")
        .box(50,2,hex_height)
        .rotate((1,0,0),(0,0,0),45)
    )

    vents = (
        cq.Workplane("XY")
        .add(vent)
        .add(vent.translate((0,-1*(5*4),0)))
        .add(vent.translate((0,-1*(5*3),0)))
        .add(vent.translate((0,-1*(5*2),0)))
        .add(vent.translate((0,-1*(5),0)))
        .add(vent.translate((0,5,0)))
        .add(vent.translate((0,5*2,0)))
        .add(vent.translate((0,5*3,0)))
        .add(vent.translate((0,5*4,0)))
    )
    return (
        hexagon2
        .cut(hexagon_cut)
        .add(vents.intersect(hexagon_cut))
    ).rotate((1,0,0),(0,0,0),32)

def make_ring2_hexagon():
    hexagon3 = (
        cq.Workplane("XY")
        .polygon(6, hex_radius)
        .extrude(hex_height)
        .translate((0,0,-1*(hex_height/2)))
        .rotate((0,0,1),(0,0,0),30)
        .rotate((1,0,0),(0,0,0),-58)
    )

    hexagon_cut = (
        cq.Workplane("XY")
        .polygon(6, hex_radius - 9)
        .extrude(hex_height)
        .translate((0,0,-1*(hex_height/2)))
        .rotate((0,0,1),(0,0,0),30)
        .rotate((1,0,0),(0,0,0),-58)
    )

    return hexagon3.cut(hexagon_cut)

def make_ring2_door():
    hexagon3 = (
        cq.Workplane("XY")
        .polygon(6, hex_radius)
        .extrude(hex_height)
        .translate((0,0,-1*(hex_height/2)))
        .rotate((0,0,1),(0,0,0),30)
        .rotate((1,0,0),(0,0,0),-58)
    )

    hexagon_cut = (
        cq.Workplane("XY")
        .polygon(6, hex_radius - 9)
        .extrude(hex_height)
        .translate((0,0,-1*(hex_height/2)))
        .rotate((0,0,1),(0,0,0),30)
        .rotate((1,0,0),(0,0,0),-58)
    )

    door = (
        cq.Workplane("XY")
        .polygon(6, hex_radius - 8.5)
        .extrude(hex_height)
        .chamfer(1.5)
        .translate((0,0,-1*(hex_height/2)))
        .rotate((0,0,1),(0,0,0),30)
    )

    hinge = (
        cq.Workplane("XY")
        .box(4,16,5)
        .translate((-20,0,0))
    )

    hinge_cylinder = (
        cq.Workplane("XY")
        .cylinder(20,2.5)
        .rotate((1,0,0),(0,0,0),90)
        .translate((-21,0,0))
    )

    handle_outline =cq.Workplane("XY").box(5,7,5.5).translate((16,0,0))
    handle = cq.Workplane("XY").box(5,7,5.5)
    handle_cut = cq.Workplane("XY").box(3,4,6)
    handle_interier = cq.Workplane("XY").box(5,7,3)

    handle_detail = (
        handle
        .cut(handle_cut)
        .add(handle_interier)
        .translate((16,0,0))
    )


    door_detailed = (
        cq.Workplane("XY")
        .add(door)
        .add(hinge)
        .add(hinge_cylinder)
        .cut(handle_outline)
        .add(handle_detail)

    )

    return (
        hexagon3
        .cut(hexagon_cut)
        .add(door_detailed.rotate((1,0,0),(0,0,0),-58))
    )

def make_ring2_pentagon():
    pentagon4 = (
        cq.Workplane("XY")
        .polygon(5, pen_radius)
        .extrude(hex_height)
        .translate((0,0,-1*(hex_height/2)))
        .rotate((0,0,1),(0,0,0),54)
        .rotate((1,0,0),(0,0,0),63)
    )

    pentagon_cut = (
        cq.Workplane("XY")
        .polygon(5, pen_radius-10)
        .extrude(hex_height)
        .translate((0,0,-1*(hex_height/2)))
        .rotate((0,0,1),(0,0,0),54)
        .rotate((1,0,0),(0,0,0),63)
    )
    return pentagon4.cut(pentagon_cut)

def make_ring3_hexagon():
    hexagon5 = (
        cq.Workplane("XY")
        .polygon(6, hex_radius)
        .extrude(hex_height)
        .translate((0,0,-1*(hex_height/2)))
        .rotate((0,0,1),(0,0,0),30)
        .rotate((1,0,0),(0,0,0),92)
        #.rotate((0,0,1),(0,0,0),-3)
    )
    return hexagon5

center_pentagon = make_center_pentagon()
r1_hex = make_ring1_hexagon()
r1_vent = make_ring1_vent()

r2_hex = make_ring2_hexagon()
r2_door = make_ring2_door()

r2_pen = make_ring2_pentagon()
r3_hex = make_ring3_hexagon()
box_cut = cq.Workplane("XY").box(153,160,150)
hexagon_cut = make_hexagon_cut()
pentagon_cut = make_pentagon_cut()

dome = (
    cq.Workplane("XY")
    #center
    .union(center_pentagon.translate((0,0,12.2)).rotate((0,0,1),(0,0,0),18))

    #ring 1
    .union(r1_hex.translate((0,38.5,0))) #right
    .union(r1_hex.translate((0,38.5,0)).rotate((0,0,1),(0,0,0), 72))
    .union(r1_hex.translate((0,38.5,0)).rotate((0,0,1),(0,0,0), 72*2))
    .union(r1_hex.translate((0,38.5,0)).rotate((0,0,1),(0,0,0), 72*3))
    .union(r1_vent.translate((0,38.5,0)).rotate((0,0,1),(0,0,0), 72*4))
)

r2_p_y = 65.6
ring_2 = (
    cq.Workplane("XY")
    .union(r2_door.translate((0,-61.5,-23)))
    .union(r2_hex.translate((0,-61.5,-23)).rotate((0,0,1),(0,0,0),72))
    .union(r2_hex.translate((0,-61.5,-23)).rotate((0,0,1),(0,0,0),72*2))
    .union(r2_door.translate((0,-61.5,-23)).rotate((0,0,1),(0,0,0),72*3))
    .union(r2_hex.translate((0,-61.5,-23)).rotate((0,0,1),(0,0,0),72*4))

    .union(r2_pen.translate((0,r2_p_y,-28.3)))
    .union(r2_pen.translate((0,r2_p_y,-28.3)).rotate((0,0,1),(0,0,0),72))
    .union(r2_pen.translate((0,r2_p_y,-28.3)).rotate((0,0,1),(0,0,0),72*2))
    .union(r2_pen.translate((0,r2_p_y,-28.3)).rotate((0,0,1),(0,0,0),72*3))
    .union(r2_pen.translate((0,r2_p_y,-28.3)).rotate((0,0,1),(0,0,0),72*4))
)

r3_y=-73
r3_z=-1
ring_3 = (
    cq.Workplane("XY")
    .union(r3_hex.translate((0,r3_y,r3_z)))
    .union(r3_hex.translate((0,r3_y,r3_z)).rotate((0,0,1),(0,0,0),36))
    .union(r3_hex.translate((0,r3_y,r3_z)).rotate((0,0,1),(0,0,0),36*2))
    .union(r3_hex.translate((0,r3_y,r3_z)).rotate((0,0,1),(0,0,0),36*3))
    .union(r3_hex.translate((0,r3_y,r3_z)).rotate((0,0,1),(0,0,0),36*4))
    .union(r3_hex.translate((0,r3_y,r3_z)).rotate((0,0,1),(0,0,0),36*5))
    .union(r3_hex.translate((0,r3_y,r3_z)).rotate((0,0,1),(0,0,0),36*6))
    .union(r3_hex.translate((0,r3_y,r3_z)).rotate((0,0,1),(0,0,0),36*7))
    .union(r3_hex.translate((0,r3_y,r3_z)).rotate((0,0,1),(0,0,0),36*8))
    .union(r3_hex.translate((0,r3_y,r3_z)).rotate((0,0,1),(0,0,0),36*9))
)

sphere = cq.Workplane("XY").sphere(75)

scene = (
    cq.Workplane("XY")
    .union(dome)
    .union(ring_2)
)

scene2 = (
    cq.Workplane("XY")
    #.add(sphere)
    .union(scene.translate((0,0,60)))
    .union(ring_3.rotate((0,0,1),(0,0,0),18))
    .cut(box_cut.translate((0,0,-1*(150/2))))

)

mini_proxy = (
    cq.Workplane("XY")
    .cylinder(32,12.5)
)


#show_object(scene2)
#show_object(hexagon_cut)
#show_object(pentagon_cut)


cq.exporters.export(hexagon_cut, "./stl/dome_hexagon_cut.stl")
cq.exporters.export(pentagon_cut, "./stl/dome_pentagon_cut.stl")
cq.exporters.export(scene2, "./stl/dome_v1.stl")
