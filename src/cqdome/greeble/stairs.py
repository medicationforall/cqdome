import cadquery as cq
from .. import Dome
from . import make_angled_steps
from cadqueryhelper import Base

class Stairs(Base):
    def __init__(self):
        super().__init__()
        self.stairs = None
        self.display_dome = False
        
    def make(self, parent=None):
        super().make(parent)
        
        if parent:
            self.parent.make()
            
        side_steps = make_angled_steps(width=10)
        side_cut = make_angled_steps(30-4,10)
        steps = make_angled_steps(30-4,10, 15-2)
        
        sides = (
            side_steps
            .cut(side_cut.translate((0,-.8,0)))
            .union(steps.translate((0,-.8,-1)))
        )
        
        self.stairs = sides
        
    def build(self):
        super().build()
        
        scene = (
            cq.Workplane("XY")
            .add(self.stairs.translate((0,-83,15/2)))
        )
        
        if self.parent:
            dome = self.parent.build()
            if self.display_dome:
                scene = scene.add(dome)
            else:
                scene = scene.cut(dome)

        return scene