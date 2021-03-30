# -*- coding: utf-8 -*-
"""
Created on Thu Mar  4 14:40:04 2021

@author: sarde
"""
import numpy as np 
import pandas as pd
from collections import defaultdict
# import json, codecs
import os
import matplotlib.pyplot as plt
from pyntcloud import PyntCloud
import argparse 

parser = argparse.ArgumentParser()
parser.add_argument("-root", "--rootdir", default = '', help = "The director containing all the clusters")
parser.add_argument("-csize", "--clustersize", default=20, help = "Cluster size to be assessed")
args = parser.parse_args() 
  
CLUSTER_SIZE=20
root_dir='D:/00_NCSU/00_Resources/00_Datasets/PartTimePSA/ClusteringExp/'
actual_dir = root_dir+str(CLUSTER_SIZE)

class BundleReader: 
    # bundle_files=[]
    
    def __init__(self, CLUSTER_SIZE, actual_dir):
        self.cluster_size=CLUSTER_SIZE 
        self.actual_dir=actual_dir
        self.bundle_files=[]
    def get_bundle_file_paths(self):
        '''
        Get paths of all bundle.out files. The last bundle.out in each dir matters.
    
        Parameters
        ----------
        actual_dir : str/ PATH
            PATH to read the files from     
        '''
        # bundle_files=[]
        for root, dirs, files in os.walk(self.actual_dir):
            files_in_folder=[]
            for file in files:
                if len(dirs)==0:
                    if file.endswith(".out"):
                         # print(os.path.join(root, file))
                         files_in_folder.append(os.path.join(root, file))
            try:
                self.bundle_files.append(files_in_folder[-1])
            except:
                continue

    def read_bundle_out(self, bundle_file):
        '''
        Read Bundle out file. 
    
        Parameters
        ----------
        bundle_file : (str/ os.PATH)
            FILE PATH for bundle.out to read
        Returns
        -------
        cam : dict
            dictionary of cam poses for images in the cluster.
        points : dict
            dict of points in that cluster. 
    
        '''
        fp = open(bundle_file, "r")
        fp.readline()
        cam_n,pts = tuple(map(int,fp.readline().strip().split()))
        file_contents = fp.readlines()
        fp.close()
        bundle_list=[]
        for line in file_contents:
            bundle_list+=list(map(float,line.strip().split()))
        del file_contents
        cam=defaultdict(list)
        points=defaultdict(list)
        idx=0
        # while bundle_list:
        for i in range(cam_n):
            cam['f'].append(bundle_list[idx])
            idx+=1
            cam['k1'].append(bundle_list[idx])
            idx+=1
            cam['k2'].append(bundle_list[idx])
            idx+=1
            r=[[],[],[]]
            for j in range(3):
                for k in range(3):
                    r[j].append(bundle_list[idx])
                    idx+=1
            # r=np.array(r)
            cam['R'].append(r)
            
            t = []
            for j in range(3):
                t.append(bundle_list[idx])
                idx+=1
            # t=np.array(t)
            cam['t'].append(t)
            
        for i in range(pts):
            pos=[]
            for j in range(3): 
                pos.append(bundle_list[idx])
                idx+=1
            # pos=np.array(pos)
            points['pos'].append(pos)
            
            col=[]
            for j in range(3): 
                col.append(bundle_list[idx])
                idx+=1
            # col=np.array(col)
            points['col'].append(col)
            length_views=bundle_list[idx]
            idx+=1
            views=[]
            for j in range(int(length_views)):
                cam_idx=bundle_list[idx]
                idx+=1
                key=bundle_list[idx]
                idx+=1
                x=bundle_list[idx]
                idx+=1
                y=bundle_list[idx]
                idx+=1
                views.append([cam_idx,key,x,y])
            # views=np.array(views)
            points['views'].append(views)
        return cam, points
        # with open('cam-data-2-20.json', 'w') as fp: 
        #     json.dump(cam, fp)
            
        # with open('point-data-2-20.json', 'w') as fp: 
        #     json.dump(points, fp)
    def read_pose_and_clustered_clouds(self):
        '''
        Read pose estimation and clustered cloud data
        Open bundle files and read the data into lists. 
    
        Parameters
        ----------
        bundle_files : list
            list of bundle_files
    
        Returns
        -------
        cam_poses : list
            list of dicts for cam poses
        pt_cld_clusters : list 
            list of dicts for clusters 
    
        '''
        cam_poses=[]
        pt_cld_clusters=[]
        for file in self.bundle_files:
            pos, pt = self.read_bundle_out(file)
            if len(pos['R'])==CLUSTER_SIZE:
                cam_poses.append(pos)
                pt_cld_clusters.append(pt)
        return cam_poses, pt_cld_clusters

def reject_outliers_2d(points, col, m=2.25):
    '''
    Reject outliers outside 2.25 std deviations of the z axis value of point 
    cloud. Statistical outlier filtering.
    Parameters
    ----------
    points : np array
        point cloud data (n x 3)
    col : np array
        color of cloud data (n x 3).
    m : int, optional
        DESCRIPTION. std dev The default is 2.25.

    Returns
    -------
    np array
        points inliers
    np array
        colors inliers

    '''
    z_pts=points[:,2]
    inliers=abs(z_pts- np.mean(z_pts)) < m * np.std(z_pts)
    return points[inliers],col[inliers]

def get_cam_centers_look_vectors(cam_poses):
    '''
    Get camera centers using R'.T formula and look vectors using Rt.[0 0 1]
    Parameters
    ----------
    cam_poses : list
        list of dicts.

    Returns
    -------
    cam_centers : np array
        camera center coordinates.
    cam_look_vectors : np array
        camera look vectors.

    '''
    ct=0
    cam_centers=[[] for i in range(len(cam_poses))]
    cam_look_vectors=[[] for i in range(len(cam_poses))]
    for i,pose in enumerate(cam_poses): 
        for j in range(len(pose['R'])):
            c=-np.dot(np.array(pose['R'][j]).T,pose['t'][j])
            ct+=1
            # print(ct,c,end='\n')
            cam_centers[i].append(c)
            cam_look_vectors[i].append(np.dot(np.array(pose['R'][j]).T,\
                                            np.array([0,0,1])))
    
    cam_centers=np.array(cam_centers)
    cam_look_vectors=np.array(cam_look_vectors)
    return cam_centers, cam_look_vectors

def get_min_max_bounds_for_clusters(pt_cld_clusters):
    '''
    Return minimum and max bounds for all dimensions per cluster. 

    Parameters
    ----------
    pt_cld_clusters : list
        list of dicts 

    Returns
    -------
    minimums : np array
        minimum bounds
    maximums : np array
        max bounds 

    '''
    minimums=[]
    maximums=[]
    # modes=[]
    total_cld=np.array(pt_cld_clusters[0]['pos'])
    total_cld_col=np.array(pt_cld_clusters[0]['col'])
    for i,pt_cld in enumerate(pt_cld_clusters):
        points = np.array(pt_cld['pos'])
        col = np.array(pt_cld['col'])
        points_filt, col_filt =reject_outliers_2d(points,col)
        minimums.append(np.amin(points_filt, axis=0))
        # modes.append(plt.hist(total_cld[:,2])[1][np.argmax(plt.hist(total_cld[:,2])[0])])
        maximums.append(np.amax(points_filt, axis=0))
        # if i>=1:
        #     total_cld=np.vstack((total_cld, points))
        #     total_cld_col=np.vstack((total_cld_col, col))
    
    minimums=np.array(minimums)
    # modes=np.array(modes)
    maximums=np.array(maximums)
    return minimums, maximums, total_cld, total_cld_col

def save_point_cloud(filename,total_cld, total_cld_col, center_data):
    '''
    save point cloud data to file. 
    Parameters
    ----------
    filename : str/ PATH
        path to save cloud
    total_cld : np array
        position of point array
    total_cld_col : np array
        color of point array
    center_data : np array
        cam center data

    Returns
    -------
    None.

    '''
    # os.touch(filename+'.ply')
    df=pd.DataFrame(
        # same arguments that you are passing to visualize_pcl
        data=np.vstack((np.hstack((total_cld, total_cld_col)),\
                        np.hstack((center_data,np.ones(np.shape(center_data))*255)))),
        columns=["x", "y", "z", "red", "green", "blue"])
    df[['red','green','blue']] = df[['red','green','blue']].astype(np.uint8)
    cloud = PyntCloud(df)
    cloud.to_file(root_dir+filename+".ply")

def closest_to_red(colors, thresh=6):
    '''
    Used to segment points with color closest to color of ball. 
    Parameters
    ----------
    colors : np array
        np array of colors of point cloud 

    Returns
    -------
    index_of_smallest : list
        indices of positions whose euclidean distance is less than certain 
        threshold 10 
    thresh : int
        Default is 10
    '''
    color=np.array([155,15,15])
    distances = np.sqrt(np.sum((colors-color)**2,axis=1))
    index_of_smallest = np.where(distances<=np.amin(distances)+thresh)
    return index_of_smallest


def calc_extent_and_scale(pt_cld_clusters, cam_centers):
    '''
    Calculate scale of each point cloud and xy extent 

    Parameters
    ----------
    pt_cld_clusters : list of dicts 
        list of pt cld clusters dict 
    cam_centers : np array
        center positions 

    Returns
    -------
    cam_to_ground_distances : min(pt_cld)-cam_center
        calculated around xy vicinity 
    delta_x : list
        change in x around center point (const for cluster).
    delta_y : list 
        change in y around center point (const for cluster).
    ball_points_clst : np array 
        points with color close to ball
    ball_maxs : np array
        list of max values for ball 
    ball_mins : np array
        list of max values for ball

    '''
    cam_to_ground_distances=[]
    delta_x=[]
    delta_y=[]

    ball_points_clst=[]
    ball_mins=[]
    ball_maxs=[]

    for cl_no in range(cam_centers.shape[0]):
        for im_no in range(cam_centers.shape[1]):
            ctr=cam_centers[cl_no,im_no,:]
            pt_cld=pt_cld_clusters[cl_no]
            try:
                ctr_nxt=cam_centers[cl_no+1, im_no+1,:]
            except:
                ctr_nxt=ctr_nxt
            points = np.array(pt_cld['pos'])
            col = np.array(pt_cld['col'])
            points_filt, col_filt =reject_outliers_2d(points,col)
    
            idx=(points_filt[:,0]-ctr[0])**2+(points_filt[:,1]-ctr[1])**2<\
                ((points_filt[:,0]-ctr_nxt[0])**2+(points_filt[:,0]-ctr_nxt[0])**2)/2
            points_vicinity=points_filt[idx]
            mins = np.amin(points_filt, axis=0)
            maxs= np.amax(points_filt, axis=0)
            delta_x.append(maxs[0]-mins[0])
            delta_y.append(maxs[1]-mins[1])
            cam_to_ground_distances.append(ctr[2]-mins[2])

        ball_indices=closest_to_red(col_filt)
        if ball_indices[0].shape[0]>50:
            ball_points=points_filt[ball_indices]
            ball_col=col_filt[ball_indices]
            ball_points_clst.append([cl_no,ball_points,ball_col])
            ball_mins.append(np.amin(ball_points,axis=0))
            ball_maxs.append(np.amax(ball_points,axis=0))
    return cam_to_ground_distances, delta_x, delta_y, ball_points_clst, \
        ball_maxs, ball_mins

def scale_clustered_clouds(pt_cld_clusters, scale_per_cluster):
    '''
    Generate total point cloud based on scales 

    Parameters
    ----------
    pt_cld_clusters : TYPE
        DESCRIPTION.
    scale_per_cluster : TYPE
        DESCRIPTION.

    Returns
    -------
    total_cld : TYPE
        DESCRIPTION.
    total_cld_col : TYPE
        DESCRIPTION.

    '''
    scaled_cld_clusters=pt_cld_clusters.copy()
    total_cld=np.array(pt_cld_clusters[0]['pos'])
    total_cld_col=np.array(pt_cld_clusters[0]['col'])
    for i in range(len(pt_cld_clusters)):
        points = np.array(pt_cld_clusters[i]['pos'])/scale_per_cluster[i]
        scaled_cld_clusters[i]['pos']=points
        col = np.array(pt_cld_clusters[i]['col'])
        points_filt, col_filt =reject_outliers_2d(points,col)
        if i>=1:
            total_cld=np.vstack((total_cld, points_filt))
            total_cld_col=np.vstack((total_cld_col, col_filt))
    return total_cld, total_cld_col, scaled_cld_clusters

def offset_points(cam_to_ground_distances, pt_cld_clusters):
    '''
    Generate offseted clusters 

    Parameters
    ----------
    cam_to_ground_distances : TYPE
        DESCRIPTION.
    pt_cld_clusters : TYPE
        DESCRIPTION.

    Returns
    -------
    total_cld : TYPE
        DESCRIPTION.
    total_cld_col : TYPE
        DESCRIPTION.
    offset_cld_clusters : TYPE
        DESCRIPTION.

    '''
    i=0
    cls_no=0
    offset_cld_clusters=pt_cld_clusters.copy()
    total_cld=np.array(pt_cld_clusters[0]['pos'])
    total_cld_col=np.array(pt_cld_clusters[0]['col'])
    while cls_no<len(cam_to_ground_distances)/CLUSTER_SIZE:
        while i<len(cam_to_ground_distances):
            points = np.array(pt_cld_clusters[cls_no]['pos'])
            col = np.array(pt_cld_clusters[cls_no]['col'])
            # points_filt, col_filt =reject_outliers_2d(points,col)
            points_filt, col_filt=points, col
            if cls_no>0:
                offset=cam_to_ground_distances[i]-\
                    cam_to_ground_distances[i-int(np.floor(CLUSTER_SIZE/3))]
                points_filt-=[0,0,offset]
                offset_cld_clusters[cls_no]['pos']=points_filt
                
                total_cld=np.vstack((total_cld, points_filt))
                total_cld_col=np.vstack((total_cld_col, col_filt))
            cls_no+=1
            i+=CLUSTER_SIZE
    return total_cld, total_cld_col, offset_cld_clusters
        

def plot_clusterwise_max_min(minimums, maximums):
    '''
    Plot min and max per cluster. for xyz 

    Parameters
    ----------
    minimums : np array
        min of xyz coords per cluster
    maximums : np array
        maxs of xyz coords per cluster
    Returns
    -------
    None.

    '''
    plt.figure()
    cls_nums=np.linspace(1,minimums.shape[0],minimums.shape[0])
    plt.plot(cls_nums, minimums[:,0], label='minx')
    plt.plot(cls_nums, minimums[:,1], label='miny')
    plt.plot(cls_nums, minimums[:,2], label='minz')
    cls_nums=np.linspace(1,minimums.shape[0],minimums.shape[0])
    plt.plot(cls_nums, maximums[:,0], label='maxx')
    plt.plot(cls_nums, maximums[:,1], label='maxy')
    plt.plot(cls_nums, maximums[:,2], label='maxz')
    plt.legend(loc=3, prop={'size':6})
    plt.title('Variation in x,y,z bounds according to cluster')
    plt.show()
    
def plot_cam_center_data(cam_centers, delta_x, delta_y, cam_to_ground_distances):
    '''
    plot centers and distances from ground and xy deltas 
    
    Parameters
    ----------
    cam_centers : np array
        center data for the center points 
    delta_x : np array
        x coordinate deltas
    delta_y : np array
        y coordinate deltas 
    cam_to_ground_distances : np array 
        distance of cam to ground

    Returns
    -------
    None.

    '''
    plt.figure()
    plt.plot(np.arange(0,cam_centers[:,:,2].reshape(-1,1).shape[0]),\
                    cam_centers[:,:,2].reshape(-1,1), label='z coord')
    plt.plot(np.arange(0,cam_centers[:,:,2].reshape(-1,1).shape[0]),\
                  cam_to_ground_distances, label='cam to ground distance')
    plt.plot(np.arange(0,cam_centers[:,:,2].reshape(-1,1).shape[0]),\
                  delta_x, label='deltax')
    plt.plot(np.arange(0,cam_centers[:,:,2].reshape(-1,1).shape[0]),\
                  delta_y, label='deltay')
    plt.xlabel('frame number')
    plt.ylabel('camera z coordinate')
    plt.title('variation in camera pose (z coordinate) and ground distance and xy delta according to frame')
    plt.legend(loc=3, prop={'size':6})
    plt.show()

def plot_clst_3d_axes(center_data, pt_cld_clusters, CLUSTER_SIZE, cam_look_vectors, cam_centers):
    i=0
    count=0
    clst=0
    while i<center_data.shape[0]:
        while count<=CLUSTER_SIZE:
            # ax = plt.axes(projection='3d')
            if i+CLUSTER_SIZE>center_data.shape[0]:
                xdata = center_data[i:-1,0]
                ydata = center_data[i:-1,1]
                zdata = center_data[i:-1,2]
            else:
                xdata = center_data[i:i+CLUSTER_SIZE,0]
                ydata = center_data[i:i+CLUSTER_SIZE,1]
                zdata = center_data[i:i+CLUSTER_SIZE,2]
            count+=CLUSTER_SIZE
            pt_cld=pt_cld_clusters[clst]
            points = np.array(pt_cld['pos'])
            col = np.array(pt_cld['col'])
            points_filt,col_filt = reject_outliers_2d(points,col)
            data = np.concatenate((xdata[:, np.newaxis], 
                            ydata[:, np.newaxis], 
                            zdata[:, np.newaxis]), 
                          axis=1)
            # Perturb with some Gaussian noise
            data += np.random.normal(size=data.shape) * 0.4
            # Calculate the mean of the points, i.e. the 'center' of the cloud
            datamean = data.mean(axis=0)
            # Do an SVD on the mean-centered data.
            uu, dd, vv = np.linalg.svd(data - datamean)            
            # Now vv[0] contains the first principal component, i.e. the direction
            # vector of the 'best fit' line in the least squares sense.
            # Now generate some points along this best fit line, for plotting.
            linepts = vv[0] * np.mgrid[-7:7:2j][:, np.newaxis]
            
            # shift by the mean to get the line in the right place
            linepts += datamean
            
            
            fig = plt.figure()
            ax = plt.axes(projection='3d')
            # ax.view_init(ax.azim, ax.elev)
            ax.scatter3D(xdata, ydata, zdata, c=zdata, cmap='Greens');
            ax.plot3D(*linepts.T)
            ax.scatter3D(points_filt[:,0], points_filt[:,1], points_filt[:,2], c=points_filt[:,2], cmap='hot');
    
            ax.quiver(xdata,ydata,zdata,cam_look_vectors[:,:,0].reshape(-1,1)[i:i+CLUSTER_SIZE],\
                      cam_look_vectors[:,:,1].reshape(-1,1)[i:i+CLUSTER_SIZE],\
                          cam_look_vectors[:,:,2].reshape(-1,1)[i:i+CLUSTER_SIZE],\
                              length=0.1, normalize=False)
            
            i+=CLUSTER_SIZE
        # try:
        #     for b in range(len(ball_points_clst)):
        #         if ball_points_clst[b][0]==clst:
        #             ax.scatter3D(ball_points_clst[b][1][:,0], ball_points_clst[b][1][:,1], \
        #                   ball_points_clst[b][1][:,2], c=ball_points_clst[b][1][:,2], cmap='Blues')
        #     plt.show()
        # except:
        #     pass
        clst+=1
        count=0



bundle_reader=BundleReader(CLUSTER_SIZE,actual_dir)
print('Fetching Bundle out files')
bundle_reader.get_bundle_file_paths()
print('Reading point clouds')
cam_poses, pt_cld_clusters=bundle_reader.read_pose_and_clustered_clouds()
print('Calculating camera centers')
cam_centers, cam_look_vectors = get_cam_centers_look_vectors(cam_poses)
min_bounds, max_bounds, total_cld, total_cld_col = \
    get_min_max_bounds_for_clusters(pt_cld_clusters)
center_data=cam_centers.reshape(cam_centers.shape[0]*cam_centers.shape[1],\
                                cam_centers.shape[2])
save_point_cloud('original_total_cld', total_cld, total_cld_col, center_data)

print('Calculating Scales')
cam_to_ground_distances, delta_x, delta_y, ball_points_clst, ball_maxs,\
    ball_mins = calc_extent_and_scale(pt_cld_clusters, cam_centers)

# scales_1meter=1/np.array(cam_to_ground_distances)
scale_clst_1 = cam_to_ground_distances[:20]
scales_1_m=[]
for i in range(16): 
    scales_1_m.append(np.divide(cam_to_ground_distances[i*20:(i+1)*20],scale_clst_1))

scale_per_cluster=np.mean(scales_1_m, axis=1) 
print('Scaling and building merged cloud')
total_cld, total_cld_col, scaled_cld_clusters=scale_clustered_clouds(pt_cld_clusters,scale_per_cluster)
save_point_cloud('total_scaled_cld',\
                 total_cld, total_cld_col, center_data)
    
print('Offsetting the clusters.')
total_cld, total_cld_col, offset_clusters=offset_points(cam_to_ground_distances,scaled_cld_clusters)
save_point_cloud('offseted_scaled_clds',\
                 total_cld, total_cld_col, center_data)
    

plot_clusterwise_max_min(min_bounds, max_bounds)
plot_cam_center_data(cam_centers, delta_x, delta_y, cam_to_ground_distances)
#CALC for SCALED Clouds 
min_bounds, max_bounds, _, _ = \
    get_min_max_bounds_for_clusters(scaled_cld_clusters)
cam_to_ground_distances, delta_x, delta_y, ball_points_clst, ball_maxs,\
    ball_mins = calc_extent_and_scale(scaled_cld_clusters, cam_centers)
plot_clusterwise_max_min(min_bounds, max_bounds)
plot_cam_center_data(cam_centers, delta_x, delta_y, cam_to_ground_distances)
# plot_clst_3d_axes(center_data, CLUSTER_SIZE, cam_look_vectors, cam_centers)

#CALC FOR OFFSET
min_bounds, max_bounds, _, _ = \
    get_min_max_bounds_for_clusters(offset_clusters)
cam_to_ground_distances, delta_x, delta_y, ball_points_clst, ball_maxs,\
    ball_mins = calc_extent_and_scale(offset_clusters, cam_centers)
plot_clusterwise_max_min(min_bounds, max_bounds)
plot_cam_center_data(cam_centers, delta_x, delta_y, cam_to_ground_distances)




#SCRATCH


# df=pd.DataFrame(
#         # same arguments that you are passing to visualize_pcl
#         data=np.vstack((np.hstack((total_cld, total_cld_col)),\
#                         np.hstack((center_data,np.ones(np.shape(center_data))*255)))),
#         columns=["x", "y", "z", "red", "green", "blue"])
#     df[['red','green','blue']] = df[['red','green','blue']].astype(np.uint8)


# # #offset
# # i=0
# # j=0
# # center_data_shifted=[]
# # distance_shifted=[]
# # delta_x_shifted=[]
# # delta_y_shifted=[]
# # OVERLAP_SIZE=np.floor(CLUSTER_SIZE/3)
# # while i<(len(cam_to_ground_distances)):
# #     while j<CLUSTER_SIZE:
