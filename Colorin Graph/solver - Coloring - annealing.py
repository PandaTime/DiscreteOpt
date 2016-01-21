#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
from collections import OrderedDict
import random
import time
import copy
import math


def solve_it(input_data):
    start_time = time.clock()
    # Modify this code to run your optimization algorithm
    #solution = {}
    # parse the input
    lines = input_data.split('\n')
    dic = {}
    first_line = lines[0].split()
    node_count = int(first_line[0])
    edge_count = int(first_line[1])
    #restrictions table
    #None for k in range(100) 
    restrictions = [[] for j in range(node_count + 1)]    
    edges = []
    for i in range(1, edge_count + 1):
        line = lines[i]
        parts = line.split()
        edges.append((int(parts[0]), int(parts[1])))

    # build a trivial solution

    #Range Nodes depending on number of Edges
    dicRanges = {}
    count = 1
    #restrictions_general array - which nodes shouldn't be equal
    restrictions_general = [[] for j in range(node_count)]
    #forming dictionary with number or Edges in Nodes so we can rank them
    #depending on number of Edges
    for i in range(1, edge_count + 1):
        #print i
        line = lines[i]        
        part = line.split()
        nextpart = lines[i+1].split()
        restrictions_general[int(part[0])].append(int(part[1]))
        restrictions_general[int(part[1])].append(int(part[0]))
        #because of the last line
        try:
            if part[0] != nextpart[0]:                
                key = int(part[0])                
                dicRanges[key] = count
                count = 1
            else:               
                count +=1
            
        except:            
            key = int(part[0])
            dicRanges[key] = count
            count = 0
    
    #same but for collumn 2
    count = 1    
    for i in range(1, edge_count + 1):
        #print i
        
        line = lines[i]        
        part = line.split()
        prevpart = lines[i+1].split()
        
        try:
            if part[1] != prevpart[1]:            
                key = int(part[1])
                try:
                    dicRanges[key] += count
                except:
                    dicRanges[key] = count
                count = 1
            else:               
                count +=1
            
        except:            
            key = int(part[1])
            dicRanges[key] = count
            count = 0
    
    #getting restrictions lists
        
    #print dicRanges
    sortedArray = list(sorted(dicRanges, key = dicRanges.get, reverse=True))
    #sorting in random way to get better value(in theory)
    node_count1 = None
    Temperature = 1
    delta = 0.999999
    Minimum_Temp = 0.1
    New = False
    prev_colors = None
    prev_solution = []
    prev_restrictions = []
    prev_sortedArray = []
    dic ={}
    restrictions = [[] for j in range(node_count)]
    
    while Temperature > Minimum_Temp:
        #print Temperature
        if Temperature != 1:
            #saving prev data
            if New == True:                
                prev_solution = copy.copy(dic)
                prev_restrictions = copy.copy(restrictions)
                prev_colors = colors
                prev_sortedArray = copy.copy(sortedArray)
            #changing elements
            first_number = random.randint(0, node_count - 1)
            #so first not equals second number
            while True:
                second_number = random.randint(0, node_count - 1)
                if second_number != first_number:
                    break
            temp = int(sortedArray[first_number])
            sortedArray[first_number] = int(sortedArray[second_number])
            sortedArray[second_number] = temp
            dic = {}
            restrictions = [[] for j in range(node_count)]
            
                        
        else:
            start_number = 0

        #Looking for color        
        for lop in range(0, len(sortedArray)):
            keys = sortedArray[lop] 
            keys = int(keys)
            try:
                dic[keys]                
            except:
                #assigning color number                              
                for i in range(0,len(restrictions[keys]) + 1): 
                    try:
                        restrictions[int(keys)]
                        #print restrictions[keys]
                        if not i in restrictions[keys]:                                
                            dic[keys] = i
                            break
                        elif i == len(restrictions[keys]) - 1:
                            dic[keys] = i + 1                    
                    except:                        
                        dic[keys] = i
                        break
            #incerting restrictions from restrictions_general(value to nodes)
            restrict = int(dic[keys])
            for data in restrictions_general[keys]:
                restrictions[data].append(restrict)
        for i in range(1, node_count + 1):            
            if not i-1 in dic:
                # [i - 1] because we're checking all the nodes
                if not restrictions[i-1]:
                    dic[i-1] = 0                  
                else:              
                    for j in range(0,len(restrictions[i - 1])):
                        try:                      
                            if not j in restrictions[i-1][j]:                                
                                dic[i-1] = j                                                       
                                break
                            if j == len(restrictions[i-1]) - 1:
                                dic[i-1] = j + 1  
                        except:                            
                            dic[i-1] = j                 
        #comparing results
        randsolution = []
        for data in dic:            
            randsolution.append(dic[data])  
        colors = max(randsolution) + 1        
        if colors < prev_colors or prev_colors is None:
            New = True            
        else:

            annealing = 1 / (1 + math.exp((colors - prev_colors)/Temperature))            
            random_annealing = random.random()
            if annealing > random_annealing:
                New = True
            else:
                dic = copy.copy(prev_solution)
                restrictions = copy.copy(prev_restrictions)
                colors = prev_colors
                sortedArray = copy.copy(prev_sortedArray)
                New = False
        Temperature *= delta
   
    solution = []
    for data in dic:
        solution.append(dic[data])
    # prepare the solution in the specified output format
    output_data = str(colors) + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, solution))
    print time.clock() - start_time, "seconds"  
    return output_data


import sys

if __name__ == '__main__':
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        input_data_file = open(file_location, 'r')
        input_data = ''.join(input_data_file.readlines())
        input_data_file.close()
        print solve_it(input_data)
    else:
        file_location = os.getcwd() + "\\data\\" + raw_input("Enter file name: ")
        input_data_file = open(file_location, 'r')
        input_data = ''.join(input_data_file.readlines())
        input_data_file.close()
        print solve_it(input_data)
        #print 'This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/gc_4_1)'

