import numpy as np 
from collections import defaultdict
# import json, codecs
import os
import matplotlib.pyplot as plt

root_dir='D:/00_NCSU/00_Resources/00_Datasets/PartTimePSA/ClusteringExp/20'
bundle_files=[]
for root, dirs, files in os.walk(root_dir):
    for file in files:
        if file.endswith("020.out"):
             print(os.path.join(root, file))
             bundle_files.append(os.path.join(root, file))

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

cam_poses=[]
pt_cld_clusters=[]
for file in bundle_files:
    pos, pt = read_bundle_out(file)
    cam_poses.append(pos)
    pt_cld_clusters.append(pt)

minimums=[]
maximums=[]
for pt_cld in pt_cld_clusters:
    points = np.array(pt_cld['pos'])
    # print(points.shape)
    print(np.amin(points, axis=0))
    minimums.append(np.amin(points, axis=0))
    maximums.append(np.amax(points, axis=0))
minimums=np.array(minimums)
maximums=np.array(maximums)

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
plt.legend()
plt.show()