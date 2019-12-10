n = 10

import bpy

for i in range(0,n+1):
    bpy.context.object.active_material_index = i
    bpy.ops.object.material_slot_select()
    bpy.ops.mesh.region_to_loop()
    bpy.ops.mesh.mark_seam()
    
bpy.ops.mesh.select_all(action='DESELECT')
bpy.ops.mesh.edges_select_sharp(sharpness=1.309)
bpy.ops.mesh.mark_seam()

bpy.ops.mesh.select_all(action='SELECT')
bpy.ops.uv.unwrap(method='ANGLE_BASED', margin=0.0157059)
