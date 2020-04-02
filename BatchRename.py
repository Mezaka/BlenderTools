import bpy

name = "CreekTrack"
appendix = "[drag]"
selected = bpy.context.selected_objects

length = len(selected)

for i in range(length):
    number = str(i+1)
    while len(number)<3:
        number = str(0)+number
    selected[i].name = name+number+appendix
