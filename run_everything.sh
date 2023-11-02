cd input_data
python3 generate_BR_network.py
python3 generate_SP_network.py
python3 generate_states_network.py

cd ../src/metrics
python3 net_stats.py

cd ../sort_nodes
python3 sort_nodes_according_to_covid.py

cd ../robustness
python3 network_robustness_failure.py
python3 network_robustness_stats.py
python3 network_robustness_sorted_covid.py

cd ../plot
python3 plot_R.py