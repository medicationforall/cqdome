import cadquery as cq
from cqdome import Dome, greeble

test_bp = greeble.CutKeyPentagon()
test_bp_2 = greeble.CutKeyHexagon()
#test_bp_2.text_height=10
vent_bp = greeble.VentHexagon()
door_bp = greeble.DoorHexagon()
door_bp.hinge_x_translate = -4.5

bp = Dome()
bp.render_cut_keys = False
bp.r1_greeble = []
bp.r2_greeble_hex = [1,2]

#center
bp.greebles_bp.append(None)

#ring 1
bp.greebles_bp.append(None)
bp.greebles_bp.append(None)
bp.greebles_bp.append(None)
bp.greebles_bp.append(None)
bp.greebles_bp.append(None)

#ring2
#bp.greebles_bp.append(vent_bp)
bp.make()
#door_bp.parent=None
#door_bp.make()
dome = bp.build()
#show_object(dome)

cq.exporters.export(dome, "./stl/dome_v3_test.stl")