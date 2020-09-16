bl_info = {
    "name": "Blender2Nier (NieR:Automata Model Exporter)",
    "author": "Woeful_Wolf",
    "version": (0, 1, 9),
    "blender": (2, 80, 0),
    "location": "File > Import-Export",
    "description": "Export Blender model to Nier:Automata wmb model data",
    "category": "Import-Export"}

import traceback
import sys
import bpy
from bpy_extras.io_utils import ExportHelper,ImportHelper
from bpy.props import StringProperty, BoolProperty, EnumProperty

class ExportBlender2Nier(bpy.types.Operator, ExportHelper):
    '''Export a NieR:Automata WMB File'''
    bl_idname = "export.wmb_data"
    bl_label = "Export WMB File"
    bl_options = {'PRESET'}
    filename_ext = ".wmb"
    filter_glob: StringProperty(default="*.wmb", options={'HIDDEN'})

    flip_normals: bpy.props.BoolProperty(name="Flip All Normals", description="NieR:Automata has inverted normals compared to Blender, thus leave enabled if using regular Blender normals.",  default=True)
    purge_materials: bpy.props.BoolProperty(name="Purge Materials", description="This permanently removes all unused materials from the .blend file before exporting. Enable if you have invalid materials remaining in your project.", default=False)

    use_visiable: bpy.props.BoolProperty(name="Visiable Objects", description="Export visible objects only", default=True)
    use_active_collection: bpy.props.BoolProperty(name="Active Collection", description="Export only objects from the active collection (and its children)", default=True)
    use_selection: bpy.props.BoolProperty(name="Selected Objects", description="Export selected and visible objects only", default=False)

    def execute(self, context):
        from . import wmb_exporter
        from . import util
        from . import export_ctx
        
        export_ctx.init_context_objects(self.use_visiable, self.use_active_collection, self.use_selection)
        if len(export_ctx.objects) == 0:
            util.show_message('No data to be exported...')
            return {'CANCELLED'}
        
        if self.flip_normals:
            wmb_exporter.flip_all_normals(self.flip_normals)

        if self.purge_materials:
            wmb_exporter.purge_unused_materials()

        try:
            wmb_exporter.main(self.filepath)
            wmb_exporter.flip_all_normals(self.flip_normals)
            print('EXPORT COMPLETE. :D')
            return {'FINISHED'}
        except:
            wmb_exporter.flip_all_normals(self.flip_normals)
            print(traceback.format_exc())
            util.show_message('Error: An unexpected error has occurred during export. Please check the console for more info.', 'WMB Export Error', 'ERROR')
            return {'CANCELLED'}

    def draw(self, context):
        pass

class BLENDER2NIER_PT_Main(bpy.types.Panel):
    '''Main Panel'''
    bl_space_type = 'FILE_BROWSER'
    bl_region_type = 'TOOL_PROPS'
    bl_label = ""
    bl_parent_id = "FILE_PT_operator"
    bl_options = {'HIDE_HEADER'}

    @classmethod
    def poll(cls, context):
        sfile = context.space_data
        operator = sfile.active_operator

        return operator.bl_idname == "EXPORT_OT_wmb_data"

    def draw(self, context):
        layout = self.layout

        layout.row()
    
        sfile = context.space_data
        operator = sfile.active_operator

        layout.prop(operator, "flip_normals")
        layout.prop(operator, "purge_materials")


class BLENDER2NIER_PT_Include(bpy.types.Panel):
    '''Include Panel'''
    bl_space_type = 'FILE_BROWSER'
    bl_region_type = 'TOOL_PROPS'
    bl_label = "Include"
    bl_parent_id = "FILE_PT_operator"

    @classmethod
    def poll(cls, context):
        sfile = context.space_data
        operator = sfile.active_operator

        return operator.bl_idname == "EXPORT_OT_wmb_data"

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False

        sfile = context.space_data
        operator = sfile.active_operator

        sublayout = layout.column(heading="Limit to")
        sublayout.prop(operator, "use_visiable")
        sublayout.prop(operator, "use_active_collection")
        sublayout.prop(operator, "use_selection")
        

def menu_func_export(self, context):
    self.layout.operator_context = 'INVOKE_DEFAULT'
    self.layout.operator(ExportBlender2Nier.bl_idname, text="WMB File for Nier: Automata (.wmb)")


export_classes = (
    ExportBlender2Nier,
    BLENDER2NIER_PT_Main,
    BLENDER2NIER_PT_Include
)

def register():
    from .wta_wtp_exporter import wta_wtp_ui_manager
    from .dat_dtt_exporter import dat_dtt_ui_manager

    for export_class in export_classes:
        bpy.utils.register_class(export_class)
    bpy.types.TOPBAR_MT_file_export.append(menu_func_export)
    wta_wtp_ui_manager.register()
    dat_dtt_ui_manager.register()


def unregister():
    from .wta_wtp_exporter import wta_wtp_ui_manager
    from .dat_dtt_exporter import dat_dtt_ui_manager

    for export_class in export_classes:
        bpy.utils.unregister_class(export_class)
    bpy.types.TOPBAR_MT_file_export.remove(menu_func_export)
    wta_wtp_ui_manager.unregister()
    dat_dtt_ui_manager.unregister()


if __name__ == '__main__':
    register()