import cadquery as cq
from . import make_hexagon, make_pentagon
from .. import Base

import cadquery as cq
from . import make_hexagon, make_pentagon
from .. import Base

_types = {
    'hexagon':make_hexagon, 
    'pentagon':make_pentagon
}

class WindowFrame(Base):
    def __init__(self):
        super().__init__()
        self.type = "hexagon" # hexagon, pentagon
        self.radius = 58
        self.height = 4
        self.pane_height = 1
        self.inner_pane_padding = 2
        self.pane_rail_translate = 0
        self.frame_size = 5

        self.outline = None
        self.pane_rail = None
        self.frame = None
        self.cut_key = None

    def _calc_radius(self):
        radius = self.radius

        if self.type == "pentagon" and self.parent and hasattr(self.parent, "pen_radius") and hasattr(self.parent, "pen_radius_cut"):
            radius = self.parent.pen_radius - self.parent.pen_radius_cut
        elif self.type == "hexagon" and self.parent and hasattr(self.parent, "hex_radius") and hasattr(self.parent, "hex_radius_cut"):
            radius = self.parent.hex_radius - self.parent.hex_radius_cut
        return radius
        
    def _resolve_make_method(self):
        if(self.type in _types):
            return _types[self.type]
        else:
            raise Exception(f'unknown make method type {self.type}')
            
    def __make_frame(self):
        radius = self._calc_radius()
        make_method = self._resolve_make_method()
        
        self.outline = make_method(radius, self.height,0)
        cut_frame = make_method(radius - self.frame_size, self.height,0)
        self.frame = self.outline.cut(cut_frame)
        
    def __make_pane_rail(self):
        radius = self._calc_radius()
        make_method = self._resolve_make_method()
        
        pane = make_method(radius, self.pane_height,0)
        inner_pane = make_method(
            radius - self.frame_size + self.inner_pane_padding, 
            self.pane_height, 
            0
        )
        pane_cut = (
            cq.Workplane("XY").box(radius, radius, self.pane_height)
            .translate((-1*(radius/2)+self.pane_rail_translate,0,0))
        )
        
        self.pane_rail = (
            pane
            .cut(pane_cut)
            .union(inner_pane)
        )



    def make(self, parent=None):
        super().make(parent)
        self.__make_frame()
        self.__make_pane_rail()


    def build(self):
        super().build()
        test = cq.Workplane("XY").box(10, 10, 10)
        
        window = (
            cq.Workplane("XY")
            .union(self.frame)
            .cut(self.pane_rail)
        )
        return window