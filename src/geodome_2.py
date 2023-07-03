import cadquery as cq

hex_radius = 25
hex_height = 25
dome_radius = 50

circle = cq.Workplane("XY").circle(dome_radius)
hexagon = (
    cq.Workplane("XY")
    .polygon(6, hex_radius)
    .extrude(hex_height)
    .translate((0,0,-1*(hex_height/2)))
)

scene = (
    cq.Workplane("XY")
    .add(hexagon)
    .add(hexagon.rotate((0,1,0),(0,0,0),90))
    .add(hexagon.rotate((0,0,1),(0,0,0),30).rotate((1,0,0),(0,0,0),90))
    .add(hexagon.rotate((1,0,0),(0,0,0),90))
    #.intersect(hexagon.rotate((0,1,0),(0,0,0),60))
    #.intersect(hexagon.rotate((0,1,0),(0,0,0),90))
    #.intersect(hexagon.rotate((0,1,0),(0,0,0),120))
)

show_object(scene)