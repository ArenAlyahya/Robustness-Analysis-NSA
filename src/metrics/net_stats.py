import igraph as ig
import numpy as np

from vuln_calculator import GraphMaking





########### LOADING INPUT FILES ##############
#BR flow_matrix and BR unique codes. csv filies
import sys
sys.path.append('../')
from data_files import Input_files

in_files = Input_files('../../') 
f_matrix_original = np.genfromtxt(in_files.get_network_file_name(),delimiter=';')
codes = np.genfromtxt(in_files.get_codes_file_name())
##############################################


relative_path = '../../results/' + in_files.get_project_name() + '/metrics/'




def export_data(codes, data, stat, thresh):
    file_out = open(relative_path +  stat + '_' + str(thresh) + '.csv', 'w')
    
    #save the crospondig codes
    for i in range(len(codes)):
        file_out.write(str(codes[i]) + ';' + str(data[i]) + '\n')
    file_out.close()

    # ordered version
    stat_array = []
    for i in range(len(data)):
        stat_array.append( ( codes[i], float(data[i]) ) )

    #name of the columns 
    dtype = [('label', int), ('stat', float)]

    #convert to an array
    stat_array = np.array(stat_array, dtype=dtype)
    
    #order using the stat value frm the smallest to the largest
    stat_array = np.sort(stat_array, order='stat')
    
    #flip them making the largest first
    stat_array = np.flip(stat_array)
    
    file_stat = open(relative_path + 'ordered_' + stat + '_' + str(thresh) + '.csv', 'w')
    for i in range(len(stat_array)):
        file_stat.write(str(stat_array[i][0]) + ';' + str(stat_array[i][1]) + '\n')
    file_stat.close()

def nth_moment_v2(g,n):
    print("Nodes degrees: ",g.degree())
    degree_np = np.array(list(g.degree()))
    return (sum(degree_np**n)/len(degree_np))
    




print('METRICS:')


N = len(codes)

data = np.genfromtxt('../../results/' + in_files.get_project_name() + '/metrics/avg_std.csv', delimiter=';') 

avg = data[0]
std = data[1]


# 3 thresholds
for thresh in [0, avg, avg+std]:
    print('  thresh=' + str(thresh))
    
    f_matrix = f_matrix_original.copy()


    # Apply threshold
    for row in range(N):
        for col in range(N):
            # anything less than the threshold consider it as 0 flow
            if f_matrix[row][col] < thresh:
                f_matrix[row][col] = 0


    print('   STRENGTH')
    #initialize the strength store for N node with 0
    node_str = np.zeros(N)
    for i in range(N):
        #out degree probably (calculate the STRENGTH for each node )
        node_str[i] = np.sum( f_matrix[i,:] )
    


    print("mean: ",np.mean(node_str))
    print("std: ", np.std(node_str))

    #save the stringth in orderd_strength_thresh.csv

    export_data(codes, node_str, 'strength', thresh)


    
    # Create graph, A.astype(bool).tolist() or (A / A).tolist() can also be used.
    # Generates a graph from its adjacency matrix  --> it seems the matrix is only 0 and 1
    g = ig.Graph.Adjacency( (f_matrix > 0.0).tolist())
    # Counts the number of vertices.
    N = g.vcount()

    # Convert to undirected graph
    g = g.as_undirected()

    #The vertex sequence of the graph
    #I think it names all the vertices 
    g.vs['label'] = codes

    print("Number of nodes", g.vcount())
    print("Number of edges", g.ecount())


    print('   DEGREE')
    degrees = g.degree()


    print("mean: ", np.mean(degrees))
    print("std: ", np.std(degrees))
    print("2th_moment: ", nth_moment_v2(g,2))
    

    export_data(codes, degrees, 'degree', thresh)


    print('   BETWEENNESS')
    #Calculates or estimates the betweenness of vertices in a graph.
    betweenness = g.betweenness(vertices=None, directed=False, cutoff=None)
    
    

    print("mean: ",np.mean(betweenness))
    print("std: ", np.std(betweenness))
    
    export_data(codes, betweenness, 'betweenness', thresh)    
    

    print('   VULNERABILITY')
    # Vulnerability indexes
    grp = GraphMaking(f_matrix)
    grp.create_graph(g)

    grp.vulnerability()

    print("mean", np.mean(grp.vuln))
    print("std", np.std(grp.vuln))

    export_data(codes, grp.vuln, 'vuln', thresh)
	

    '''
    # weighted metrics
    g = ig.Graph.Weighted_Adjacency(f_matrix.tolist(), mode=ig.ADJ_MAX)
    N = g.vcount()

    # Convert to undirected graph
    g = g.as_undirected()

    g.vs['label'] = codes

    betweenness = g.betweenness(vertices=None, directed=False, cutoff=None, weights='weight') 
    export_data(codes, betweenness, 'betweenness_weight', thresh)

    print('   WEIGHTED VULNERABILITY')
    grp = GraphMaking(f_matrix)
    grp.create_graph(g)
    grp.weighted_vulnerability()
    export_data(codes, grp.weighted_vuln, 'wVuln', thresh)

    print('   WEIGHTED ISOLATION')
    grp.weighted_isolation()
    export_data(codes, grp.infinities_weight, 'wIsolation', thresh)'''