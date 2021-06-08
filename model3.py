import create_graph
import network_analitic
import random
import matplotlib.pyplot as plt

CONST_IN = 150
COEF_Z = 0.95

def summ(adj, nodes):
    sums = 0
    for item in adj:
        sums+=nodes[item][0][1]
    return sums

def node_state(node):
    max_p = max(max(node[0][0], node[0][1]),node[0][2])
    return list(node[0]).index(max_p)



# def SIR_model(adj_list, leaders_ranks, G, count = 200):
    
#     t = [i for i in range(count)]
#     Ft = [0 for i in range(count)]
#     rpt = 0 
#     step = 50
#     while rpt < step:
#         rpt+=1
#         I = CONST_IN
#         S = len(leaders_ranks)-I
#         R = 0
#         beta = COEF_Z
#         #gama = # число связей?
#         nodes = dict()
#         i=0
#         for item in leaders_ranks.keys():
#             state = [0, 1, 0] if i<I else [1, 0, 0]
#             gama = (1 - 1 /G.in_degree(item)) if G.in_degree(item)!=0 else 0 
#             # len(adj_list[item]) // if item in adj_list.keys() else 0 
#             try:
#                 nodes[item] = [state, gama]
#             except:
#                 print(item, "eiofn ")
#             i+=1

#         i=0
#         s_set_len = S
#         i_set =  [node  for node in list(nodes.items()) if node[1][0][1]== 1 ]
#         while i<count and len(i_set)>0: 
#             i+=1
#             some_el_i = random.choice(i_set) 
#             if not (some_el_i[0] in adj_list):
#                  Ft[i-1]=Ft[i-2] 
#                  continue
#             # if not (G.in_degree(some_el_i[0])!=0): continue              
#             some_fol = random.choice(adj_list[some_el_i[0]])
#             # p = [node for node in G.nbunch_iter(some_el_i[0])]
#             # some_fol = random.choice(p)
#             some_el_x = some_el_i[1][0][1]

#             prev_state = node_state(nodes[some_fol])

#             # if (node_state(some_el_i[1])==1 and prev_state==2 and some_fol in adj_list 
#             # and some_el_i[0] in adj_list[some_fol]):
#             #     some_el_x = nodes[some_fol][0][1] #node i x
#             #     some_fol = some_el_i[0] #node j = node i 
#             #     prev_state = node_state(nodes[some_fol])
#             #     print(2110)
                
#             dsi = 0
#             if (some_fol in adj_list): a=0
#             if (G.in_degree(some_fol)!=0):
#                 dsi = -beta*nodes[some_fol][0][0]*some_el_x
#             dri = nodes[some_fol][1]*nodes[some_fol][0][1]
#             dxi = -dsi-dri
#             nodes[some_fol][0][0]+=dsi
#             nodes[some_fol][0][1]+=dxi
#             nodes[some_fol][0][2]+=dri
#             new_state = node_state(nodes[some_fol])
#             if(prev_state == 1 and new_state !=1 ):
#                 i_set.remove((some_fol,nodes[some_fol]))
#             if(prev_state != 1 and new_state ==1 ):
#                 s_set_len-=1
#                 i_set.append((some_fol,nodes[some_fol]))
#             # print(node_state(some_el_i[1]), prev_state, new_state, s_set_len)
            
#             Ft[i-1]  += (len(leaders_ranks)- s_set_len)/step
#             # print(Ft[i-1])
            
#             # i+=1
#             # print(i)

#     return t,Ft


def dif_SIR_model(adj_list, leaders_ranks, G, infected,count = 200):
    
    t = [i for i in range(count)]
    Ft = [0 for i in range(count)]
    rpt = 0 
    step = 10
    while rpt < step:
        rpt+=1
        I = len(infected)
        S = len(leaders_ranks)-I
        R = 0
        beta = COEF_Z
        #gama = # число связей?
        nodes = dict()
        i=0
        for item in leaders_ranks.keys():
            state = [0, 1, 0] if item in infected else [1, 0, 0]
            gama = (1 - 1 /G.in_degree(item)) if G.in_degree(item)!=0 else 0 
# len(adj_list[item]) // if item in adj_list.keys() else 0 
            try:
                nodes[item] = [state, gama]
            except:
                print(item, "eiofn ")
            i+=1

        i=0
        s_set_len = S
        i_set =  [node  for node in list(nodes.items()) if node[1][0][1]== 1 ]
        while i<count and len(i_set)>0: 
            i+=1
            some_el_i = random.choice(i_set) 
            if not (some_el_i[0] in adj_list):
                 Ft[i-1]=Ft[i-2] 
                 continue
            # if not (G.in_degree(some_el_i[0])!=0): continue              
            some_fol = random.choice(adj_list[some_el_i[0]])
            # p = [node for node in G.nbunch_iter(some_el_i[0])]
            # some_fol = random.choice(p)
            some_el_x = some_el_i[1][0][1]

            prev_state = node_state(nodes[some_fol])
            if (node_state(some_el_i[1])==1 and prev_state==2 and some_fol in adj_list 
            and some_el_i[0] in adj_list[some_fol] and random.random() > 0.5):
            
                some_el_x = nodes[some_fol][0][1] #node i x
                some_fol = some_el_i[0] #node j = node i 
                prev_state = node_state(nodes[some_fol])
                print(2110)
                
            dsi = 0
            if (some_fol in adj_list): a=0
            if (G.in_degree(some_fol)!=0):
                dsi = -beta*nodes[some_fol][0][0]*some_el_x
            dri = nodes[some_fol][1]*nodes[some_fol][0][1]
            dxi = -dsi-dri
            nodes[some_fol][0][0]+=dsi
            nodes[some_fol][0][1]+=dxi
            nodes[some_fol][0][2]+=dri
            new_state = node_state(nodes[some_fol])
            if(prev_state == 1 and new_state !=1 ):
                i_set.remove((some_fol,nodes[some_fol]))
            if(prev_state != 1 and new_state ==1 ):
                s_set_len-=1
                i_set.append((some_fol,nodes[some_fol]))
            # print(node_state(some_el_i[1]), prev_state, new_state, s_set_len)
            
            Ft[i-1]  += (len(leaders_ranks)- s_set_len)/step
            # print(Ft[i-1])
            
            # i+=1
            # print(i)

    return t,Ft



def show_plt(t,Ft=[],Fh=[],Fs=[],Fr=[]):        
    if len(Ft)>0: plt.plot(t, Ft, color="blue",alpha = 0.4 )
    if len(Fh)>0: plt.plot(t, Fh, color="green", alpha = 0.6)    
    if len(Fs)>0: plt.plot(t, Fs, color="orange",  alpha = 0.7)
    if len(Fr)>0: plt.plot(t, Fr, color="maroon",  alpha = 0.8)
    plt.xlabel("Time")
    plt.ylabel("F(t)")
    plt.grid(True)
    plt.axis('on')
    # plt.show()
    fig = plt.gcf()  # get the figure to show
    # fig.show()
    return fig
    


# def get_modeling_experiment(dc, pr, lr, cr, sr, count, name):
#     adj_list = create_graph.get_id_into_file(name)
#     G = create_graph.graph_create(adj_list)
#     Ft = []
#     Fs = []
#     Fg = []
#     Fh = []
#     Fr = []
#     if len(dc)>0:
#         (t, Ft) = SIR_model(adj_list, dc, G, count)
#     if len(pr)>0:
#         (t, Fg) = SIR_model(adj_list, pr, G, count)
#     if len(lr)>0:
#         (t, Fh) = SIR_model(adj_list, lr, G, count)
#     if len(cr)>0:
#         (t, Fs) = SIR_model(adj_list, cr, G, count)
#     if len(sr)>0:
#         (t, Fr) = SIR_model(adj_list, sr, G, count)
#     return show_plt(t,Ft,Fg,Fh,Fs,Fr)

def get_modeling_experiment(dc, lr, cr, sr, count, name):
    adj_list = create_graph.get_id_into_file(name)
    G = create_graph.graph_create(adj_list)
    id_values = []
    all = [dict(dc), dict(lr), dict(cr), dict(sr)]
    for i in range(len(all)):
        id_values.append([el[0] for el in list(all[i].items())[:CONST_IN]])
    # Ft = [], Fs = [], Fg = [], Fh = [], Fr = []
    
    all = [dc, lr, cr, sr]
    res_y = [[] for _ in range(len(all))]
    for i in range(len(all)):
        if len(all[i])>0:
            (t, res_y[i]) = dif_SIR_model(adj_list, all[i], G, id_values[i], count)

    return show_plt(t,res_y[0],res_y[1],res_y[2],res_y[3])


def dif_modeling_experiment(dc, lr, cr, sr, count, name):
    adj_list = create_graph.get_id_into_file(name)
    G = create_graph.graph_create(adj_list)
    id_values = different(dc, lr, cr, sr)
    # Ft = [], Fs = [], Fg = [], Fh = [], Fr = []
    
    all = [dc, lr, cr, sr]
    res_y = [[] for _ in range(len(all))]
    for i in range(len(all)):
        if len(all[i])>0:
            (t, res_y[i]) = dif_SIR_model(adj_list, all[i], G, id_values[i], count)

    return show_plt(t,res_y[0],res_y[1],res_y[2],res_y[3])

def different(dc, lr, cr, sr):
    all = [dict(dc), dict(lr), dict(cr), dict(sr)]
    pair = []
    index = []
    N = len(all)
    for i in range(N):
        pair.append([el[0] for el in list(all[i].items())[:CONST_IN]])
        index.extend(pair[i])
    print()

    num =0
    for i in all:
        if len(i)>0: num+=1

    for i in index:
        if index.count(i) > num-1:
            for d in pair:
                if i in d:  
                    d.remove(i)

    return pair
                 




def main():
    adj_list = create_graph.get_id_into_file("187235639adj.txt")
    G = create_graph.graph_create(adj_list)
    ranks = network_analitic.degree_centralitys(G)
    # ranks1 = network_analitic.page_rank(G)
    # ranks2 = network_analitic.cluster_runk(G)
    # ranks3 = network_analitic.leader_rank(G)

    # (t, Fg) =  SIR_model(adj_list , dict(sorted(ranks.items(), key=lambda item: item[1])), G)
    # (t, Ft) = SIR_model( adj_list, ranks, G)

    # (t,Fg) = SIR_model(adj_list, ranks1, G)
    # (t,Fh) = SIR_model(adj_list, ranks2, G)
    # (t, Fs) = SIR_model(adj_list, ranks3, G)

    # fig = show_plt(t,Ft,Fg)
    # fig.show()



if __name__ == "__main__":
    main()