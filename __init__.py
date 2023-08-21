dependencies = {
    'pip': {},
    'pymeshlab': {"url": "https://pymeshlab.readthedocs.io/en/latest/"},
}

for dependency in dependencies:
    if dependency != 'pip':
        try:
            __import__(dependency)
        except ImportError:
            import sys, subprocess
            subprocess.call([sys.executable, "-m", "pip", "install", dependency])

import bpy
from bpy_extras.io_utils import ExportHelper

import pymeshlab
import numpy as np

bl_info = {
    "name": "U3D Exporter",
    "author": "kmarchais",
    "version": (0, 1),
    "blender": (3, 0, 0),
    "location": "File > Import-Export",
    "description": "Export U3D files",
    "warning": "",
    "doc_url": "https://github.com/kmarchais/blender-u3d-exporter",
    "category": "Import-Export",
}

class ExportU3D(bpy.types.Operator, ExportHelper):
    """Export to U3D"""
    bl_idname = "export.u3d"
    bl_label = "Export U3D"

    filename_ext = ".u3d"

    filter_glob: bpy.props.StringProperty(
        default="*.u3d",
        options={'HIDDEN'},
        maxlen=255,  # Max internal buffer length, longer would be clamped.
    )

    position_val: bpy.props.FloatVectorProperty(
        name="Position",
        description="Position",
        default=(0.0, 0.0, -1.73205),
        subtype='XYZ',
        size=3,
    )

    target_val: bpy.props.FloatVectorProperty(
        name="Target",
        description="Target",
        default=(0.0, 0.0, 0.0),
        subtype='XYZ',
        size=3,
    )

    fov_val: bpy.props.FloatProperty(
        name="FOV",
        description="FOV",
        default=60.0,
    )

    compression_val: bpy.props.IntProperty(
        name="Compression",
        description="Compression",
        default=500,
        min=0,
        max=1000,
    )

    save_vertex_color: bpy.props.BoolProperty(
        name="Save Vertex Color",
        description="Save Vertex Color",
        default=False,
    )

    save_face_color: bpy.props.BoolProperty(
        name="Save Face Color",
        description="Save Face Color",
        default=False,
    )

    save_wedge_texcoord: bpy.props.BoolProperty(
        name="Save Wedge Texcoord",
        description="Save Wedge Texcoord",
        default=False,
    )

    def execute(self, context):
        obj = context.active_object

        vertices = obj.data.vertices
        faces = obj.data.polygons

        vertices = np.array([vertex.co for vertex in vertices])
        faces = np.array([face.vertices[:] for face in faces])

        mesh = pymeshlab.Mesh(vertices, faces)
        ms = pymeshlab.MeshSet()
        ms.add_mesh(mesh)

        ms.save_current_mesh(
            file_name=self.filepath,
            position_val=np.array(self.position_val),
            target_val=np.array(self.target_val),
            fov_val=self.fov_val,
            compression_val=self.compression_val,
            save_vertex_color=self.save_vertex_color,
            save_face_color=self.save_face_color,
            save_wedge_texcoord=self.save_wedge_texcoord,
        )

        return {'FINISHED'}


def menu_func_import(self, context):
    self.layout.operator(ExportU3D.bl_idname, text="U3D (.u3d)")

def register():
    bpy.utils.register_class(ExportU3D)
    bpy.types.TOPBAR_MT_file_export.append(menu_func_import)

def unregister():
    bpy.utils.unregister_class(ExportU3D)
    bpy.types.TOPBAR_MT_file_export.remove(menu_func_import)
