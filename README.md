# Edge solidify
A python script for [Blender](https://www.blender.org/) to solidify edge only flat meshes. 

In the python script you can change the parameters height, width, z_offset, ends_offset

### Height
The height of the walls.

### Width
The width of the walls.

### Z_offset
The vertical offset of the wall's mesh. Common values are 1,0,-1 but can be any number. If this value is 1 the wall will be exactly on top of the original mesh. If -1 the wall will be below the mesh and for 0 will be on the middle. 

### Ends_offset
The length that the wall ends protrude. Can be any number but usually positive. If 0 then no protrusion, 1 equals half the width protrusion etc.

## Examples

![Example1 before](/images/img1_before.png)
![Example1 after](/images/img1_after.png)

![Example2 before](/images/img2_before.png)
![Example2 after](/images/img2_after.png)

![Example3 before](/images/img3_before.png)
![Example3 after](/images/img3_after.png)