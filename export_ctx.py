import bpy

objects = []
materials = []

def init_context_objects(use_visiable, use_active_collection, use_selection):
    global objects
    global materials
    context = bpy.context
    if use_active_collection:
        if use_visiable:
            objects = tuple(obj
                                for obj in context.view_layer.active_layer_collection.collection.all_objects
                                if not obj.hide_get())
        elif use_selection:
            objects = tuple(obj
                                for obj in context.view_layer.active_layer_collection.collection.all_objects
                                if obj.select_get())
        else:
            objects = context.view_layer.active_layer_collection.collection.all_objects
    else:
        if use_visiable:
            objects = context.visible_objects
        elif use_selection:
            objects = context.selected_objects
        else:
            objects = context.view_layer.objects

    objects = sorted((obj for obj in objects if obj.type in ['MESH', 'ARMATURE']), key=lambda obj: obj.name)
    
    materials_map = {}
    for obj in objects:
        if obj.type == 'MESH':
            material = obj.material_slots[0].material
            if material.name not in materials_map:
                materials_map[material.name] = material
                
    materials = list(materials_map.values())
    
    print ('Init materials, length: ', len(materials))