

hex_radius = 25
hex_height = 100
dome_radius = 50

circle = cq.Workplane("XY").circle(dome_radius)
sphere = cq.Workplane("YX").sphere(dome_radius)

hexagon = (
    cq.Workplane("XY")
    .polygon(6, hex_radius)
    .extrude(hex_height)
    .translate((0,0,-1*(hex_height/2)))
)

hexagon2 = (
    cq.Workplane("XY")
    .polygon(6, hex_radius)
    .extrude(hex_height+20)
    .translate((0,0,-1*((hex_height+20)/2)))
)

hexagon3 = (
    cq.Workplane("XY")
    .polygon(6, hex_radius+0.5)
    .extrude(hex_height+20)
    .translate((0,0,-1*((hex_height+20)/2)))
)

hexes = (
    cq.Workplane("XY")
    .union(hexagon)#center
    .union(hexagon.translate((0,hex_radius-3,0)))
    .union(hexagon.translate((0,-1*(hex_radius-3),0)))
    .union(hexagon.translate((hex_radius-6,hex_radius/2-1.5,0)))
    .union(hexagon.translate((-1*(hex_radius-6),hex_radius/2-1.5,0)))
    .union(hexagon.translate((-1*(hex_radius-6),-1*(hex_radius/2-1.5),0)))
    .union(hexagon.translate(((hex_radius-6),-1*(hex_radius/2-1.5),0)))

    .union(hexagon.translate((0,hex_radius*2-3*2,0)))
    .union(hexagon.translate((0,-1*(hex_radius*2-3*2),0)))

    .union(hexagon.translate((hex_radius*2-12,0,0)))
    .union(hexagon.translate((-1*(hex_radius*2-12),0,0)))

    .union(hexagon.translate((hex_radius-6,hex_radius+8,0)))
    .union(hexagon.translate((hex_radius-6,-1*(hex_radius+8),0)))
    .union(hexagon.translate((-1*(hex_radius-6),hex_radius+8,0)))
    .union(hexagon.translate((-1*(hex_radius-6),-1*(hex_radius+8),0)))

    .union(hexagon.translate((hex_radius*2-12,hex_radius-3,0)))
    .union(hexagon.translate((hex_radius*2-12,-1*(hex_radius-3),0)))
    .union(hexagon.translate((-1*(hex_radius*2-12),hex_radius-3,0)))
    .union(hexagon.translate((-1*(hex_radius*2-12),-1*(hex_radius-3),0)))
)

side = (
    cq.Workplane("XY")
    .union(hexagon2)#center
    .union(hexagon2.translate((0,hex_radius-3,0)))
    .union(hexagon2.translate((0,-1*(hex_radius-3),0)))
    .union(hexagon2.translate((hex_radius-6,hex_radius/2-1.5,0)))
    .union(hexagon2.translate((-1*(hex_radius-6),hex_radius/2-1.5,0)))
    .union(hexagon2.translate((-1*(hex_radius-6),-1*(hex_radius/2-1.5),0)))
    .union(hexagon2.translate(((hex_radius-6),-1*(hex_radius/2-1.5),0)))
    .rotate((1,0,0),(0,0,0),90)
    #.rotate((0,0,1),(0,0,0),30)
)
side_cut = (
    cq.Workplane("XY")
    .union(hexagon3)#center
    .union(hexagon3.translate((0,hex_radius-3,0)))
    .union(hexagon3.translate((0,-1*(hex_radius-3),0)))
    .union(hexagon3.translate((hex_radius-6,hex_radius/2-1.5,0)))
    .union(hexagon3.translate((-1*(hex_radius-6),hex_radius/2-1.5,0)))
    .union(hexagon3.translate((-1*(hex_radius-6),-1*(hex_radius/2-1.5),0)))
    .union(hexagon3.translate(((hex_radius-6),-1*(hex_radius/2-1.5),0)))
    .rotate((1,0,0),(0,0,0),90)
    #.rotate((0,0,1),(0,0,0),30)
)

scene = (
    cq.Workplane("XY")
    .union(hexes)
    .cut(side_cut.rotate((0,1,0),(0,0,0),60))
    .union(side.rotate((0,1,0),(0,0,0),60))
    .cut(side_cut.rotate((0,1,0),(0,0,0),30).rotate((0,0,1),(0,0,0),90))
    .union(side.rotate((0,1,0),(0,0,0),30).rotate((0,0,1),(0,0,0),90))
    .intersect(sphere)
)

show_object(scene)
show_object(circle)
#show_object(sphere)
