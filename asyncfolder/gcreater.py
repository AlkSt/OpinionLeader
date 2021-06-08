import networkx as nx
from IPython.display import Image
import matplotlib.pyplot as plt


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
    # for node in G:
    #     if G.out_degree([node])[node] ==0:
    #         G.remove_nodes_from()

    return G

def group_graf(G):   
    # центральность
    c_degree = nx.degree_centrality(G)
    # for i in c_degree:
    #     print('id ' + str(i)+ ' DC ' + str(c_degree[i]))

    # результаты
    final_dict = dict([max(c_degree.items(), key=lambda k_v: k_v[1])])
    # print('Maximal centrality element\n {}'.format(final_dict))
    c_degree = list(c_degree.values())
    # print('Centrality {}'.format(max(c_degree)))

    #рисование
    pos = nx.spring_layout(G, k = 0.3)
    nx.draw_networkx_nodes(G, pos=pos,  node_color = c_degree, node_size=25, cmap = plt.get_cmap('coolwarm'))
    nx.draw_networkx_edges (G, pos = pos, edge_color='gray', alpha = 0.2 )
    plt.axis('off')
    #nx.draw(G, cmap = plt.get_cmap('inferno'), node_color = c_degree, node_size=50, pos=pos, with_labels=False, edge_color='r' )
    #plt.show()
    fig = plt.gcf()  # get the figure to show
    #fig.show()
    return fig


def load(file_name):
    adj_list = get_id_into_file(file_name)
    G = graph_create(adj_list)
    return group_graf(G)

def get_graph(file_name):
    adj_list = get_id_into_file(file_name)
    return graph_create(adj_list)

def main():
    fig = load("24243817adj1.txt")    
    

if __name__ == "__main__":
    main()