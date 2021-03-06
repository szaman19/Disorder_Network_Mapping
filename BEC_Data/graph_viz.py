import networkx as nx 
import matplotlib as mp
import matplotlib.pyplot as plt 
import sys
from multiprocessing import pool as Pool
from matplotlib.pyplot import figure
#figure(num=None,figsize=(3.5,3.5),dpi=200,facecolor='w',edgecolor='k')

def generate_graph(file_name, reciprocal = True):
    data = open(file_name)
    
    graphs = []
    labels = []
    condensates = []
    #graph = nx.DiGraph()
    #label = ''
    #condensate = ''
    max_val = 0
    max_vals=[]

    for line in data:
        #Clean up the data to get the numerical values
        data_points = line.strip().split()
        data_points = " ".join(data_points).split()
        if (data_points[0] == 'For'):
            graph = nx.Graph()
            label = str(data_points[2])
            condensate = str(data_points[4])
            graphs.append(graph)
            labels.append(label)
            condensates.append(condensate)

            if (max_val != 0):
                max_vals.append(max_val)
            max_val=0
        else:

        #data_points currently hold [from_site_index, to_site_index, correlation_val]
            site_i = int(data_points[0])
            site_j = int(data_points[1])
            
            corr = float(data_points[2])
        #Regular division is not helpful in this situation. Make sure to not add when i = j, because corr == inf

            if(site_i != site_j):
            #print(site_i, site_j, corr)
                if reciprocal:
                    corr = 1 / corr
                if (corr > max_val):
                    max_val = corr
                
                graph.add_edge(site_i,site_j, weight = corr)

    max_vals.append(max_val)
    #adj_matrix = nx.adjacency_matrix(graph)
    #print(np.matrix(adj_matrix))
    return graphs, labels, condensates, max_vals

def graph_visualize(graph,label, cond, max_val,order):
    fig = plt.figure(num=order,figsize=(3.5,2.8),dpi=200,facecolor='w',edgecolor='k')
    plt.rcParams["axes.labelweight"] = "bold"
    plt.rcParams["font.family"] = "serif"
    plt.rcParams["font.serif"]="Times New Roman"

    layout = nx.layout.circular_layout(graph)
    plt.gcf().subplots_adjust(left=0, bottom=0.05,right=.97,top=.97)
    M = graph.number_of_edges()
    edge_colors = range(2,M+2)
    e = graph.edges()
    # print(max_val)

    

    # edge_alphas = [(graph[u][v]['weight']/max_val) for u,v in e]

    #print(edge_alphas)
    
    nodes = nx.draw_networkx_nodes(graph,layout,node_size=20,node_color='blue')

    # edges = nx.draw_networkx_edges(graph,layout,arrows=True,node_size=20,edge_cmap=plt.cm.Blues,width=1,arrowsize=2,arrowstyle='->',edge_color=edge_colors)

    nodes = nx.draw_networkx_nodes(graph,layout,node_size=10,node_color='black')
    for u,v in e:
        nx.draw_networkx_edges(graph,layout,edgelist=[(u,v)],width=graph[u][v]['weight']/5)
    #ax.set_rasterize(True)
    label = str(label).replace(".","d")
    cond = str(cond).replace(".","d")
    fig.savefig("BEC_Graph_beta="+label[:3]+"condensate="+cond[:2]+".svg",format='svg')
    fig.savefig("BEC_Graph_beta="+label[:3]+"condensate="+cond[:2]+".png",format='png')
def cc(graph, beta, condensate):
    adjacency_matrix = nx.to_numpy_array(graph)
    c_c = 0
    val = 0
    #print(adjacency_matrix.shape[0])
    for i in range(adjacency_matrix.shape[0]):
        W = 0
        for j in range(adjacency_matrix.shape[0]):
            for k in range(adjacency_matrix.shape[0]):
                if (i != j and i != k and k != j):
                    W += adjacency_matrix[j][k]
        val += W
    c_c = val / (51 * 50 * 49)
    #print ("B="+str(beta)+" C=" + str(condensate)," \t", c_c)
    return beta,c_c
def avg_path(graph,beta,condensate):
    avg = nx.average_shortest_path_length(graph, weight='weight')
    return beta, avg

def file_reader(file_name):
    reader = open(file_name, 'r')

    for line in reader:
        print(line)
def main():
    if (len(sys.argv) < 2):
        print("Needs file name")
    else:
        file_name = sys.argv[1]
        graphs, betas, condensates, max_vals = generate_graph(file_name, reciprocal=True)

        #pool = Pool.Pool(processes=len(graphs))
        #results = [pool.apply_async(cc, args=(graphs[i],betas[i],condensates[i])) for i in range(len(graphs))]
        #output = [p.get() for p in results]

        pool = Pool.Pool(processes=len(graphs))
        avg_p = [pool.apply_async(graph_visualize, args=(graphs[i],betas[i],condensates[i],max_vals[i],i+1)) for i in range(len(graphs))]
        avg_p_results = [p.get() for p in avg_p]
        #print(output)
        #file_name = open('average_shortest_path_length.dat', 'w')
        #for beta,clustering in avg_p_results:
        #    line = "L="+str(beta) + '\t' + 'C=' + str(clustering) +'\n'
        ##    file_name.write(line)
        #    print (line)
main()
