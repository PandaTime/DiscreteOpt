#!/usr/bin/python
# -*- coding: utf-8 -*-
import time
from collections import namedtuple
Item = namedtuple("Item", ['index', 'value', 'weight', 'cost'])

def solve_it(input_data):
    start_time = time.clock()
    
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')

    firstLine = lines[0].split()
    item_count = int(firstLine[0])
    capacity = int(firstLine[1])
    count = 0
    items = []
    Array = []
    for i in range(1, item_count+1):
        line = lines[i]
        parts = line.split()
        items.append(Item(i-1, int(parts[0]), int(parts[1]), float(float(parts[0]) / float(parts[1]))))

    # a trivial greedy algorithm for filling the knapsack
    # it takes items in-order until the knapsack is full
    value = 0
    weight = 0
    taken = [0]*len(items)
    lowest = None
    weight_array_prev = []
    #finding lowest item.weight
    for item in items:
        if (item.weight < lowest) or lowest is None:
            lowest = item.weight
            
    lowest -= 1
    #starting progress
    for item in items:
        weight_array = []
        XOR = []
        #loop for weight brackets
        for i in range(lowest, capacity + 1):
        #condition for the first item
            
            if item.index == 0:                
                if item.weight <= i:
                    weight_array.append(item.value)
                    
                else:
                    weight_array.append(int(0))
                weight_array_prev.append(int(0))
            #Array.append(weight_array) - at the very end
                        
            else:                
                if item.weight <= i:
                    #so that we don't have problem with minus position in array (below 0)
                    if i - item.weight < lowest:
                        
                        if item.value > weight_array_prev[i - lowest]:                            
                            weight_array.append(item.value)
                        else:
                            weight_array.append(weight_array_prev[i - lowest])
                    else:
                        if item.value + weight_array_prev[i - item.weight - lowest] >= weight_array_prev[i - lowest]:
                            weight_array.append(item.value + weight_array_prev[i - item.weight - lowest])
                        else:
                            weight_array.append(weight_array_prev[i - lowest])
                else:
                    weight_array.append(weight_array_prev[i - lowest])        
        
        count = 0
        for item in weight_array:
            if item != weight_array_prev[count]:
                XOR.append(int(1))
            else:
                XOR.append(int(0))
            count +=1
        Array.append(XOR)
        weight_array_prev = weight_array
        
        
        
    LookUpWeight = capacity - lowest
    
    for i in range(len(Array) - 1, -1, -1):        
        if Array[i][LookUpWeight] == 1:
            taken.pop(i)
            taken.insert(i,1)
            LookUpWeight -= items[i].weight
            if LookUpWeight <= 0:
                LookUpWeight = 0            
            value +=items[i].value
            
    print time.clock() - start_time, "seconds"     
    
    # prepare the solution in the specified output format
    output_data = str(value) + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, taken))
    return output_data

import os
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
        #print 'This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/ks_4_0)'

