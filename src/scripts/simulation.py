from iscas_parser import parse_iscas
from io_file_work import load_csv_file

def simulation(circuit_path, inputs_path, test_vecotors_path):
    
    circuit = parse_iscas(circuit_path)
    circuit.draw_circuit()
    
    input_file = load_csv_file(inputs_path)
    test_vector_file = load_csv_file(test_vecotors_path)
    
    # print(input_file)
    # print(test_vector_file)
    
    time = -20
    max_iterations = 50
    # while time < max_iterations:
    #     # Perform a single clock cycle
    #     if(time < 0):
    #         circuit.set_levels() 
    #         time += 0.1 
    #     elif(time >= 0):
    #         time = int(time)
    #         print(f"Time step: {time} started -----------------------------")
        
        
    #     # time_step_inputs = input_file[input_file['time'] == time]
    #     # circuit.set_input_value(time_step_inputs, time)
    #     # circuit.pass_values_to_output(time_step_inputs)
    #     # circuit.print_output(time)
        
    #         print(f"Time step: {time} ended -----------------------------")
    #         time = time + 1




