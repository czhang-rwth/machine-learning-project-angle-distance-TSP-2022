from typing import List
import ast
from math import acos
import sympy
import os
import numpy as np

def distance(node1: List, node2: List) -> float:
    return ((node1[0]-node2[0])**2 + (node1[1]-node2[1])**2)**0.5

def angle(node1: List, node2: List, node3: List, unit:str) -> float: #node1 -> node2 -> node3 angle between 12 and 23 
    pi = 3.1415926
    vector12 = [node2[0]-node1[0], node2[1]-node1[1]]
    vector23 = [node3[0]-node2[0], node3[1]-node2[1]]
    vector_product = vector12[0]*vector23[0] + vector12[1]*vector23[1]
    len_product = distance(node1, node2) * distance(node2, node3)
    if len_product != 0:
        cos = vector_product / len_product
        if unit == 'degree':
            return (acos(round(cos, 15)) / pi) * 180
        elif unit == 'radiant':
            return acos(round(cos, 15))
        else:
            return np.nan
    else:
        return 0

def obj_distance_angle(path_nodes: str, path_obj: str) -> float:
    data = open(path_nodes)
    
    nodes = {}
    
    for line in data:
        if len(line.split(' ')) != 1:
            node = int(line.split(' ')[0])
            x = int(line.split(' ')[1])
            y = int(line.split(' ')[2])
            nodes[node] = [x, y]
        else:
            continue

    obj_data = open(path_obj)

    for line in obj_data:
        if line.find('Tour') > -1:
            tour = ast.literal_eval(line.split(': ')[1])
        if line.find('Obj') > -1:
            obj = float(line.split(': ')[1])
            
    obj_distance = 0
    obj_angle = 0

    for i in range(1, len(tour)):
        obj_distance += distance(nodes[tour[i-1]], nodes[tour[i]])
    obj_distance += distance(nodes[tour[-1]], nodes[tour[0]])

    for i in range(2, len(tour)):
        obj_angle += angle(nodes[tour[i-2]], nodes[tour[i-1]], nodes[tour[i]], 'radiant')
    obj_angle += angle(nodes[tour[-2]], nodes[tour[-1]], nodes[tour[0]], 'radiant') + angle(nodes[tour[-1]], nodes[tour[0]], nodes[tour[1]], 'radiant')

    return obj_distance, obj_angle, obj

path_nodes_1 = "E:\OR_Coding\machine learning\dataset_AngleDistanceTSP\dataset_AngleDistanceTSP\Data_Class2\Instances_C2\inst_5001.txt"
path_obj_1 = 'E:\OR_Coding\machine learning\dataset_AngleDistanceTSP\dataset_AngleDistanceTSP\Data_Class2\Optimal_solutions_C2\inst_5001_sol.txt'

path_nodes_2 = "E:\OR_Coding\machine learning\dataset_AngleDistanceTSP\dataset_AngleDistanceTSP\Data_Class2\Instances_C2\inst_5002.txt"
path_obj_2 = 'E:\OR_Coding\machine learning\dataset_AngleDistanceTSP\dataset_AngleDistanceTSP\Data_Class2\Optimal_solutions_C2\inst_5002_sol.txt'

coe1 = obj_distance_angle(path_nodes_1, path_obj_1)
coe2 = obj_distance_angle(path_nodes_2, path_obj_2)
print(coe1)
print(coe2)

x,y = sympy.symbols("x y")
ans = sympy.solve([coe1[0]*x + coe1[1]*y - coe1[2], coe2[0]*x + coe2[1]*y - coe2[2]],[x,y])
print(ans)

instances = 'E:\OR_Coding\machine learning\dataset_AngleDistanceTSP\dataset_AngleDistanceTSP\Data_Class2\Instances_C2'
solutions = 'E:\OR_Coding\machine learning\dataset_AngleDistanceTSP\dataset_AngleDistanceTSP\Data_Class2\Optimal_solutions_C2'

files_nodes = os.listdir(instances)
files_nodes.sort(key=lambda x:int(x[5:-4]))

files_obj = os.listdir(solutions)
files_obj.sort(key=lambda x:int(x[5:-8]))

for i in range(len(files_nodes)):
    coe = obj_distance_angle(instances+'\\'+files_nodes[i], solutions+'\\'+files_obj[i])
    if coe[2]- (coe[0]*ans[x] + coe[1]*ans[y]) < 0.001:
        print(f'{files_nodes[i]}: {ans[x]} * sum_distance + {ans[y]} * sum_angle == obj')
    else:
        print('error')
        break