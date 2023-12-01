# -*- coding: utf-8 -*-

import numpy as np

import flow_matrix



# Load the flow matrix
#TODO road data needed {id1 ciry1 id2 city2 flow}

#f_matrix_original => flow matrix ,, codes => city ID
f_matrix_original, codes = flow_matrix.generate_flow_matrix('processed_T_T100D_MARKET_US_CARRIER_ONLY.csv')  
N = len(f_matrix_original)	
#################################################


print('GENERATING US NETWORK')


file_out = open('US_network.csv','w')

for row in range(N):
	file_out.write(str(f_matrix_original[row,0]))
	for col in range(1,N):
		file_out.write(';' + str(f_matrix_original[row,col]))
	file_out.write('\n')
file_out.close()


file_out = open('US_network_codes.csv','w')
for i in range(N):
	file_out.write(str(codes[i]) + '\n')
file_out.close()