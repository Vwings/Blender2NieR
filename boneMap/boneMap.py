import bpy, bmesh, math
from .. import export_ctx

class c_boneMap(object):
    def __init__(self, bones):
        boneMap = []
        for obj in export_ctx.objects:
            if obj.type == 'ARMATURE':
                boneMap = obj.data['boneMap']
        
        self.boneMap = boneMap

        self.boneMap_StructSize = len(boneMap) * 4