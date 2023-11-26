
import numpy as np
from RRT.RRT import RRTMain
from RRTStar.RRTStar import RRTStarMain
import parameters
import pickle
import os 
import sys

rrt_star = False

start_pos = (2,30)
end_pos = (40,5)
n_obstacles = 50
window_width = 150
window_height = 150

obstacle_file_name = 'obstacle_file'
rrt_window_width = 650
rrt_window_height = 650
rrt_start_pos = (10,500)
rrt_end_pos = (590,56)
rrt_n_obstacles = 200
obstacle_dim = parameters.OBSTACLE_DIM

def createObstacles():
    obs = set()
    n = 108
    x_coord = np.random.randint(0,window_width,n).tolist()
    y_coord = np.random.randint(0,window_height,n).tolist()

    for i in range(n):
        if( (x_coord[i] == start_pos[0] and y_coord[i] == start_pos[1]) 
              or (x_coord[i] == end_pos[0] and y_coord[i] == end_pos[1])):
            continue

        obs.add((x_coord[i],y_coord[i]))
    return obs 

def createObstacles_RandomSampling():
    
    obs = set()
    x_coord = np.random.randint(0,rrt_window_width-obstacle_dim,rrt_n_obstacles).tolist()
    y_coord = np.random.randint(0,rrt_window_height-obstacle_dim,rrt_n_obstacles).tolist()

    file = open(obstacle_file_name,'ab')   
    for i in range(len(x_coord)):
        if(
            (x_coord[i]>= rrt_start_pos[0] and x_coord[i] <= rrt_start_pos[0] + obstacle_dim) or
            (y_coord[i]>= rrt_start_pos[1] and y_coord[i] <= rrt_start_pos[1] + obstacle_dim) or
            (x_coord[i]>= rrt_end_pos[0] and x_coord[i] <= rrt_end_pos[0] + obstacle_dim) or
            (y_coord[i]>= rrt_end_pos[1] and y_coord[i] <= rrt_end_pos[1] + obstacle_dim) 
            ):
            continue

        obs.add((x_coord[i],y_coord[i]))
    pickle.dump(obs,file)
    file.close()
    return obs

def main(newOb = True):
    obstacles = createObstacles()
    if newOb == True:
        if os.path.exists(obstacle_file_name):
            os.remove(obstacle_file_name)
            print(f"{obstacle_file_name} will be rebuilt.")
        else:
            print(f"{obstacle_file_name} will be built.")


    rrt_obstacles = None
    if os.path.exists(obstacle_file_name):
        picklefile = open(obstacle_file_name, 'rb')     
        rrt_obstacles = pickle.load(picklefile)
        picklefile.close()

    else:
        rrt_obstacles = createObstacles_RandomSampling()
   
    if rrt_star:
        rrtstar = RRTStarMain(rrt_start_pos,rrt_end_pos,rrt_obstacles,obstacle_dim,rrt_window_width,rrt_window_height)
        rrtstar.run()
    else:
        rrt = RRTMain(rrt_window_width,rrt_window_height,rrt_start_pos,rrt_end_pos,rrt_obstacles,len(rrt_obstacles))
        rrt.run()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        newOb_value = sys.argv[1]  
        main(newOb_value)
    else:
        main(True)