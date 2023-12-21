# Copyright 2023 James Adams
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import cadquery as cq
from . import BasePentagon, make_pentagon

class CutKeyPentagon(BasePentagon):
    def __init__(self):
        super().__init__()
        self.radius = 58
        self.height = 2

        # text
        self.text = "MiniForAll" 
        self.text_height = 2
        self.text_size = 7

        #cut hole
        self.cut_hole_height = 3
        self.cut_hole_radius = 1.5
        self.cut_hole_y_translate = 12

        self.cut_key = None

    def _calc_radius(self):
        radius = self.radius

        if self.parent and hasattr(self.parent, "pen_radius") and hasattr(self.parent, "pen_radius_cut"):
            radius = self.parent.pen_radius - self.parent.pen_radius_cut
        return radius

    def make(self, parent=None):
        super().make(parent)

        radius = self._calc_radius()

        cut_key = make_pentagon(radius, self.height, 0)

        logo_text = (
            cq.Workplane("XY")
            .text(self.text,self.text_size, self.text_height)
            .translate((-.5,0,0))
        )
        cut_hole = (
            cq.Workplane("XY")
            .cylinder(self.cut_hole_height, self.cut_hole_radius)
            .translate((0, self.cut_hole_y_translate, 0))
        )

        self.cut_key = (
            cut_key
            .union(logo_text)
            .cut(cut_hole)
            .translate((0,0,self.height/2))
        )


    def build(self):
        super().make()
        return self.cut_key