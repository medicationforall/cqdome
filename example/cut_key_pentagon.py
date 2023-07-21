import cadquery as cq
from cqdome import greeble

bp = greeble.CutKeyPentagon()
bp.radius = 58
bp.text = "MiniForAll" 
bp.make()
cut_key = bp.build()

#show_object(cut_key)
cq.exporters.export(cut_key,'stl/CutKeyPentagon.stl')