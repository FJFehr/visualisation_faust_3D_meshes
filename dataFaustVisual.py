# This script will visualise the hand as a point cloud an mesh
# 9 June 2020
# Fabio Fehr

import open3d as o3d
import glob2
def loadMeshes(direc="meshes/", ply_Bool=True):
    '''
    Provided a directory of .ply meshes (default) otherwise .stl format. This function reads them in and returns a list of meshes

    :param direc: directory of meshes
    :return: List of meshes
    '''
    if (ply_Bool):
        paths = glob2.glob(direc + "*.ply")
    else:
        paths = glob2.glob(direc + "*.stl")

    paths = sorted(paths)  # makes sure its in the correct order
    meshes = [o3d.io.read_triangle_mesh(path) for path in paths]
    return meshes
#
# meshes = loadMeshes("../meshes/")
#
#
import matplotlib.pyplot as plt
from PIL import Image, ImageChops

def trim(im):

    '''
    This function trims the white space of an image

    :param im: image
    :return: trimmed image
    '''
    bg = Image.new(im.mode, im.size, im.getpixel((0, 0)))
    diff = ImageChops.difference(im, bg)
    diff = ImageChops.add(diff, diff, 2.0, -100)
    bbox = diff.getbbox()
    print(bbox)
    if bbox:
        return im.crop((749,21,1098,801)) #left, upper, right, and lower pixel coordinate.
#
#
#
# plt.figure()
# plt.tight_layout(pad=3)
# plt.subplot(1, 2, 1)
# img1 = Image.open("pointCloudHand.png")
# img1 = trim(img1)
# plt.imshow(img1)
# plt.axis('off')
# plt.title("Point cloud", fontsize=15, x = 0.55,y=-0.12)
#
# plt.subplot(1, 2, 2)
# img2 = Image.open("triangleMeshHand.png")
# img2 = trim(img2)
# plt.imshow(img2)
# plt.axis('off')
# plt.title("Triangle mesh", fontsize=15, x = 0.55,  y=-0.12)
#
# plt.savefig('handDiagram.pdf', dpi=600)
#
#
def meshVisSave(mesh, path, col, cameraName):
    '''
    This function saves a mesh visualisation as png

    :param mesh: 3D mesh obj from open3D
    :param path: path and name to where you would like it saved
    :param col: The colour in a list [255,255,255]
    :param x_rotation: The amount you rotate in the x direction
    :param y_rotation: The amount you rotate in the y direction
    :return: saves mesh
    '''
    # compute normals to visualise
    mesh.compute_vertex_normals()

    # convert the 255 code to be between 0-1 of Open3d
    col = [i / 255.0 for i in col]
    mesh.paint_uniform_color(col)
    vis = o3d.visualization.Visualizer()
    vis.create_window()
    ctr = vis.get_view_control()
    vis.add_geometry(mesh)
    parameters = o3d.io.read_pinhole_camera_parameters(cameraName+"CameraSettings.json")
    ctr.convert_from_pinhole_camera_parameters(parameters)
    vis.update_geometry(mesh)
    vis.poll_events()
    vis.capture_screen_image(path + ".png")
    vis.destroy_window()

meshes = loadMeshes("meshes/")
plt.figure()
label = ['a','b','c','d','e','f','g','h','i','j']
for i in range(1,11):
    j = i+((i-1)*10)-1 # This gives the correct sequence I need
    meshVisSave(meshes[j],"faust"+str(j), [180, 180, 180],cameraName="faust") # Saves the correct ones

    plt.subplot(2, 5, i)
    img = Image.open("faust"+str(j)+".png")
    img = trim(img)
    plt.imshow(img)
    plt.axis('off')
    # plt.ylim(700, 0)
    # plt.title(str(i)+label[i-1])
    plt.title(f'${str(i)}{label[i-1]}$', fontsize = 8,y=-0.1)


plt.tight_layout(pad=0.4, w_pad=0.5, h_pad=1.0)
plt.savefig('faustDiagram.pdf', dpi=300)

# meshes = loadMeshes("meshes/")
# plt.figure()
# for i in range(1,50):
#     meshVisSave(meshes[i],"faust"+str(i), [180, 180, 180],cameraName="faust") # Saves the correct ones
#     img = Image.open("faust"+str(i)+".png")
#     img = trim(img)
#     plt.imshow(img)
#     plt.axis('off')
#     # plt.ylim(700, 0)

# (min,min,max,max)
# bbox = (749,50,1092,801)  left, upper, right, and lower pixel coordinate.



