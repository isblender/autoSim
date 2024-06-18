# SimNIBS Subject Simulation Script

This script is designed to run SimNIBS simulations on a set of subjects. The script can handle running simulations on a single subject, multiple specified subjects, or all subjects in a given directory.

## Prerequisites

- Python 3.x
- SimNIBS
- Necessary directories and subject data should be available in the specified paths.

## Usage

### Command-Line Arguments

- `--s`: List of subjects to run the simulation on. Provide subject directories without the common prefix (`ASD`, etc.).
- `--a`: Run the simulation on all subjects in the specified directory.
- `--c`: Compile all subjects in results, only for if theres error with automatic compiling.

### Examples

#### Run Simulation on All Subjects

```bash
python run_sim.py --s ASD001 ASD002
python run_sim.py --a
python run_sim.py --c
```
## Script Description

### Functions

1) compile_results(subjects, results_dir, results_file) -- Compiles results from individual subject simulations into a single results file.
2) get_subjects(subject_list) -- Retrieves and filters subject directories based on a provided list or includes all subjects that match a specific naming convention.
3) run_simulation(subjects) -- Runs the SimNIBS simulation on the specified subjects.

### Main Execution Flow
1) Uses argparse to parse command-line arguments for specifying subjects or running on all subjects.
2) Based on the parsed arguments, the script selects the appropriate subjects using the get_subjects function.
3) Runs the simulation on the selected subjects using the run_simulation function.
4) Compiles the results from the simulations into a single results file using the compile_results function.
