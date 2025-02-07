# ISCAS Test Simulation

A Python-based simulation framework for ISCAS benchmark circuits. This project provides tools for simulating and analyzing digital circuits using ISCAS benchmarks.

## Features
- Supports multiple ISCAS benchmark circuits.
- Modular object-oriented design.
- Jupyter Notebook for interactive analysis.
- Conda environment for easy dependency management.
- Implements circuit components such as gates, fanouts, and connections.
- Includes visualization tools for circuit structure and behavior.
- True value simulation with and without gate delay.
- Implementation of the PODEM algorithm to generate test vectors for single stuck-at faults.
- Reads fault input files and sequentially processes faults.
- Saves generated test vectors in the `test_vector` folder.

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/sadegh15khedry/ISCAS-Test-Simulation
   cd ISCAS-Test-Simulation
   ```
2. Create and activate the Conda environment:
   ```bash
   conda env create -f environment.yml
   conda activate iscas
   ```
3. Use the jupyter server for running the simulation.ipynb

## Usage
1. Select the the created jupyter server for running the simulation.ipynb
2. Set the circuit_name variable to the proper name of the circuit that you want to simulate
1. Run the Jupyter notebook




## Project Structure
```
ISCAS-Test-Simulation/
│── notebooks/
│   ├── simulation.ipynb    # simulation notebook
│── src/
│   ├── classes/        # Circuit simulation core classes
│   │   ├── circuit.py  # Defines circuit structure
│   │   ├── connection.py  # Handles circuit connections
│   │   ├── gate.py     # Implements logic gates
│   │   ├── fanout.py   # Handles fanout components
│   ├── resources/
│   │   ├── circuits/ # Contains circuits netlist files
│   │   ├── falut_input/ # Contains fault file for the PODEM simulation
│   │   ├── inputs/ # Contains inputs for true value simulation
│   │   ├── test_vector/ # Contains test vectors which PODEM simulation achived
│   ├── scritpts/
│   │   ├── io_file_work.py  # file work related script
│   │   ├── iscas_parser.py  # ISCAS parser script 
│   │   ├── simulation.py   # Simulation script file
│── /       # Directory for storing generated test vectors
│── environment.yml     # Conda environment setup
│── LICENSE            # License file
│── README.md          # Project documentation
```


## License
This project is licensed under the terms of the MIT license.

## Contributing
Feel free to fork the repository, create feature branches, and submit pull requests for improvements!

## Contact
For inquiries, reach out via GitHub issues or email at [your-email@example.com].
