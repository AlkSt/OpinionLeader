from math import floor, sqrt
import math
import networkx as nx
from networkx.algorithms.centrality.degree_alg import degree_centrality
from numpy import copy
from numpy.lib.function_base import append
import create_graph
import random
import numpy as np
# from sklearn.cluster import AgglomerativeClustering
from sklearn.cluster import KMeans



def dist(u,v,W):
    X = W[u][0] - W[v][0]
    Y = W[u][1] - W[v][2]
    Z = W[u][2] - W[v][2]
    Q = W[u][3] - W[v][3]
    return sqrt(X**2+Y**2+Z**2+Q**2)

def clusterring(G):
    node_list = list(G.nodes())
    N = len(node_list)
    ind = nx.in_degree_centrality(G)
    btw = nx.betweenness_centrality(G)
    clc = nx.clustering(G) #{node: (1/N)*(G.out_degree(node)/ind[node]) for node in node_list}
    center = { node: ind[node]*btw[node]/clc[node] if clc[node]>0 else 1 for node in node_list}
    parameters = {node:(ind[node],btw[node],clc[node],center[node]) for node in node_list}
    cluster = dict()
    K=5
    seed = [0 for i in range(K)]
    D = { i: 0.0 for i in node_list}
    seed[0] = random.choice(node_list)
    sums =0 
    for i in range(K-1):
        for nodej in node_list: 
            D[nodej] = dist(nodej, seed[i],parameters)
            sums+=D[nodej]
        rand = sums*0.3
        for nodej in node_list: 
            rand -= D[nodej]
            print(rand)
            if ((rand) <= 0):
                seed[i + 1] = nodej
                break
        
    
    prev = dict()
    
    while True:
        cluster = { i: [seed[i]] for i in range(K)}
        for node in node_list:
            if not (node in seed):
                dis = [dist(node,seed[i],parameters) for i in range(K)]
                item = dis.index(min(dis))
                cluster[item].append(node) 
        
        for i in range(K):
            modul = len(cluster[i]) 
            w1 = sum([ind[node] for node in cluster[i]])/modul 
            w2 = sum([btw[node] for node in cluster[i]])/modul 
            w3 = sum([clc[node] for node in cluster[i]])/modul 
            w4 = sum([center[node] for node in cluster[i]])*modul
            w4 -= floor(w4) #frac
            print( parameters[seed[i]][0] - w1,parameters[seed[i]][1] -w2,parameters[seed[i]][2] -w3,parameters[seed[i]][3] -w4 )
            parameters[seed[i]] = [w1,w2,w3,w4]

        print()
        #print(cluster)# можно и значения сравнивать
        if prev == cluster: break
        else: prev = cluster

    centers = [ max(center[j]) for j in cluster[i] for i in range(K)]
    res = max(centers)
    print (res)
    return res


def cluster_runk(lock, lst, G):
    #рассчет степеней кластеризации
    i=0
    cluster_list = list(nx.clustering(G).values())
    cluster_deg = dict()
    #подготовка результирующего словаря
    for nod in G.nodes:
        cluster_deg[nod] = 10**-cluster_list[i]
        i+=1
    #рассчет суммы
    list_neighbors = {nod: [nodes for nodes in G.predecessors(nod)] for nod in G.nodes} #list(nx.all_neighbors(G,nod)) 
    # list_neighbors = {nod:list(nx.all_neighbors(G,nod)) for nod in G.nodes}
    for key in list_neighbors.keys():
        sum = 0 # cумма внешних степеней сосоедей 
        for nig in list_neighbors[key]:
            sum+=G.in_degree(nig)
        cluster_deg[key] *= sum
    # возрат метрики
    res = sorted(cluster_deg.items(), key=lambda item: item[1],reverse= True)
    # with lock:
    #     lst.put(dict(res))
    return dict(res)

def degree_centralitys(lock, lst, G):

    norm = 1.0 / (len(G) - 1.0)
    centrality = dict()
    for node, deg in G.out_degree(): 
        centrality[node] = deg * norm
     
    res = sorted(centrality.items(), key=lambda item: item[1],reverse= True)
    # with lock:
    #     lst.put(dict(res))
    return dict(res)


def leader_rank(lock, lst, G):
    i = 0
    # Число узлов в сети
    num_nodes = G.number_of_nodes()
    # Узел
    nodes = G.nodes()
    # Добавить узел g в сеть и присоеденить его ко всем узлам
    G.add_node(0)
    for node in nodes:
        G.add_edge(node, 0)
        G.add_edge(0, node)
    #инициализация значений LR
    LR = dict.fromkeys(nodes, 1.0)
    LR[0] = 0.0
    #Итерация для удовлетворения условия остановки
    total_LR = []
    while i< 100:
        total_LR.append(sorted(LR.items(), key=lambda item: item[1],reverse= True))
        i+=1
        tempLR = {}
        for node1 in G.nodes():
            s = 0.0
            for node2 in G.predecessors(node1):
                deg = 1.0 /G.in_degree(node2) if G.in_degree(node2)>0 else 0
                s += deg * LR[node2]
            tempLR[node1] = s
        
        for tlr in total_LR:
            if tlr == sorted(tempLR.items(), key=lambda item: item[1],reverse= True): 
                print()
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
    res = sorted(LR.items(), key=lambda item: item[1],reverse= True)
    print(i)
    # with lock:
        # lst.put(dict(res))
    return dict(res)


def clusters(G):
    n = len(G.nodes())
    pcc_longueurs=list(nx.all_pairs_shortest_path_length(G))
    distances=np.zeros((n,n))
    # distances[i, j] is the length of the shortest path between i and j
    
    node_list = list(G.nodes())
    for i in range(n):
        for j in range(n):
            try: distances[i,j] = pcc_longueurs[i][1][node_list[j]]
            except: distances[i,j] = 0
    clustering = KMeans(n_clusters=4).fit_predict(distances) #,linkage='average',affinity='precomputed'
    data_cluster = {clustering[i]: [] for i in range(n)}
    for i in range(n):
        data_cluster[clustering[i]].append(node_list[i])

    return data_cluster

def stars_rank(lock, lst, G):
    data_cluster = clusters(G)
    c_degree = {} #nx.out_degree_centrality(G)
    max_in = max(dict(G.in_degree()).values())
    rkin = {node: math.log(G.in_degree(node)+1)/math.log(max_in+1) for node in G.nodes()}

    for cluster in data_cluster:
        for nodei in data_cluster[cluster]:
            sumi = sumj = 0
            c_degree[nodei] = rkin[nodei]
            for nodej in G.predecessors(nodei): # for nodej in node_list:
                if nodej in data_cluster[cluster]: sumi+=rkin[nodej]
                else: sumj += rkin[nodej]
            if sumi!=0: c_degree[nodei] *=(sumi/(sumi+sumj))
            else: c_degree[nodei] *=0


    res = sorted(c_degree.items(), key=lambda item: item[1],reverse= True)
    # with lock:
    #     lst.put(dict(res))
    return dict(res)



def get_analitic_res(lock, lst, G):
    for item in [degree_centralitys, cluster_runk, stars_rank, leader_rank]:
        res = item(G)
        with lock:
            lst.put(res)


    
def main():
    # G = create_graph.get_graph("108366262adj.txt")
    # res = stars_rank(G)
    G = create_graph.get_graph("152573807adj.txt")
    res = degree_centralitys(G)

if __name__ == "__main__":
    main()