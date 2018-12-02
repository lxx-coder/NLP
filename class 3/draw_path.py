# coding=utf-8

import csv
import networkx as nx
import pandas
import matplotlib.pyplot as plt


def search_destiantion(graph, start, destination):
    pathes = [[start]]
    seen = set()
    chosen_pathes = []
    while pathes:
        path = pathes.pop(0)
        frontier = path[-1]
        if frontier in seen: continue
        if frontier not in graph.keys(): continue
        for city in graph[frontier]:
            new_path = path + [city]
            pathes.append(new_path)
            if city == destination: return new_path

        seen.add(frontier)
    return chosen_pathes

station = {}
with open("E:/test.csv", "r") as csvFile:
    stations = csv.reader(csvFile)
    for s in stations:
#         print(s)
        if not s:continue
        station[s[0]] = s[1:]
        print("{}:{}".format(s[0],station[s[0]]))

cities = list(station.keys())
city_graph = nx.Graph()
city_graph.add_nodes_from(cities)
# nx.draw(city_graph,pos=nx.random_layout(city_graph), with_labels=True, node_size=10)
# plt.show()

cities_connection_graph = nx.Graph(station)
nx.draw(cities_connection_graph, pos=nx.random_layout(cities_connection_graph))

# print(city_graph)
search_destiantion(station,'北京站','朝阳门站')