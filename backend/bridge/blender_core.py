"""
Blender Core Wrapper
Provides a clean interface to interact with Blender's Python API (bpy)
"""
import bpy
import os
from typing import Dict, List, Any, Optional
import json


class BlenderCore:
    """Wrapper class for Blender operations"""
    
    def __init__(self):
        """Initialize Blender Core"""
        self.export_dir = os.path.join(os.path.dirname(__file__), '..', 'exports')
        os.makedirs(self.export_dir, exist_ok=True)
        self.clear_scene()
    
    def clear_scene(self) -> Dict[str, Any]:
        """Clear all objects from the current scene"""
        try:
            bpy.ops.object.select_all(action='SELECT')
            bpy.ops.object.delete(use_global=False)
            
            # Clear all mesh data
            for mesh in bpy.data.meshes:
                bpy.data.meshes.remove(mesh)
                
            return {"status": "success", "message": "Scene cleared"}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def create_primitive(self, primitive_type: str, name: str = None, 
                        location: tuple = (0, 0, 0), 
                        scale: tuple = (1, 1, 1)) -> Dict[str, Any]:
        """
        Create a primitive object
        
        Args:
            primitive_type: Type of primitive (cube, sphere, cylinder, cone, torus, plane)
            name: Optional name for the object
            location: (x, y, z) position
            scale: (x, y, z) scale
        """
        try:
            # Create primitive based on type
            if primitive_type == "cube":
                bpy.ops.mesh.primitive_cube_add(location=location)
            elif primitive_type == "sphere":
                bpy.ops.mesh.primitive_uv_sphere_add(location=location)
            elif primitive_type == "cylinder":
                bpy.ops.mesh.primitive_cylinder_add(location=location)
            elif primitive_type == "cone":
                bpy.ops.mesh.primitive_cone_add(location=location)
            elif primitive_type == "torus":
                bpy.ops.mesh.primitive_torus_add(location=location)
            elif primitive_type == "plane":
                bpy.ops.mesh.primitive_plane_add(location=location)
            else:
                return {"status": "error", "message": f"Unknown primitive type: {primitive_type}"}
            
            # Get the active object (the one just created)
            obj = bpy.context.active_object
            
            # Set name if provided
            if name:
                obj.name = name
            
            # Set scale
            obj.scale = scale
            
            return {
                "status": "success",
                "object_name": obj.name,
                "type": primitive_type,
                "location": list(location),
                "scale": list(scale)
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def apply_modifier(self, object_name: str, modifier_type: str, 
                      params: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Apply a modifier to an object
        
        Args:
            object_name: Name of the object
            modifier_type: Type of modifier (subdivision, bevel, array, etc.)
            params: Modifier parameters
        """
        try:
            obj = bpy.data.objects.get(object_name)
            if not obj:
                return {"status": "error", "message": f"Object '{object_name}' not found"}
            
            params = params or {}
            
            if modifier_type == "subdivision":
                mod = obj.modifiers.new(name="Subdivision", type='SUBSURF')
                mod.levels = params.get('levels', 2)
                mod.render_levels = params.get('render_levels', 2)
            elif modifier_type == "bevel":
                mod = obj.modifiers.new(name="Bevel", type='BEVEL')
                mod.width = params.get('width', 0.1)
                mod.segments = params.get('segments', 2)
            elif modifier_type == "array":
                mod = obj.modifiers.new(name="Array", type='ARRAY')
                mod.count = params.get('count', 3)
            else:
                return {"status": "error", "message": f"Unknown modifier type: {modifier_type}"}
            
            return {
                "status": "success",
                "object_name": object_name,
                "modifier": modifier_type,
                "params": params
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def export_scene(self, filename: str = "preview.glb") -> Dict[str, Any]:
        """
        Export the current scene to GLB format
        
        Args:
            filename: Output filename
        """
        try:
            filepath = os.path.join(self.export_dir, filename)
            
            # Export as GLB (GLTF 2.0 binary format)
            bpy.ops.export_scene.gltf(
                filepath=filepath,
                export_format='GLB',
                export_texcoords=True,
                export_normals=True,
                export_materials='EXPORT',
                export_colors=True,
                use_selection=False,
                export_cameras=False,
                export_lights=False
            )
            
            file_size = os.path.getsize(filepath)
            
            return {
                "status": "success",
                "filepath": filepath,
                "filename": filename,
                "size_bytes": file_size,
                "url": f"/api/preview/{filename}"
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def get_scene_info(self) -> Dict[str, Any]:
        """Get information about the current scene"""
        try:
            objects = []
            for obj in bpy.data.objects:
                objects.append({
                    "name": obj.name,
                    "type": obj.type,
                    "location": list(obj.location),
                    "scale": list(obj.scale),
                    "rotation": list(obj.rotation_euler)
                })
            
            return {
                "status": "success",
                "object_count": len(objects),
                "objects": objects
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def update_object_transform(self, object_name: str, 
                               location: Optional[tuple] = None,
                               rotation: Optional[tuple] = None,
                               scale: Optional[tuple] = None) -> Dict[str, Any]:
        """Update object transformation"""
        try:
            obj = bpy.data.objects.get(object_name)
            if not obj:
                return {"status": "error", "message": f"Object '{object_name}' not found"}
            
            if location:
                obj.location = location
            if rotation:
                obj.rotation_euler = rotation
            if scale:
                obj.scale = scale
            
            return {
                "status": "success",
                "object_name": object_name,
                "location": list(obj.location),
                "rotation": list(obj.rotation_euler),
                "scale": list(obj.scale)
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}
