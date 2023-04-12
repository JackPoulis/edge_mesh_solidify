import bpy
import bmesh
import numpy as np
from mathutils import Vector
from math import atan2

width = 0.2
height = 2
z_offset = 0 # The vertical offset (common values are from -1 to 1)
ends_offset = 0 # The end points offset (common values are from 0 to 1)

z_disp = 1/2*(z_offset - 1)*height
hw = width/2
ends_disp = ends_offset*hw

# Get the active mesh
active_obj = bpy.context.object.data

# Get a BMesh representation
bm = bmesh.new()   # create an empty BMesh
bm.from_mesh(active_obj)   # fill it in from a Mesh

def unit_vector(vector):
    return vector / np.linalg.norm(vector)

def cart2pol(x, y):
    rho = np.sqrt(x**2 + y**2)
    phi = np.arctan2(y, x)
    return [rho, phi]

def pol2cart(rho, phi):
    x = rho * np.cos(phi)
    y = rho * np.sin(phi)
    return [x, y]

def create_vertice(vector):
    new_vertice = bm.verts.new(vector)
    new_vertice.index = len(bm.verts)-1
    return new_vertice

joints = [None]*len(bm.verts)
edges = []
for k in range(len(bm.edges)):
    edges.append([])

for v in bm.verts:
    if(len(v.link_edges)==1):
        linked_vertice = Vector(v.link_edges[0].other_vert(v).co)
        disp_vector = Vector(v.co)
        disp_vector -= linked_vertice
        disp_vector = unit_vector(disp_vector)
        disp_vector_90 = Vector([disp_vector.y, -disp_vector.x, disp_vector.z])
        disp_vector = Vector([0,0,z_disp]) + disp_vector*ends_disp
        new_point_a = Vector(disp_vector_90*hw + v.co + disp_vector)
        new_point_b = Vector(-disp_vector_90*hw + v.co + disp_vector)
        n_vert_a = create_vertice(new_point_a)
        n_vert_b = create_vertice(new_point_b)
        
        this_joint = [n_vert_a, n_vert_b]
        joints[v.index] = this_joint
        edges[v.link_edges[0].index].extend([n_vert_a, n_vert_b])
    
    #If the vertice is connected to more than 1 edge   
    elif(len(v.link_edges)>1):
        linked_verts = []
        this_joint = []
        
        #Create a list of points/vectors with all the connected vertices
        for le in v.link_edges:
            temp = Vector(le.other_vert(v).co)
            temp -= v.co
            p_temp = cart2pol(temp.x, temp.y)
            linked_verts.append([le.index, p_temp[1]])
        
        #Sort the point list from smallest polar coordinates angle to largests
        linked_verts.sort(key = lambda x: x[1])
        
        #For each pair of connected edges create a corner point 
        for i in range(-1,len(linked_verts)-1):
            a = np.abs(linked_verts[i+1][1] - linked_verts[i][1])
            theta = (linked_verts[i+1][1] + linked_verts[i][1])/2
            if(i==-1):
                theta += np.pi
            p_corner = [hw/np.sin(a/2), theta]
            c_corner = pol2cart(p_corner[0], p_corner[1])
            new_point = Vector([c_corner[0], c_corner[1] , z_disp]) + v.co
            n_vertice = create_vertice(new_point)
            
            this_joint.append(n_vertice)
            edges[linked_verts[i][0]].append(n_vertice)
            edges[linked_verts[i+1][0]].append(n_vertice)
        
        joints[v.index] = this_joint

faces = []
for joint in joints:
    new_geom = bmesh.ops.contextual_create(bm, geom = joint)
#    print(new_geom["faces"])
    if (len(new_geom["faces"]) > 0):
        faces.append(new_geom["faces"][0])

for edge_group in edges:
    new_geom = bmesh.ops.contextual_create(bm, geom = edge_group)
    if (len(new_geom["faces"]) >= 0):
        faces.append(new_geom["faces"][0])

# Extrude 
extruded = bmesh.ops.extrude_face_region(bm, geom=faces)
# Move extruded geometry
translate_verts = [v for v in extruded['geom'] if isinstance(v, bmesh.types.BMVert)]

up = Vector((0, 0, height))
bmesh.ops.translate(bm, vec=up, verts=translate_verts)

# Finish up, write the bmesh back to the mesh
bm.to_mesh(active_obj)
bm.free()  # free and prevent further access