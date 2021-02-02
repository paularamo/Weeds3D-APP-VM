# -*- coding: utf-8 -*-
import numpy as np 
import pandas as pd
import open3d as o3d
from collections import defaultdict
# import json, codecs
import os
import matplotlib.pyplot as plt
# from pyntcloud import PyntCloud
# from ReadBundleOut import read_bundle_out

root_dir='D:/00_NCSU/00_Resources/00_Datasets/PartTimePSA/ClusteringExp/MD-301/20'
cld_dir='D:/00_NCSU/Spring2021/00_PartTime/00_Scripts/'
ply_dir=cld_dir+'MD-301-PLY/'
def read_point_clouds_from_folder(root_dir, voxel_size=0.0):
    pmvs_files=[]
    pcds=[]
    volumes=[]
    for root, dirs, files in os.walk(root_dir):
        for i,file in enumerate(files):
            if file.endswith("pmvs_options.txt.ply"):
                 print(os.path.join(root, file))
                 pmvs_files.append(os.path.join(root, file))
                 pcd=o3d.io.read_point_cloud(pmvs_files[-1], format='ply')
                 # pcd.colors = o3d.utility.Vector3dVector(rgb_t.astype(np.float)/255.0)
                 pcd_down = pcd.voxel_down_sample(voxel_size=voxel_size)
                 pcds.append(pcd_down)
    return pcds

def scale_pt_clouds(pcds):
    volumes=[]
    pcds_scaled=[]
    for pcd in pcds: 
        obb = pcd.get_oriented_bounding_box()
        obb.color = (0, 1, 0)
        volumes.append(obb.volume())
    print(volumes)
    mean_volume=np.mean(volumes)
    for i,pcd in enumerate(pcds):
        pcd_scaled=pcd.scale(mean_volume/volumes[i], center=pcd.get_center())
        pcds_scaled.append(pcd_scaled)
        # if i>1:
        #     pcd_down.scale(volumes[-2]/volumes[-1], center=pcd_down.get_center())
        #     obb = pcd.get_oriented_bounding_box()
        #     obb.color = (0, 1, 0)
        #     volume=obb.volume()
        #     volumes.pop()
        #     volumes.append(volume)
        #     print(volumes)
    return pcds_scaled

def display_inlier_outlier(cloud, ind):
    inlier_cloud = cloud.select_by_index(ind)
    outlier_cloud = cloud.select_by_index(ind, invert=True)

    print("Showing outliers (red) and inliers (gray): ")
    outlier_cloud.paint_uniform_color([1, 0, 0])
    inlier_cloud.paint_uniform_color([0.8, 0.8, 0.8])
    o3d.visualization.draw_geometries([inlier_cloud, outlier_cloud],
                                      zoom=0.3412,
                                      front=[0.4257, -0.2125, -0.8795],
                                      lookat=[2.6172, 2.0475, 1.532],
                                      up=[-0.0694, -0.9768, 0.2024])

voxel_size = 0.05
pcds_down = read_point_clouds_from_folder(root_dir,voxel_size)
pcds_scaled=scale_pt_clouds(pcds_down)
o3d.visualization.draw_geometries(pcds_scaled,
                                  zoom=0.3412,
                                  front=[0.4257, -0.2125, -0.8795],
                                  lookat=[2.6172, 2.0475, 1.532],
                                  up=[-0.0694, -0.9768, 0.2024])
                  # total_pcd.extend(pcd)
                 # total_pcd.append(o3d.io.read_point_cloud(pmvs_files[-1]))
                 # try:
                 #     aabb = pcd.get_axis_aligned_bounding_box()
                 #     aabb.color = (1, 0, 0)
                 #     obb = pcd.get_oriented_bounding_box()
                 #     obb.color = (0, 1, 0)
                 #     total_pcd.extend([aabb,obb])
                 # except:
                 #     continue
                 # o3d.visualization.draw_geometries([pcd, aabb, obb],
                                      # zoom=0.7,
                                      # front=[0.5439, -0.2333, -0.8060],
                                      # lookat=[2.4615, 2.1331, 1.338],
                                      # up=[-0.1781, -0.9708, 0.1608])

def pairwise_registration(source, target):
    print("Apply point-to-plane ICP")
    icp_coarse = o3d.pipelines.registration.registration_icp(source, target, max_correspondence_distance_coarse, np.identity(4),
o3d.pipelines.registration.TransformationEstimationPointToPlane())
    icp_fine = o3d.pipelines.registration.registration_icp(source, target, max_correspondence_distance_fine,
        icp_coarse.transformation,
        o3d.pipelines.registration.TransformationEstimationPointToPlane())
    transformation_icp = icp_fine.transformation
    information_icp = o3d.pipelines.registration.get_information_matrix_from_point_clouds(
        source, target, max_correspondence_distance_fine,
        icp_fine.transformation)
    return transformation_icp, information_icp


def full_registration(pcds, max_correspondence_distance_coarse,
                      max_correspondence_distance_fine):
    pose_graph = o3d.pipelines.registration.PoseGraph()
    odometry = np.identity(4)
    pose_graph.nodes.append(o3d.pipelines.registration.PoseGraphNode(odometry))
    n_pcds = len(pcds)
    for source_id in range(n_pcds):
        for target_id in range(source_id + 1, n_pcds):
            transformation_icp, information_icp = pairwise_registration(
                pcds[source_id], pcds[target_id])
            print("Build o3d.pipelines.registration.PoseGraph")
            if target_id == source_id + 1:  # odometry case
                odometry = np.dot(transformation_icp, odometry)
                pose_graph.nodes.append(
                    o3d.pipelines.registration.PoseGraphNode(
                        np.linalg.inv(odometry)))
                pose_graph.edges.append(
                    o3d.pipelines.registration.PoseGraphEdge(source_id,
                                                             target_id,
                                                             transformation_icp,
                                                             information_icp,
                                                             uncertain=False))
            else:  # loop closure case
                pose_graph.edges.append(
                    o3d.pipelines.registration.PoseGraphEdge(source_id,
                                                             target_id,
                                                             transformation_icp,
                                                             information_icp,
                                                             uncertain=True))
    return pose_graph

print("Full registration ...")
max_correspondence_distance_coarse = voxel_size * 25
max_correspondence_distance_fine = voxel_size * 1.5
with o3d.utility.VerbosityContextManager(o3d.utility.VerbosityLevel.Debug) as cm:
    pose_graph = full_registration(pcds_scaled,
                                   max_correspondence_distance_coarse,
                                   max_correspondence_distance_fine)
    
print("Optimizing PoseGraph ...")
option = o3d.pipelines.registration.GlobalOptimizationOption(
    max_correspondence_distance=max_correspondence_distance_fine,
    edge_prune_threshold=0.25,
    reference_node=0)
with o3d.utility.VerbosityContextManager(
        o3d.utility.VerbosityLevel.Debug) as cm:
    o3d.pipelines.registration.global_optimization(
        pose_graph,
        o3d.pipelines.registration.GlobalOptimizationLevenbergMarquardt(),
        o3d.pipelines.registration.GlobalOptimizationConvergenceCriteria(),
        option)
    
print("Transform points and display")
for point_id in range(len(pcds_scaled)):
    print(pose_graph.nodes[point_id].pose)
    pcds_scaled[point_id].transform(pose_graph.nodes[point_id].pose)
o3d.visualization.draw_geometries(pcds_scaled,
                                  zoom=0.3412,
                                  front=[0.4257, -0.2125, -0.8795],
                                  lookat=[2.6172, 2.0475, 1.532],
                                  up=[-0.0694, -0.9768, 0.2024])


pcd_combined = o3d.geometry.PointCloud()
for point_id in range(len(pcds_scaled)):
    # pcds_scaled[point_id].transform(pose_graph.nodes[point_id].pose)
    o3d.io.write_point_cloud(ply_dir+str(point_id)+".ply", pcds_scaled[point_id])
    pcd_combined += pcds_scaled[point_id]
pcd_combined_down = pcd_combined.voxel_down_sample(voxel_size=voxel_size)
o3d.io.write_point_cloud(ply_dir+"multiway_registration.ply", pcd_combined_down)
o3d.visualization.draw_geometries([pcd_combined_down],
                                      zoom=0.3412,
                                  front=[0.4257, -0.2125, -0.8795],
                                  lookat=[2.6172, 2.0475, 1.532],
                                  up=[-0.0694, -0.9768, 0.2024])

print("Statistical oulier removal")
cl, ind = pcd_combined_down.remove_statistical_outlier(nb_neighbors=20,
                                                    std_ratio=2.0)
display_inlier_outlier(pcd_combined_down, ind)
o3d.io.write_point_cloud(ply_dir+"multiway_registration_no_outlier.ply", cl)
# aabb = pcd.get_axis_aligned_bounding_box()
# aabb.color = (1, 0, 0)
# obb = pcd.get_oriented_bounding_box()
# obb.color = (0, 1, 0)
# o3d.visualization.draw_geometries([pcd, aabb, obb],
#                                   zoom=0.7,
#                                   front=[0.5439, -0.2333, -0.8060],
#                                   lookat=[2.4615, 2.1331, 1.338],
#                                   up=[-0.1781, -0.9708, 0.1608])
