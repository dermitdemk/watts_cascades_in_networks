import pandas as pd
import numpy as np
import network
import os

file_name = 'result_temp_df_conference_20_01_v3.csv'
path_to_data = 'code/dataFakhteh/FilmMessages.txt'
result_df = pd.DataFrame(columns=['t','p', 'size_of_cascade', 'verlauf'])

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



## preprering data
inter_valle = [pow(10,2),pow(10,3),pow(10,4),pow(10,5)]
for _ in range(5):
    for time_intervall in inter_valle:
        for p in np.arange(start_p,1.1,0.1):
            n = network.network()
            n.read_csv(path_to_data,p)
            n.bin_data(intervall =time_intervall)
            n.shock_network(int(len(n.nodes)*0.01),1,0)
            verlauf = n.check_cascade_with_new_nodes()
            cascade_size = n.size_of_cascade()

            # Save the result
            result_df.loc[len(result_df)] = {'t': time_intervall , 'p': p, 'size_of_cascade': cascade_size, 'verlauf': verlauf}
            result_df.to_csv(file_name, index=False)

