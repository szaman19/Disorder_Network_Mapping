from matplotlib import pyplot 
import numpy as np
import scipy 
import networkx as nx
import graph_util
from multiprocessing import process
from multiprocessing import pool as Pool
from threading import Thread
import os

CWD = os.getcwd()
CWD+='/500_Diffusion_data/'

def per_graph_cc(file_name):
    file_name = CWD + file_name
    graph,label = graph_util.generate_graph(file_name,reciprocal=False)
    clustering = graph_cc(graph,label,method="Lopez")
    return clustering, label 

def graph_cc(graph,label,method="Lopez"):
    adjacency_matrix = nx.to_numpy_array(graph)

    #print(adjacency_matrix)
    #G = np.power(adjacency_matrix, 1/3)
    #G_3 = G @ G @ G
    c_c = 0

    if (method == "Barrat"):
        for i in range(adjacency_matrix.shape[0]):
            weights = 0
            sum_kj = 0
            for k in range(adjacency_matrix.shape[0]):
                for j in range(adjacency_matrix.shape[0]):
                    if (i !=k and i != j and k!= j):
                        sum_kj += (adjacency_matrix[i][k] + adjacency_matrix[i][j]) / 2
                weights += adjacency_matrix[i][k]
            c_c += sum_kj / (weights * (499))
        c_c /= 500
    
    elif (method=="Zhang"):
        G = np.power(adjacency_matrix,1)
        G_3 = G @ G @ G

        for i in range(adjacency_matrix.shape[0]):
            denom = 0
            sq = 0 
            for k in range(adjacency_matrix.shape[0]):
                
                denom += adjacency_matrix[i][k]
                sq += adjacency_matrix[i][k]**2

            c_c += G_3[i][i]/(denom  ** 2 - sq)
        
        c_c /= 500
    elif (method == 'new'):
        cube_root = np.power(adjacency_matrix,1/3)
        square_root = np.power(adjacency_matrix,1/2)

        val = 0
        for i in range(adjacency_matrix.shape[0]):
            Del = 0
            W = 0
            for k in range(adjacency_matrix.shape[0]):
                for j in range(adjacency_matrix.shape[0]):
                    if (i != j) and (i != k) and (j != k):
                        temp_del = cube_root[i][j] * cube_root[j][k] * cube_root[k][i]
                        temp_a_mean = (adjacency_matrix[i][j] + adjacency_matrix[j][k] + adjacency_matrix[k][i])**2

                        Del += temp_del * 9  / (temp_a_mean)

                        temp_W = (square_root[i][j] * square_root[k][i])
                        temp_w_mean = (adjacency_matrix[i][j] + adjacency_matrix[k][i])**2
                        W += temp_W * 4 / temp_w_mean
            val += Del / W
        c_c = val / 500    
    elif (method == 'updated'):
        max_nodes = adjacency_matrix.shape[0]
        cube_root = np.power(adjacency_matrix,1/3)
        square_root = np.power(adjacency_matrix,1/2)
        
        val = 0
        for i in range(max_nodes):
            N_i_delta = 0
            N_i_tri = 0

            for j in range(max_nodes):
                for k in range(max_nodes):
                    if ( i != j and i != k and k != j):
                        W = 1 / (cube_root[i][j] * cube_root[i][k] * cube_root[j][k])
                        w = 1 / (square_root[i][j] * square_root[i][k])

                        N_i_delta += W
                        N_i_tri += w
            val += (N_i_delta/N_i_tri)
        c_c = val / 500
    elif (method == 'Lopez'):
        val = 0
        for i in range(adjacency_matrix.shape[0]):
            W = 0
            for j in range(adjacency_matrix.shape[0]):
                for k in range(adjacency_matrix.shape[0]):
                    if (i != j and i != k and k != j):
                        W += adjacency_matrix[j][k]
            val += W
        c_c = val / (500 * 499 * 498)
            


                    

    #to do 
    # Include new clustering coefficient implementation using combination of geometric and arithmetic mean 

    
    print(label," \t",c_c)
    
    return c_c

def main():
    files = ['w-0-E-0-diffusion-500.txt',
            'w-0-1-E-0-diffusion-500.txt',
            'w-0-2-E-0-diffusion-500.txt',
            'w-0-3-E-0-diffusion-500.txt',
            'w-0-4-E-0-diffusion-500.txt',
            'w-0-5-E-0-diffusion-500.txt',
            'w-0-6-E-0-diffusion-500.txt',
            'w-0-7-E-0-diffusion-500.txt',
            'w-0-8-E-0-diffusion-500.txt',
            'w-0-9-E-0-diffusion-500.txt',
            'w-1-0-E-0-diffusion-500.txt',
            'w-1-1-E-0-diffusion-500.txt',
            'w-1-2-E-0-diffusion-500.txt',
            'w-1-3-E-0-diffusion-500.txt',
            'w-1-4-E-0-diffusion-500.txt',
            'w-1-5-E-0-diffusion-500.txt'
            ]
    pool = Pool.Pool(processes=len(files))
    results = [pool.apply_async(per_graph_cc, args=(files[x],)) for x in range(len(files))]
    output = [p.get() for p in results]
    print(output)

    file_output = open("clustering_coefficient_per_disorder.dat",'w')
    for label, clustering in output:
        line = "W="+str(label) + '\t' + 'C=' + str(clustering) +'\n'
        file_output.write(line)
    file_output.close()

main()
