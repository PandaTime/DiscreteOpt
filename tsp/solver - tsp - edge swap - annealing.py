#!/usr/bin/python
# -*- coding: utf-8 -*-

import math
from collections import namedtuple
import os
import time
import random
import copy

Point = namedtuple("Point", ['x', 'y'])

def length(point1, point2):
    return math.sqrt((point1.x - point2.x)**2 + (point1.y - point2.y)**2)

def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')

    nodeCount = int(lines[0])

    points = []
    for i in range(1, nodeCount+1):
        line = lines[i]
        parts = line.split()
        points.append(Point(float(parts[0]), float(parts[1])))

    # build a trivial solution
    # visit the nodes in the order they appear in the file
    #start with random point
    Path_Taken = []
    #first point
    #Temp variables
    Temp = 1
    Min_Temp = 0.1
    delta = 0.9999
    #Optimization
    New = False #Checking if we need to change variables    
    Distance = 0
    Old_Distance = None       
    #Our Loop
    while Temp > Min_Temp:        
        #print Temp
        Left_Points = copy.copy(points)
        Distance = 0
        Path_Taken = []
        Started = False
        #Selectin 2 random edges
        First_Random_Edge = random.randint(0, nodeCount - 1)
        #Selecting previous node to create edge
        if First_Random_Edge == 0:
            Pre_First_Random_Edge = nodeCount - 1
        else:
            Pre_First_Random_Edge = First_Random_Edge - 1
        #Selecting second random Edge
        while True:
            Second_Random_Edge = random.randint(0, nodeCount - 1)
            if Second_Random_Edge != First_Random_Edge or Second_Random_Edge != First_Random_Edge + 1 or Second_Random_Edge != Pre_First_Random_Edge:
                    break
        #Selecting previous node to create edge
        if Second_Random_Edge == 0:
            Second_Random_Edge_2 = nodeCount - 1
        else:
            Second_Random_Edge_2 = Second_Random_Edge - 1
        
        #Adding first edge
        #saving 1-st random edge:
        First_random_data = Left_Points[First_Random_Edge]
        #saving 2-nd random edge:
        Second_Random_Data = Left_Points[Second_Random_Edge]
        Second_Random_Data_2 = Left_Points[Second_Random_Edge_2]
        #removing 1-st random - 1 node(to start edge, so we start with 1-st random node)
        Path_Taken.append(Left_Points[Pre_First_Random_Edge])
        Left_Points.remove(Left_Points[Pre_First_Random_Edge])
        #Our Loop
        Start_with = Left_Points.index(First_random_data)
        while len(Left_Points) != 1:

            #saving for future use(case we removing it)
            Point_Now = Left_Points[Start_with]
            #so that we don't take it
            Left_Points.remove(Left_Points[Start_with])   
            if Point_Now == Second_Random_Data and First_Taken == False:
                First_Taken = True #so that we don't double count it
                Min_Length = length(Second_Random_Data, Second_Random_Data_2)
                Next_Point = Second_Random_Data_2
                Start_with = Left_Points.index(Second_Random_Data_2)
            elif Point_Now == Second_Random_Data_2 and First_Taken == False:
                First_Taken = True #so that we don't double count it
                Min_Length = length(Second_Random_Data, Second_Random_Data_2)
                Next_Point = Second_Random_Data
                Start_with = Left_Points.index(Second_Random_Data)                
            else:
                Min_Length = None
                for j in range(0, len(Left_Points)):
                    length_to = length(Point_Now, Left_Points[j])                
                    if Min_Length is None or Min_Length > length_to:
                        Min_Length = length_to                
                        Next_Point = Left_Points[j]
                        Start_with = j
                
            Distance += (Min_Length)
            Path_Taken.append(Next_Point)
        #Solutions Comparison
        if Distance < Old_Distance or Old_Distance is None:
            Old_Distance = Distance            
            Old_Path_Taken = copy.copy(Path_Taken)
        #annealing
        else:
            try:
                annealing = 1 / (1 + math.exp((Distance - Old_Distance)/Temp))
            except:
                annealing = 0
        Temp *= delta
    
    #Getting our Solution
    solution = []
    
    for i in range(0, len(Old_Path_Taken)):
        if Old_Path_Taken[i] in points:
            solution.append(points.index(Old_Path_Taken[i]))
    #solution = range(0, nodeCount)
    
    # calculate the length of the tour
    obj = length(points[solution[-1]], points[solution[0]])
    for index in range(0, nodeCount-1):
        obj += length(points[solution[index]], points[solution[index+1]])

    # prepare the solution in the specified output format
    output_data = str(obj) + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, solution))

    return output_data


import sys

if __name__ == '__main__':
    if len(sys.argv) > 1:        
        file_location = sys.argv[1].strip()
        start_time = time.clock()
        input_data_file = open(file_location, 'r')
        input_data = ''.join(input_data_file.readlines())
        input_data_file.close()
        print solve_it(input_data)
        print time.clock() - start_time, "seconds"
    else:
        file_location = os.getcwd() + "\\data\\" + raw_input("Enter file name: ")
        start_time = time.clock()
        input_data_file = open(file_location, 'r')
        input_data = ''.join(input_data_file.readlines())
        input_data_file.close()
        print solve_it(input_data)
        print time.clock() - start_time, "seconds"
        #print 'This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/tsp_51_1)'

