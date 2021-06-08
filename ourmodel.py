import create_graph
import network_analitic
import random
import matplotlib.pyplot as plt

def summ(adj, nodes):
    sums = 0
    for item in adj:
        sums+=nodes[item][0][1]
    return sums

def node_state(node):
    max_p = max(max(node[1][0][0], node[1][0][1]),node[1][0][2])
    return list(node[1][0]).index(max_p)



def SIR_model(adj_list, leaders_ranks, G):
    t = [i for i in range(30)]
    Ft = [0 for i in range(30)]
    rpt = 0 
    while rpt < 50:
        rpt+=1
        I = 20
        S = len(leaders_ranks)-I
        R = 0
        beta = 1.1
        #gama = # число связей?
        nodes = dict()
        i=0
        for item in leaders_ranks.keys():
            state = [0, 1, 0] if i<=I else [1, 0, 0]
            gama = (1 - 1 /len(adj_list[item])) if item in adj_list.keys() else 0 

            try:
                nodes[item] = [state, gama]
            except:
                print(item, "eiofn ")
            i+=1

        i=0
        i_set_len = I
        while i<30 and i_set_len > 0:
            for node in list(nodes.items()):
                prev_state = node_state(node)
                dsi = 0
                if (node[0] in adj_list):
                    dsi = -beta*node[1][0][0]*summ(adj_list[node[0]], nodes)
                dri = node[1][1]*node[1][0][1]
                dxi = -dsi-dri
                node[1][0][0]+=dsi
                node[1][0][1]+=dxi
                node[1][0][2]+=dri
                new_state = node_state(node)
                if(prev_state == 1 and new_state !=1 and node[1][0][2] > 0.8): i_set_len-=1
                if(prev_state != 1 and new_state ==1 ): i_set_len+=1


            if i%1==0:
                Ft[i]  += (len(nodes)-i_set_len/len(nodes))/50
                print(Ft[i])
            
            i+=1

    return t,Ft

def show_plt(t,Ft,Fg):        
    plt.plot(t, Ft, color="orange")
    plt.plot(t, Fg, color="blue",alpha = 0.3)
    plt.xlabel("Time")
    plt.ylabel("F(t)")
    plt.grid(True)
    plt.show()




def main():
    adj_list = create_graph.get_id_into_file("24243817adj1.txt")
    G = create_graph.graph_create(adj_list)
    ranks = network_analitic.degree_centralitys(G)
    ranks1 = network_analitic.page_rank(G)
    (t, Ft) = SIR_model( adj_list, ranks, G)
    # (t, Fg) =  SIR_model(adj_list , dict(sorted(ranks.items(), key=lambda item: item[1])), G)
    (t,Fg) = SIR_model(adj_list, ranks1, G)
    show_plt(t,Ft,Fg)



if __name__ == "__main__":
    main()