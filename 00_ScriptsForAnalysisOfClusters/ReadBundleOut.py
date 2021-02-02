import numpy as np 
import pandas as pd
from collections import defaultdict
# import json, codecs
import os
import matplotlib.pyplot as plt
from pyntcloud import PyntCloud

def read_bundle_out(bundle_file):
    # fp = open(root+'bundle_020.out', "r")
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
    
def reject_outliers_2d(data, m=2):
    col=data[2,:]
    return data[:,abs(col - np.mean(col)) < m * np.std(col)]

root_dir='D:/00_NCSU/00_Resources/00_Datasets/PartTimePSA/ClusteringExp/20'
bundle_files=[]
for root, dirs, files in os.walk(root_dir):
    for file in files:
        if file.endswith("020.out"):
             print(os.path.join(root, file))
             bundle_files.append(os.path.join(root, file))

cam_poses=[]
pt_cld_clusters=[]
for file in bundle_files:
    pos, pt = read_bundle_out(file)
    cam_poses.append(pos)
    pt_cld_clusters.append(pt)

minimums=[]
maximums=[]
modes=[]
total_cld=np.array(pt_cld_clusters[0]['pos'])
total_cld_col=np.array(pt_cld_clusters[0]['col'])
for i,pt_cld in enumerate(pt_cld_clusters):
    points = np.array(pt_cld['pos'])
    # points_filt = reject_outliers_2d(points)
    points_filt=points
    col = np.array(pt_cld['col'])
    # col_filt = reject_outliers_2d(col)
    col_filt=col
    # print(points.shape)
    # print(np.amin(points_filt, axis=0))
    minimums.append(np.amin(points_filt, axis=0))
    modes.append(plt.hist(total_cld[:,2])[1][np.argmax(plt.hist(total_cld[:,2])[0])])
    maximums.append(np.amax(points_filt, axis=0))
    # print(f'Volume and XY area of bounding box for cluster {i}', \
    #   (maximums[-1][0]-minimums[-1][0])* (maximums[-1][1]-minimums[-1][1])\
    #       *(maximums[-1][2]-minimums[-1][2]),((maximums[-1][0]-minimums[-1][0])* \
    #       (maximums[-1][1]-minimums[-1][1])*(maximums[-1][2]-minimums[-1][2]))\
    #       /(maximums[-1][2]-minimums[-1][2]))
        
    
    if i>=1:
    #     # print([minimums[0][2]])
    #     print('min before offset')
    #     print(np.amin(points_filt, axis=0))
    #     # points_filt=points_filt-np.array([0,0,minimums[0][2]])
    #     points_filt=points_filt-np.array([0,0,modes[0]])
    #     print('min after offset')
    #     print(np.amin(points_filt, axis=0))
        total_cld=np.vstack((total_cld, points))
        total_cld_col=np.vstack((total_cld_col, col))
minimums=np.array(minimums)
modes=np.array(modes)
maximums=np.array(maximums)

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


plt.figure()
cls_nums=np.linspace(1,len(bundle_files),len(bundle_files))
plt.plot(cls_nums, minimums[:,0], label='minx')
plt.plot(cls_nums, minimums[:,1], label='miny')
plt.plot(cls_nums, minimums[:,2], label='minz')
# plt.legend()
# plt.show()
# plt.figure()
cls_nums=np.linspace(1,len(bundle_files),len(bundle_files))
plt.plot(cls_nums, maximums[:,0], label='maxx')
plt.plot(cls_nums, maximums[:,1], label='maxy')
plt.plot(cls_nums, maximums[:,2], label='maxz')

plt.plot(cls_nums, modes[:], label='modez')
# plt.plot(cls_nums, modes[:,1], label='modey')
# plt.plot(cls_nums, modes[:,2], label='modez')
plt.legend(loc=3, prop={'size':6})
plt.title('Variation in x,y,z bounds according to cluster')
plt.show()

plt.figure()
plt.plot(cam_centers[:,:,2].reshape(-1,1), label='z coord')
plt.xlabel('frame number')
plt.ylabel('camera z coordinate')
plt.title('variation in camera pose (z coordinate) according to frame')
plt.legend(loc=3, prop={'size':6})
plt.show()

center_data=cam_centers.reshape(cam_centers.shape[0]*cam_centers.shape[1],\
                                cam_centers.shape[2])

df=pd.DataFrame(
    # same arguments that you are passing to visualize_pcl
    data=np.vstack((np.hstack((total_cld, total_cld_col)),\
                   np.hstack((center_data,np.ones(np.shape(center_data))*255)))),
    columns=["x", "y", "z", "red", "green", "blue"])
df[['red','green','blue']] = df[['red','green','blue']].astype(np.uint8)
cloud = PyntCloud(df)





cloud.to_file("offset_cld.ply")
fig = plt.figure()
ax = plt.axes(projection='3d')

xdata = center_data[:,0]
ydata = center_data[:,1]
zdata = center_data[:,2]
ax.scatter3D(xdata, ydata, zdata, c=zdata, cmap='Greens');
ax.scatter3D(points[:,0], points[:,1], points[:,2], c=points[:,2], cmap='Reds');