import matplotlib.pyplot as plt 
import graph_util 
import networkx as nx
import matplotlib as mp
import os 
from multiprocessing import pool as Pool
from matplotlib.pyplot import figure

# figure(num=None,figsize=(3.5,3),dpi=200,facecolor='w',edgecolor='k')

CWD = os.getcwd()
FILE_DIR = CWD + '/500_Diffusion_data/'
def visualizer(file_name, order):
	font = {
	'fontname':'Times New Roman',
	'color':'black',
	'weight':'normal',
	'size':14
	}
	plt.rcParams["axes.labelweight"] = "bold"
	plt.rcParams["font.family"] = "serif"
	plt.rcParams["font.serif"]="Times New Roman"
	file_name = FILE_DIR + file_name
	fig = plt.figure(num=order,figsize=(3.5,2.8),dpi=200,facecolor='w',edgecolor='k')
	plt.gcf().subplots_adjust(left=0, bottom=0.05,right=.97,top=.97)
	graph, label = graph_util.di_generate_graph(file_name, reciprocal=False)
	lab = label
	label = label.replace(".","-")
	layout = nx.layout.circular_layout(graph)
	print("graph generated")
	M = graph.number_of_edges()
	max_val=1
	edge_colors = range(2,M+2)
	e = graph.edges()
	edge_alphas = [(graph[u][v]['weight']/max_val) for u,v in e]

	nodes = nx.draw_networkx_nodes(graph,layout,node_size=10,node_color='black')
	for u,v in e:
		nx.draw_networkx_edges(graph,layout,edgelist=[(u,v)],width=graph[u][v]['weight']/5)
		# print("Nodes 1: ", u,"\t Node 2: ",v, "\t" , graph[u][v]['weight'] )

	# nodes = nx.draw_networkx_nodes(graph,layout,node_size=10,node_color='black')
	# edges = nx.draw_networkx_edges(graph,layout,arrows=True,node_size=2,edge_cmap=plt.cm.Greys,width=.3,arrowsize=.1,arrowstyle='->',edge_color=edge_colors)
	# for i in range(M):
	#     edges[i].set_alpha(edge_alphas[i])
	# pc = mp.collections.PatchCollection(edges,cmap=plt.cm.Greys)
	# pc.set_array([e for e in edge_alphas])

	# fig.colorbar(pc)
	ax = fig.gca()
	ax.set_axis_off()
	ax.text(-0.25,-1.25,"(W="+lab+")", fontdict=font)
	#nx.draw_circular(graph, **options)
	# plt.tight_layout()
	plt.show()
    # label = label.replace(".","-")
	# plt.savefig("25-W-"+label+".svg",format='svg')
	# plt.savefig('25-W-'+label+".png",format='png')

def main():
	file_name = 'w-0-E-0-diffusion-500.txt'
	file_name2 = 'w-1-5-E-0-diffusion-500.txt'
	# visualizer(file_name,0)
	# visualizer(file_name2,1)
	pool = Pool.Pool(processes=2)
	p1 = pool.apply_async(visualizer, args=(file_name,1, ))
	p2 = pool.apply_async(visualizer, args=(file_name2,2, ))
	p1.get()
	p2.get()
main()
