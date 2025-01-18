import pandas as pd
import numpy as np
import network
import os

file_name = 'result_temp_df.csv'
path_to_data = 'code/dataFakhteh/email.dat'
result_df = pd.DataFrame(columns=['p', 'size_of_cascade', 'verlauf'])

# Check if there is a saved progress file
if os.path.exists(file_name):
    result_df = pd.read_csv(file_name)
    if not result_df.empty:
        # Extract the last processed values
        start_p = result_df['p'].iloc[-1]
    print(f"Resuming from p={start_p}")
else:
    start_p = 0.1
    print("Starting from the beginning.")

## reading data
data = []
with open (path_to_data,'r') as file:
    lines = file.readlines()
    for line in lines:                                                                                                                                        
        data.append(line.replace('\n','').split(" "))
df = pd.DataFrame(data,columns=['id_1','id_2','time'])
print(f"die anzahl der connection ist {len(df)}")
anzahl_nodes = len(list(df['id_2'].unique()) + list(df['id_1'].unique()))
print(f"die anzahl der nodes ist: {anzahl_nodes}")
print(f"die mean connection ist {len(df)/anzahl_nodes}")
def bin_data (data:list,intervall:int=0 ,bins:int=0)->list:
    if intervall>0:
        return([int(i)//10 for i in data ])
    if bin > 0:
        bind_data = [i%bins for i in range(len(data))]
        bind_data.sort()
        return(bind_data)
    print('error while bining data')


## preprering data
time_intervall = pow(10,4)
for p in np.arange(start_p,1,0.1):
    data = df.to_numpy()
    network_df = pd.DataFrame(data,columns=['node1','node2','time'])
    network_df['time'] = bin_data(network_df['time'].to_list(),time_intervall)
    all_nodes = set(network_df['node1'].to_list()+ network_df['node2'].to_list())
    nodeInfo_df = pd.DataFrame({'nodeId': list(all_nodes), 'p': [p]*len(all_nodes), 'c':[0]*len(all_nodes)}).set_index('nodeId')
    n = network.network()
    n.set_node_info(nodeInfo_df)
    n.set_network(network_df)
   
    n.shock_network(50,1)
    verlauf = n.check_cascade_with_new_nodes()
    cascade_size = n.size_of_cascade()

    # Save the result
    result_df.loc[len(result_df)] = {'t': time_intervall , 'p': p, 'size_of_cascade': cascade_size, 'verlauf': verlauf}
    result_df.to_csv(file_name, index=False)

