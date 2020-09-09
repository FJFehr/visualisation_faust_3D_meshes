# This script will visualise the hand as a point cloud an mesh
# 9 June 2020
# Fabio Fehr

import open3d as o3d

# Read in mesh and compute normals
mesh = o3d.io.read_triangle_mesh("meshes/tr_reg_009.ply") #read in your .ply mesh
mesh.compute_vertex_normals()

# Show mesh
o3d.visualization.draw_geometries([mesh],mesh_show_wireframe=True)

# Zoom about to get the view of the hand you require and press P (for a screenshot and ctrl+C to coppy the view!)

# Here is the view
# {
# 	"class_name" : "ViewTrajectory",
# 	"interval" : 29,
# 	"is_loop" : false,
# 	"trajectory" :
# 	[
# 		{
# 			"boundingbox_max" : [ 0.48368588089942932, 1.0233516693115234, 0.30533051490783691 ],
# 			"boundingbox_min" : [ -0.34745797514915466, -1.1544585227966309, -0.085829161107540131 ],
# 			"field_of_view" : 60.0,
# 			"front" : [ -0.061617119981911321, 0.011758130080231459, 0.99803059918128334 ],
# 			"lookat" : [ 0.42699499472225155, 0.87734962096677394, -0.018764571727350667 ],
# 			"up" : [ 0.019539595913392833, 0.99975318725205919, -0.010572075051303692 ],
# 			"zoom" : 0.14000000000000001
# 		}
# 	],
# 	"version_major" : 1,
# 	"version_minor" : 0
# }

# Here is how we save the Point cloud image
mesh =o3d.io.read_point_cloud("meshes/tr_reg_009.ply") #read in your .ply mesh

col = [140, 140, 140]
col = [i / 255.0 for i in col]
mesh.paint_uniform_color(col)
vis = o3d.visualization.Visualizer()
vis.create_window()
ctr = vis.get_view_control()
vis.add_geometry(mesh)
ctr.set_lookat(lookat = [ 0.42699499472225155, 0.87734962096677394, -0.018764571727350667 ])
ctr.set_zoom(zoom=0.14)
ctr.set_front(front = [ -0.061617119981911321, 0.011758130080231459, 0.99803059918128334 ])
ctr.set_up(up = [ 0.019539595913392833, 0.99975318725205919, -0.010572075051303692 ])
vis.update_geometry(mesh)
vis.poll_events()
vis.capture_screen_image("pointCloudHand.png")
vis.destroy_window()

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
    if bbox:
        return im.crop(bbox)

plt.figure()
plt.tight_layout(pad=3)
plt.subplot(1, 2, 1)
img1 = Image.open("pointCloudHand.png")
img1 = trim(img1)
plt.imshow(img1)
plt.axis('off')
plt.title("Point cloud", fontsize=15, x = 0.55,y=-0.12)

plt.subplot(1, 2, 2)
img2 = Image.open("triangleMeshHand.png")
img2 = trim(img2)
plt.imshow(img2)
plt.axis('off')
plt.title("Triangle mesh", fontsize=15, x = 0.55,  y=-0.12)

plt.savefig('handDiagram.pdf', dpi=600)


