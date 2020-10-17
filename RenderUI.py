import bpy
import math
import os

pixelsPerUnit = 424.0
selectChildren = True
autoSaveRender = True

objectName = bpy.context.selected_objects[0].name

if selectChildren:
    for i in range(0,10):
        bpy.ops.object.select_hierarchy(direction='CHILD', extend=True)

resolutionX = bpy.context.scene.render.resolution_x
resolutionY = bpy.context.scene.render.resolution_y

#calculate boundign box
maxX = -math.inf
maxY = -math.inf

minX = math.inf
minY = math.inf

#Buffer objetcs as names so struct RNA stays intact
myObjects = bpy.context.selected_objects
myObjectNames = list()
for obj in myObjects:
    myObjectNames.append(obj.name)

for name in myObjectNames:
    bpy.ops.ed.undo_push()
    
    #make single user
    override = bpy.context.copy()
    override['selected_objects'] = list([bpy.data.objects[name]])
    bpy.ops.object.make_single_user(obdata=True)
    
    #convert to mesh
    override = bpy.context.copy()
    override['selected_objects'] = list([bpy.data.objects[name]])
    bpy.ops.object.convert(target='MESH')
    
    #apply transform
    override = bpy.context.copy()
    override['selected_objects'] = list([bpy.data.objects[name]])
    bpy.ops.object.transform_apply(override, location=False, rotation=True, scale=True)
    
    
    aaBoundingBox = bpy.data.objects[name].bound_box
    location = bpy.data.objects[name].location
    maxX = max(maxX, aaBoundingBox[7][0]+location.x)
    maxY = max(maxY, aaBoundingBox[7][1]+location.y)
    
    minX = min(minX, aaBoundingBox[0][0]+location.x)
    minY = min(minY, aaBoundingBox[0][1]+location.y)
    
    bpy.ops.ed.undo_push()
    
    bpy.ops.ed.undo()

#calculate helpers
centerX = (maxX-minX)*0.5+minX
centerY = (maxY-minY)*0.5+minY

sizeX = maxX - minX
sizeY = maxY - minY

#Set Scene Resolution
bpy.context.scene.render.resolution_x = sizeX*pixelsPerUnit
bpy.context.scene.render.resolution_y = sizeY*pixelsPerUnit

#Set Camera Scale
cam = bpy.data.cameras["Camera.001"]
cam.ortho_scale = max(sizeX,sizeY)

#set Camera Position
bpy.data.objects["Camera"].location[0] = centerX
bpy.data.objects["Camera"].location[1] = centerY
bpy.data.objects["Camera"].location[2] = 50

#hide Objects
for obj in bpy.data.objects:
    obj.hide_render = not obj in bpy.context.selected_objects

#render scene
bpy.ops.render.render(use_viewport=True)

#save render
if autoSaveRender:
    blend_path = bpy.data.filepath
    assert blend_path # abort if .blend is not unsaved
    blend_path = os.path.dirname(bpy.path.abspath(blend_path))

    dirpath = os.path.join(blend_path, "Images")

    collectionName = bpy.context.selected_objects[0].users_collection[0].name
    dirpath = os.path.join(dirpath, collectionName)
    os.makedirs(dirpath, exist_ok=True)

    name = objectName.replace(".","")
    filepath = os.path.join(dirpath, name+".png")

    bpy.data.images["Render Result"].save_render(filepath)
    
    print("Saved "+filepath+name+".png")
