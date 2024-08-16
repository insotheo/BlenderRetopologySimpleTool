import bpy

class OBJECT_OT_retopology(bpy.types.Operator):
    bl_idname = "object.retopology"
    bl_label = "Perform Retopology"
    bl_options = {'REGISTER', 'UNDO'}
    
    target: bpy.props.EnumProperty(
        name="Target",
        description="Select the target object type",
        items=[
            ('MESH', "Mesh", "Retopology on selected mesh"),
            ('GRID', "Grid", "Retopology on a grid"),
        ],
        default='MESH'
    )
    
    polycount: bpy.props.IntProperty(
        name="Desired Polycount",
        description="Desired number of polygons",
        default=1000,
        min=12
    )
    
    iterations: bpy.props.IntProperty(
        name="Iterations",
        description="Number of iterations",
        default=1,
        min=1,
        max=50
    )
    
    algorithm: bpy.props.EnumProperty(
        name="Algorithm",
        description="Choose the retopology algorithm",
        items=[
            ('REMESH', "Remesh", "Use Remesh modifier"),
            ('DECIMATE', "Decimate", "Use Decimate modifier")
        ],
        default='DECIMATE'
    )

    remesh_detail: bpy.props.IntProperty(
        name="Remesh Detail",
        description="Octree depth for the Remesh modifier (higher = finer detail)",
        default=6,
        min=0,
        max=10
    )
    
    preserve_uvs: bpy.props.BoolProperty(
        name="Preserve UVs",
        description="Try to preserve UV mapping during retopology",
        default=False
    )

    smooth_shading: bpy.props.BoolProperty(
        name="Smooth Shading",
        description="Apply smooth shading to the new mesh",
        default=False
    )
    
    triangulate: bpy.props.BoolProperty(
        name="Triangulate Result",
        description="Output the retopo mesh as triangles",
        default=True
    )

    @classmethod
    def poll(cls, context):
        return context.active_object and context.active_object.type == 'MESH'

    def invoke(self, context, event):
        # Получаем активный объект и устанавливаем максимальное значение полигонов
        obj = context.active_object
        if obj:
            self.polycount = len(obj.data.polygons)
        return self.execute(context)

    def execute(self, context):
        obj = context.active_object
        
        if self.target == 'GRID':
            bpy.ops.mesh.primitive_grid_add(size=10, enter_editmode=False, align='WORLD', location=(0, 0, 0))
            obj = context.active_object
        
        if not obj or obj.type != 'MESH':
            self.report({'ERROR'}, "No mesh object selected")
            return {'CANCELLED'}
        
        if self.algorithm == 'REMESH':
            bpy.ops.object.modifier_add(type='REMESH')
            obj.modifiers["Remesh"].mode = 'SHARP'
            obj.modifiers["Remesh"].octree_depth = self.remesh_detail
            bpy.ops.object.modifier_apply(modifier="Remesh")
        
        elif self.algorithm == 'DECIMATE':
            bpy.ops.object.modifier_add(type='DECIMATE')
            obj.modifiers["Decimate"].ratio = self.polycount / len(obj.data.polygons)
            bpy.ops.object.modifier_apply(modifier="Decimate")

        if self.preserve_uvs and len(obj.data.uv_layers) > 0:
            uv_layer = obj.data.uv_layers.active.data
            print("Preserving UVs is not fully implemented.")
        
        if self.smooth_shading:
            bpy.ops.object.shade_smooth()
        
        if self.triangulate:
            bpy.ops.object.modifier_add(type='TRIANGULATE')
            bpy.ops.object.modifier_apply(modifier="Triangulate")

        for _ in range(self.iterations):
            if self.algorithm == 'REMESH':
                bpy.ops.object.modifier_add(type='REMESH')
                obj.modifiers["Remesh"].mode = 'SHARP'
                obj.modifiers["Remesh"].octree_depth = self.remesh_detail
                bpy.ops.object.modifier_apply(modifier="Remesh")
            elif self.algorithm == 'DECIMATE':
                bpy.ops.object.modifier_add(type='DECIMATE')
                obj.modifiers["Decimate"].ratio = self.polycount / len(obj.data.polygons)
                bpy.ops.object.modifier_apply(modifier="Decimate")
        
        return {'FINISHED'}

class VIEW3D_PT_retopology(bpy.types.Panel):
    bl_label = "Retopology"
    bl_idname = "VIEW3D_PT_retopology"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Tools'
    
    def draw(self, context):
        layout = self.layout
        layout.operator(OBJECT_OT_retopology.bl_idname, text="Confirm")

def register():
    bpy.utils.register_class(OBJECT_OT_retopology)
    bpy.utils.register_class(VIEW3D_PT_retopology)

def unregister():
    bpy.utils.unregister_class(OBJECT_OT_retopology)
    bpy.utils.unregister_class(VIEW3D_PT_retopology)

if __name__ == "__main__":
    register()