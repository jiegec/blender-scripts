# Blender Scripts

## Bake vertex colors to texture image

- Run with: blender -b -P bake_vertex_colors_to_texture_image.py -- input_ply output_obj
- Tested with blender 3.0.0
- Input: PLY format with vertex color attributes i.e. rgb channels
- Output: OBJ format with texture image
- Blender version requirement: <= 3.6.0 due to api changes, see #1 for discussions
