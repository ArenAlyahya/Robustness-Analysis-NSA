cd input_data
#python3 generate_BR_network.py
#python3 generate_SP_network.py
#python3 generate_states_network.py

python3 sum_maching_rows.py
python3 generate_US_network.py
python3 generate_US_STATES_network.py

cd ../src/
python3 setup.py

cd ../src/metrics
python3 net_stats.py

cd ../sort_nodes
#python3 sort_nodes_according_to_covid.py


cd ../robustness
#python3 export_sorted_cities_according_to_metrics.py
python3 network_robustness_failure.py
python3 network_robustness_stats.py
#python3 network_robustness_sorted_covid.py


cd ../plot
python3 plot_R.py