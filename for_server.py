import pandas as pd
import numpy as np
import network
import os

# Initialize variables
result_df = pd.DataFrame(columns=['z', 'p', 'size_of_cascade', 'verlauf'])
start_z = 0
start_p = 0.1

file_name = 'result_df.csv'

# Check if there is a saved progress file
if os.path.exists(file_name):
    result_df = pd.read_csv(file_name)
    if not result_df.empty:
        # Extract the last processed values
        start_z = result_df['z'].iloc[-1]
        start_p = result_df['p'].iloc[-1]
    print(f"Resuming from z={start_z}, p={start_p}")
else:
    print("Starting from the beginning.")

# Main loop
for z in range(start_z, 17):  # Iterate over z
    p_start = start_p if z == start_z else 0.1  # Resume at the right p for the starting z
    for p_int in range(int(p_start * 100), 27):  # Iterate over p (converted to integer steps)
        p = p_int / 100.0
        for _ in range(10):  # Repeat 10 times for each z and p
            # Generate and analyze the network
            n = network.network()
            n.generate_a_network_version2(size=5000, z=z, p=p)
            n.shock_network(size=30, c=1)
            verlauf = n.check_cascade()
            cascade_size = n.size_of_cascade()

            # Save the result
            result_df.loc[len(result_df)] = {'z': z, 'p': p, 'size_of_cascade': cascade_size, 'verlauf': verlauf}

        # Save progress after each p iteration
        result_df.to_csv(file_name, index=False)
    # Reset p after the first z iteration
    start_p = 0.1
