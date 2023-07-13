import cadquery as cq
from cqdome import Dome

bp = Dome()
bp.make()
#print(dir(bp))
dome,door,vent,keys = bp.build_plate_parts()

#show_object(test)
cq.exporters.export(dome, "./stl/parts_dome_frame.stl")
cq.exporters.export(door, "./stl/parts_door.stl")
cq.exporters.export(vent, "./stl/parts_vent.stl")
cq.exporters.export(keys, "./stl/parts_keys.stl")
