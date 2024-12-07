
from iscas_parser import parse_iscas
from io_file_work import load_csv_file, generate_input_file

def simulation(simulation_type, circuit_path, inputs_path, test_vectors_path, delay_consideration, max_iterations, input_file_generation):
    
    circuit = parse_iscas(circuit_path)
    circuit.initialize_net_connections()
    circuit.set_levels()
    circuit.set_controlability()
    circuit.set_observability()
    circuit.draw_circuit()
    
    if (simulation_type == "PODEM"):
        print("PODEM simulation started")
    
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

