# Tested with blender 3.0.0
# Run with: blender -b -P texture.py -- input_ply output_obj

import bpy
import argparse
import sys
import os

index = sys.argv.index('--')

parser = argparse.ArgumentParser(
    description='Bake vertex colors to texture image')
parser.add_argument('input_ply', type=str,
                    help='Input PLY File')
parser.add_argument('output_obj', type=str,
                    help='Output OBJ File')

args = parser.parse_args(sys.argv[index:])
input_ply = args.input_ply
output_obj = args.output_obj
name, _ = os.path.splitext(output_obj)
output_png = '{}.png'.format(name)
output_mtl = '{}.mtl'.format(name)

print('Input PLY: {}'.format(input_ply))
print('Output OBJ: {}'.format(output_obj))
print('Output PNG: {}'.format(output_png))
print('Output MTL: {}'.format(output_mtl))

# https://docs.blender.org/api/current/bpy.data.html
print('Remove default cube mesh')
if "Cube" in bpy.data.meshes:
    mesh = bpy.data.meshes["Cube"]
    bpy.data.meshes.remove(mesh)

print('Import PLY')
bpy.ops.import_mesh.ply(
    filepath=input_ply)

print('Toggle edit mode')
bpy.ops.object.editmode_toggle()

print('UV smart project')
bpy.ops.uv.smart_project()

# https://blender.stackexchange.com/questions/5668/add-nodes-to-material-with-python
print('Add shading material')
material = bpy.data.materials.new('SomeMaterial')
material.use_nodes = True
nodes = material.node_tree.nodes

print('Toggle edit mode')
bpy.ops.object.editmode_toggle()

print('Add input vertex color')
input_node = nodes.new('ShaderNodeVertexColor')
bsdf_node = nodes.get('Principled BSDF')

print('Link vertex color to bsdf')
material.node_tree.links.new(bsdf_node.inputs[0], input_node.outputs[0])

print('Add texture image')
texture_node = nodes.new('ShaderNodeTexImage')
texture_node.select = True
nodes.active = texture_node

print('Create empty image')
image = bpy.data.images.new(name='SomeImage', width=1024, height=1024)

print('Assign image to node')
texture_node.image = image

print('Switch to CYCLES render engine')
bpy.context.scene.render.engine = 'CYCLES'

print('Select active material')
bpy.context.active_object.active_material = material

print('Bake image')
bpy.context.scene.cycles.bake_type = 'DIFFUSE'
bpy.context.scene.render.bake.use_pass_direct = False
bpy.context.scene.render.bake.use_pass_indirect = False
bpy.context.view_layer.objects.active = bpy.context.active_object
print(bpy.ops.object.bake(type='DIFFUSE',
      pass_filter={'COLOR'}, use_clear=True))

print('Save image')
image.save_render(output_png)

# set map_Kd correctly in mtl file
image.filepath = os.path.basename(output_png)

print('Connect texture node to bsdf')
material.node_tree.links.new(bsdf_node.inputs[0], texture_node.outputs[0])

print('Export OBJ')
bpy.ops.export_scene.obj(filepath=output_obj)
