import cadquery as cq

def make_angled_step(
    length=30, 
    width=10, 
    height=15, 
    angle = 36
):
    step_half = (
        cq.Workplane("XY")
        .box(length,width,height)
    )

    step = (
        cq.Workplane("XY")
        .add(
            step_half
            .translate((-1*(length/2),width/2,0))
            .rotate((0,0,1),(0,0,0),angle)
        )
        .add(
            step_half
            .translate((length/2,width/2,0))
        )
    )
    
    step = (
        step
        .rotate((0,0,1),(0,0,0),-1*(angle/2))
        .translate((0,-1*(length/5),0))
    )
    return step

def make_angled_steps(
        length=30, 
        width=10, 
        height=15,
        dec=5
):
    steps = cq.Workplane("XY")

    for i in range(3):
        step_height = height -dec*i
        step = make_angled_step(
            length,
            width,
            step_height
        )

        steps = (
            steps
            .union(
                step
                .translate((
                    0,
                    -width*i,
                    -1*(height/2)+(step_height/2))
                )
            )
        )
    return steps