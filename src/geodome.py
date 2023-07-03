import cadquery as cq

hex_radius = 25
hex_height = 2
dome_radius = 50

circle = cq.Workplane("XY").circle(dome_radius)
hexagon_raw = (
    cq.Workplane("XY")
    .polygon(6, hex_radius)
    .extrude(hex_height)
    .translate((0,0,-1*(2/2)))
)

hexagon = hexagon_raw.rotate((1,0,0),(0,0,0),90).translate((0,dome_radius-hex_height/2,0))

hex_ring = (
    cq.Workplane("XY")
    .add(hexagon)
    .add(hexagon.rotate((0,0,1),(0,0,0),45))
    .add(hexagon.rotate((0,0,1),(0,0,0),90))
    .add(hexagon.rotate((0,0,1),(0,0,0),135))
    .add(hexagon.rotate((0,0,1),(0,0,0),180))
    .add(hexagon.rotate((0,0,1),(0,0,0),225))
    .add(hexagon.rotate((0,0,1),(0,0,0),270))
    .add(hexagon.rotate((0,0,1),(0,0,0),315))
)

hedron = (
    cq.Workplane("XY")
    .union(hex_ring)
    .union(hex_ring.rotate((0,1,0),(0,0,0),60))
    .union(hex_ring.rotate((0,1,0),(0,0,0),120))
)

hedrons = (
    cq.Workplane("XY")
    .add(
        hexagon_raw
        .rotate((1,0,0),(0,0,0),60)
        .translate((0,50-hex_height/2,22))
        
    )
)

show_object(circle)
show_object(hedron)
show_object(hedrons, options={"alpha":0.5, "color": (64, 164, 223)})