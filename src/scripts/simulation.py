
from iscas_parser import parse_iscas
from io_file_work import load_csv_file, generate_input_file, load_fault_file


def simulation(simulation_type, circuit_path, inputs_path, fault_input_path, test_vectors_path, delay_consideration, max_iterations, input_file_generation):
    
    circuit = parse_iscas(circuit_path)
    circuit.initialize_net_connections()
    circuit.set_levels()
    circuit.set_controlability()
    circuit.set_observability()
    circuit.draw_circuit()
    
    if (simulation_type == "PODEM"):
        print("PODEM simulation started")
        row_count = 1
        fault_input = load_fault_file(fault_input_path)
        test_vectors = []
        
        for row in fault_input:
            print(f"iteration:{row_count}---------------------------------------")
            
            connection_name = row["connection"]
            stuck_at = row["stuck_at"]
            circuit.set_stuck_at_fault(connection_name, int(stuck_at))
            test_vector = circuit.run_podem()
            test_vectors.append(test_vector)
            print(f"test_vector: {test_vector}")
            circuit.remove_stuck_at_fault(connection_name)
            
            
            row_count += 1
            print("-------------------------------------------------------")
            
        print("-----------------------------------------------------------------")
        print("PODEM simulation finished")
        print(test_vectors)
    elif(simulation_type == 'true_value'):
        input_file = load_csv_file(inputs_path)
        if(input_file is None and input_file_generation == True):
            generate_input_file(circuit, inputs_path)
            input_file = load_csv_file(inputs_path)

        circuit.check_delays()
        time = 0
        while time < max_iterations:


            time = int(time)

                    
            print(f"Time step: {time} started -----------------------------")
        
            # time_step_inputs = input_file[input_file['time'] == time]
            time_step_inputs = input_file[input_file['time'] == time]
            circuit.set_circuit_inputs(time_step_inputs, time)
            circuit.pass_values_to_output(time, delay_consideration)
            circuit.print_connections_values()
            
            print(f"Time step: {time} ended -----------------------------")
            time = time + 1

