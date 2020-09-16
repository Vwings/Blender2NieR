import bpy, bmesh, math
from .mesh import *
from .. import export_ctx

class c_meshes(object):
    def __init__(self, offsetMeshes):

        def get_meshes(self, offsetMeshes):
            meshes = []
            meshes_names_added = []
            numMeshes = 0

            # groupedMeshOrder = []
            # for obj in export_ctx.objects:
            #     if obj.type == 'MESH':
            #         meshGroupIndex = obj["meshGroupIndex"]

            # for obj in export_ctx.objects:
            #     if obj.type == 'MESH':
            #         obj_name = obj.name.split('-')
            #         if obj_name[1] not in meshes_names_added:
            #             numMeshes += 1
            #             meshes_names_added.append(obj_name[1])

            # currentGroupIndex = 0
            
            # print('meshGroupIndex:', meshGroupIndex)
            # print('numMeshes', numMeshes)
            
            # groupedMeshObjOrder = []
            # while len(groupedMeshObjOrder) < numMeshes:
            #     for obj in export_ctx.objects:
            #         if obj.type == 'MESH':
            #             meshGroupIndex = obj["meshGroupIndex"]
            #             if meshGroupIndex == currentGroupIndex:
            #                 groupedMeshObjOrder.append(obj)
            #                 currentGroupIndex += 1

            groupedMeshObjOrder = sorted((obj for obj in export_ctx.objects if obj.type == 'MESH'), key=lambda obj: obj['meshGroupIndex'])

            meshes_names_added = []
            for obj in groupedMeshObjOrder:
                # if obj.type == 'MESH':
                obj_name = obj.name.split('-')
                if obj_name[1] not in meshes_names_added:
                    print('[+] Generating Mesh', obj.name)
                    mesh = c_mesh(offsetMeshes, numMeshes, obj)
                    meshes.append(mesh)
                    meshes_names_added.append(mesh.name)
                    offsetMeshes += len(mesh.name) + 1 + mesh.numMaterials * 2 + mesh.numBones * 2

            return meshes

        def get_meshes_StructSize(self, meshes):
            meshes_StructSize = 0
            for mesh in meshes:
                meshes_StructSize += mesh.mesh_StructSize
            return meshes_StructSize

        self.meshes = get_meshes(self, offsetMeshes)

        self.meshes_StructSize = get_meshes_StructSize(self, self.meshes)