import bpy, bmesh, math

from .vertexGroup import c_vertexGroup
from .. import export_ctx

class c_vertexGroups(object):
    def __init__(self, offsetVertexGroups):
        self.offsetVertexGroups = offsetVertexGroups

        def get_vertexGroups(self, offsetVertexGroups):
            vertexGroupIndex = []

            for obj in export_ctx.objects:
                if obj.type == 'MESH':
                    obj_name = obj.name.split('-')
                    obj_vertexGroupIndex = int(obj_name[-1])
                    if obj_vertexGroupIndex not in vertexGroupIndex:
                        vertexGroupIndex.append(obj_vertexGroupIndex)

            vertexGroupIndex.sort()

            vertexesOffset = offsetVertexGroups + len(vertexGroupIndex) * 48
            
            vertexGroups = []
            for index in vertexGroupIndex:
                print('[+] Creating Vertex Group', index)
                vertexGroup = c_vertexGroup(index, vertexesOffset)
                vertexGroups.append(vertexGroup)
                vertexesOffset += vertexGroup.vertexGroupSize
            return vertexGroups

        self.vertexGroups = get_vertexGroups(self, self.offsetVertexGroups)

        def get_vertexGroupsSize(self, vertexGroups):
            vertexGroupsSize = len(vertexGroups) * 48

            for vertexGroup in vertexGroups:
                vertexGroupsSize += vertexGroup.vertexGroupSize
            return vertexGroupsSize

        self.vertexGroups_StructSize = get_vertexGroupsSize(self, self.vertexGroups)