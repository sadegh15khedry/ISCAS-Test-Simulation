from iscas_parser import parse_iscas
from io_file_work import load_csv_file

def simulation(circuit_path, inputs_path, test_vectors_path, delay_consideration, max_iterations):
    
    circuit = parse_iscas(circuit_path)
    circuit.initialize_net_connections()
    circuit.draw_circuit()
    
    
    input_file = load_csv_file(inputs_path)
    # test_vector_file = load_csv_file(test_vectors_path)
    
    # print(input_file)
    # print(test_vector_file)
    
    time = -20
    while time < max_iterations:

        if(time < 0):
            circuit.set_levels() 
            time += 0.001 
        elif(time >= 0):
            time = int(time)
            # if(time == 0):
                # circuit.draw_circuit()
                
            print(f"Time step: {time} started -----------------------------")
    
            # time_step_inputs = input_file[input_file['time'] == time]
            time_step_inputs = input_file[input_file['time'] == time]
            circuit.set_circuit_inputs(time_step_inputs, time)
            circuit.pass_values_to_output(time, delay_consideration)
            circuit.print_connections_values()
        
            print(f"Time step: {time} ended -----------------------------")
            time = time + 1




