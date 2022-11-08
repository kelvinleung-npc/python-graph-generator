import matplotlib
# Force matplotlib to not use any Xwindows backend.
matplotlib.use('Agg')
import json
import matplotlib.pyplot as plt
import numpy as np
import os
import sys, getopt
import matplotlib.ticker as ticker
from matplotlib.ticker import MaxNLocator

########################################################
# parses JSON file for hashes of graph input           #
# then outputs them as graphs                          #
########################################################

########################
# Example JSON file    #                 
########################
# {
#     "1":{   
#         "type": "linegraph",
#         "title":"testlinegraph",
#         "label_and_y_value_arrays": [["line1",[1,2,3]],["line2",[7,8,9]]],
#         "x_value_array": ["one","two","three"]
#         },
#     "2":{
#         "type": "bargraph",
#         "title" :"test2",
#         "x_label":"xlabel",
#         "y_label": "ylabel",
#         "y_value_array": [0,1,2,3,4],
#         "x_value_array": ["one","two","three","four","five"]
#         },
#     "3": {
#         "type": "treemap",
#         "title": "treemap",
#         "labels": ["A","B","C","D"],
#         "size_array": [50,30,10,10]
#         }
# }

#################################################################################
# Given a title: string, label_and_y_value_arrays: [[label,[y_array_values]]...]#
# and an x_value_array. generates a line_graph either singular or multiple      #             
#################################################################################
def line_graph(title, label_and_y_value_arrays, x_value_array):
    plt.rcParams["figure.figsize"] = (10,7)
    fig,ax = plt.subplots()
    plt.xticks(rotation=45, ha='right')
    for part in label_and_y_value_arrays:
        label = part[0]
        y_value_array = part[1]
        ax.plot(x_value_array,y_value_array,label = label, linestyle="-")
    if(len(x_value_array) < 11):
        ax.xaxis.set_major_locator(MaxNLocator(len(x_value_array)))    ###############################
    else:                                                              # restricts x ticks to max 11 #
        ax.xaxis.set_major_locator(MaxNLocator(11))                    ###############################
    plt.title(title)
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.6, box.height])
    lgd = plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    fig.savefig(title, bbox_extra_artists=(lgd,), bbox_inches='tight')
    plt.clf() 

def bar_graph(title,x_label,y_label, y_value_array, x_value_array):
    plt.rcParams["figure.figsize"] = (10,7)
    plt.figure()
    plt.bar(x_value_array, y_value_array)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.tight_layout()
    plt.savefig(title)
    plt.clf()

def pie_chart(title,labels,size_array):
    fig1, ax1 = plt.subplots()
    ax1.pie(size_array, labels=labels, autopct='%1.1f%%',
        shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.savefig(title)

argv = sys.argv[1:]
############################################################
#Example running                                           #
#python generalized_graph_generator.py --json="data.json"  #
############################################################
def main(argv): 
    try:
        opts, args = getopt.getopt(argv,"",["json="])
    except Exception:
        print("failed to get arguments")
        
    totaldata = ''
    for (option, value) in opts:
        if option == "--json":
            f = open(value)
            totaldata = json.load(f)
    for graph in totaldata:
        data = totaldata[graph]
        graphtype = data["type"]
        if graphtype == "linegraph":
            line_graph(data["title"], data["label_and_y_value_arrays"], data["x_value_array"])
        elif graphtype == "bargraph":
            bar_graph(data["title"], data["x_label"], data["y_label"], data["y_value_array"], data["x_value_array"])
        elif graphtype == "treemap":
            tree_map(data["title"], data["labels"], data["size_array"])
        elif graphtype == "piechart":
            pie_chart(data["title"], data["labels"], data["size_array"])
main(argv)
