import requests
import time
import json
import vk
import numpy as np
import random
import networkx as nx
from IPython.display import Image
import matplotlib.pyplot as plt

group_id = 152573807#input("Input group ID: ")#45627034


def get_id_into_file(name):
    with open(name) as f:
        file_arr = f.read()[:-2].split('};')
        adjacency_list = dict()
        for line in file_arr:
             unit = line.split("{")
             mem = int(unit[0])
             adjacency_list[mem] = []
             flw = [int(x) for x in unit[1].split(",")]
             adjacency_list[mem].extend(flw)
        return adjacency_list

def graph_create(adjacency_list):
    # построение
    G=nx.DiGraph()
    for key in adjacency_list:
        if(len(adjacency_list[key])>0):
            for val in adjacency_list[key]:
                G.add_edge(val,key)
    return G

def group_graf(G):   
    # центральность
    c_degree = nx.pagerank_scipy(G)
    for i in c_degree:
        print('id ' + str(i)+ ' DC ' + str(c_degree[i]))

    # результаты
    final_dict = dict([max(c_degree.items(), key=lambda k_v: k_v[1])])
    print('Maximal centrality element\n {}'.format(final_dict))
    c_degree = list(c_degree.values())
    print('Centrality {}'.format(max(c_degree)))

    #рисование
    pos = nx.spring_layout(G)
    nx.draw(G, cmap = plt.get_cmap('inferno'), node_color = c_degree, node_size=50, pos=pos, with_labels=False, edge_color='r' )
    plt.show()

def cluster_runk(G):
    #рассчет степеней кластеризации
    i=0
    сс_list = list(nx.clustering(G).values())
    сс_degrees = dict()
    #подготовка результирующего словаря
    for nod in G.nodes:
        сс_degrees[nod] = 10**-сс_list[i]
        i+=1
    #рассчет суммы
    list_neighbors = {nod: list (nx.all_neighbors(G,nod)) for nod in G.nodes}
    for key in list_neighbors.keys():
        sum = 0 # cумма внешних степеней сосоедей 
        for nig in list_neighbors[key]:
            sum+=G.out_degree(nig)
        сс_degrees[key] *= sum
    # возрат метрики
    return сс_degrees

def leader_rank(G):
    """
         Node ordering
         :param G: complex network G Graph
         :return: return the node sort value
    """
    # Число узлов в сети
    num_nodes = G.number_of_nodes()
    # Узел
    nodes = G.nodes()
    # Добавить узел g в сеть и присоеденить его ко всем узлам
    G.add_node(0)
    for node in nodes:
        G.add_edge(0, node)
    #инициализация значений LR
    LR = dict.fromkeys(nodes, 1.0)
    LR[0] = 0.0
    #Итерация для удовлетворения условия остановки
    while True:
        tempLR = {}
        for node1 in G.nodes():
            s = 0.0
            for node2 in G.nodes():
                if node2 in G.neighbors(node1):
                    s += 1.0 / G.out_degree([node2])[node2] * LR[node2]
            tempLR[node1] = s
        #Условие завершения: значение LR не меняется
        error = 0.0
        for n in tempLR.keys():
            error += abs(tempLR[n] - LR[n])
        if error == 0.0:
            break
        LR = tempLR
    # Значение LR узла g равномерно распределяется по другим N узлам и узел удаляется
    avg = LR[0] / num_nodes
    LR.pop(0)
    for k in LR.keys():
        LR[k] += avg

    return LR


def main():
    # создаем список смежности (пока пустая)
    adjacency_list = get_id_into_file (str(group_id)+'adj.txt')
    G = graph_create(adjacency_list)
    #cluster_dict = cluster_runk(adjacency_list)
    #работа с графом (по списку смежности)
    #group_graf(adjacency_list)
    #print(cluster_dict)
    lir = leader_rank(G).items()
    print()
    lir = sorted(lir, key=lambda i:i[0])
    print (sorted(leader_rank(G).items(), key=lambda item: item[1]))

main()

