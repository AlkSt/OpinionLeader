import create_graph
import network_analitic
import random
import matplotlib.pyplot as plt

def SIR_model(adj_list, leaders_ranks, G):
    rpt = 0 
    while rpt < 50:
        rpt+=1
        t = [i for i in range(300)]
        Ft = [0 for i in range(300)]
        S = 50
        I = len(leaders_ranks)-S
        R = 0
        alpha = 1.2
        nodes = dict()
        i=0
        for item in leaders_ranks.keys():
            state = 'S' if i<=S else 'I'
            try:
                nodes[item] = [state,len(adj_list[item])]
            except:
                print(item, "eiofn ")
            i+=1

        i=0
        s_set_len = 1
        while i<300 and s_set_len > 0:
            s_set =  [node  for node in list(nodes.items()) if node[1][0]=='S' ]
            s_set_len = len(s_set)
            some_el_s = random.choice(s_set)
            some_fol = random.choice(adj_list[some_el_s[0]])
            x = 1/leaders_ranks[some_el_s[0]]
            if not some_fol in nodes:
                continue
            if nodes[some_fol][0] == 'I' :
                p = alpha/ some_el_s[1][1]
                if x > p:
                    nodes[some_fol][0] = 'S'
                    S+=1
                    s_set_len+=1
                    I-=1
            else:
                beta = 1/(G.out_degree(some_el_s[0])+1)
                p = beta/ some_el_s[1][1]
                if x > p:
                    nodes[some_el_s[0]][0] = 'R'
                    S-=1
                    s_set_len-=1
                    R+=1

            if i%5==0:
                Ft[i]  += ((S+R)/len(nodes))/10
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