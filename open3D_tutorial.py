# This tutorial will walk through loading meshes and basic visualisations
# 9 June 2020
# Fabio Fehr

# http://www.open3d.org/docs/release/tutorial/Basic/index.html

# @article{Zhou2018,
#    author  = {Qian-Yi Zhou and Jaesik Park and Vladlen Koltun},
#    title   = {{Open3D}: {A} Modern Library for {3D} Data Processing},
#    journal = {arXiv:1801.09847},
#    year    = {2018},
# }

import open3d as o3d
import numpy as np
import os
import matplotlib.pyplot as plt

######################################################################################################################
# Load the .ply mesh #################################################################################################
######################################################################################################################

print("Testing mesh in open3d ...")
mesh = o3d.io.read_triangle_mesh("meshes/tr_reg_007.ply") #read in your .ply mesh
print(mesh)
print('Vertices:')
print(np.asarray(mesh.vertices))
print('Triangles:')
print(np.asarray(mesh.triangles))

######################################################################################################################
# Basic visualisation ################################################################################################
######################################################################################################################

# We can visualise a mesh!
# This results in just a grey figure no detail

#o3d.visualization.draw_geometries([mesh])
#print("A mesh with no normals and no colors does not look good.")

# Computing normals actually highlights the surface
print("Computing normal and rendering it.")
mesh.compute_vertex_normals()
print(np.asarray(mesh.triangle_normals))
o3d.visualization.draw_geometries([mesh])

# Now lets colour it
print("Painting the mesh")
mesh.paint_uniform_color([1, 0.706, 0])
o3d.visualization.draw_geometries([mesh])

######################################################################################################################
# Animation: Rotation ################################################################################################
######################################################################################################################

def custom_draw_geometry_with_rotation(pcd):

    def rotate_view(vis):
        ctr = vis.get_view_control()
        ctr.rotate(10.0, 0.0)
        return False

    o3d.visualization.draw_geometries_with_animation_callback([pcd],rotate_view)

custom_draw_geometry_with_rotation(mesh)

######################################################################################################################
# Animation: saving ##################################################################################################
######################################################################################################################

# Not sure how to save animations yet

def custom_draw_geometry_with_camera_trajectory(pcd):
    custom_draw_geometry_with_camera_trajectory.index = -1
    custom_draw_geometry_with_camera_trajectory.trajectory =\
            o3d.io.read_pinhole_camera_trajectory(
                    "../../TestData/camera_trajectory.json")
    custom_draw_geometry_with_camera_trajectory.vis = o3d.visualization.Visualizer(
    )
    if not os.path.exists("../../TestData/image/"):
        os.makedirs("../../TestData/image/")
    if not os.path.exists("../../TestData/depth/"):
        os.makedirs("../../TestData/depth/")

    def move_forward(vis):
        # This function is called within the o3d.visualization.Visualizer::run() loop
        # The run loop calls the function, then re-render
        # So the sequence in this function is to:
        # 1. Capture frame
        # 2. index++, check ending criteria
        # 3. Set camera
        # 4. (Re-render)
        ctr = vis.get_view_control()
        glb = custom_draw_geometry_with_camera_trajectory
        if glb.index >= 0:
            print("Capture image {:05d}".format(glb.index))
            depth = vis.capture_depth_float_buffer(False)
            image = vis.capture_screen_float_buffer(False)
            plt.imsave("../../TestData/depth/{:05d}.png".format(glb.index),\
                    np.asarray(depth), dpi = 1)
            plt.imsave("../../TestData/image/{:05d}.png".format(glb.index),\
                    np.asarray(image), dpi = 1)
            #vis.capture_depth_image("depth/{:05d}.png".format(glb.index), False)
            #vis.capture_screen_image("image/{:05d}.png".format(glb.index), False)
        glb.index = glb.index + 1
        if glb.index < len(glb.trajectory.parameters):
            ctr.convert_from_pinhole_camera_parameters(
                glb.trajectory.parameters[glb.index])
        else:
            custom_draw_geometry_with_camera_trajectory.vis.\
                    register_animation_callback(None)
        return False

    vis = custom_draw_geometry_with_camera_trajectory.vis
    vis.create_window()
    vis.add_geometry(pcd)
    vis.get_render_option().load_from_json("../../TestData/renderoption.json")
    vis.register_animation_callback(move_forward)
    vis.run()
    vis.destroy_window()

#custom_draw_geometry_with_camera_trajectory(mesh)

######################################################################################################################
# Animation: Set keys to do things ###################################################################################
######################################################################################################################

def custom_draw_geometry_with_key_callback(pcd):

    def change_background_to_black(vis):
        opt = vis.get_render_option()
        opt.background_color = np.asarray([0, 0, 0])
        return False

    def capture_depth(vis):
        depth = vis.capture_depth_float_buffer()
        plt.imshow(np.asarray(depth))
        plt.show()
        return False

    def capture_image(vis):
        image = vis.capture_screen_float_buffer()
        plt.imshow(np.asarray(image))
        plt.show()
        return False

    key_to_callback = {}
    key_to_callback[ord("K")] = change_background_to_black
    key_to_callback[ord(",")] = capture_depth
    key_to_callback[ord(".")] = capture_image
    o3d.visualization.draw_geometries_with_key_callbacks([pcd], key_to_callback)


custom_draw_geometry_with_key_callback(mesh)
