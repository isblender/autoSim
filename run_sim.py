import os
import shutil
import argparse
from simnibs import sim_struct, run_simnibs
import simnibs 

# Get current directory, make results directory if not already existing
curr_folder = '/nafs/sgreen/fmri/Prisma/TMS/Simnibs/subjects/'
scripts_folder = '/nafs/sgreen/fmri/Prisma/TMS/Simnibs/scripts/'
results_folder = os.path.join(scripts_folder, 'results')
results_file = os.path.join(results_folder, 'overall_results.txt')

if not os.path.exists(results_folder):
    os.makedirs(results_folder)
    print(f"Created directory: {results_folder}")
else:
    print(f"Directory already exists: {results_folder}")

def compile_results(subjects, results_folder, results_file):
    if not os.path.exists(results_file):
        os.system(f'touch {results_file}')
        print(f"'{results_file}' has been created in '{results_folder}'.")
    with open(results_file, 'w') as output_file:
        for _, subject in subjects.items():
            subject_results_file = os.path.join(results_folder, subject, 'fields_summary.txt')
            # Check if the results.txt file exists in the current subject directory
            if os.path.exists(subject_results_file):
                # Open and read the contents of the results.txt file
                with open(subject_results_file, 'r') as input_file:
                    contents = input_file.read()
                    # Write the contents to the overall_results.txt file
                    output_file.write(contents)
                    output_file.write('\n')
                    print(f'Wrote {subject}\'s results to overall results.')
def get_subjects(subject_list):
    subjects = {}
    for directory in os.listdir(curr_folder):
        # Check if there is mandated list
        if directory[0:3] == 'ASD' and (not subject_list or directory in subject_list):
            name = 'm2m_' + directory
            subject_dir = os.path.join(curr_folder, directory, 'T1_MPRAGE/')
            subjects[subject_dir] = name
    return subjects
def sim(subject_folder, subject):
    try:
        print(f'Starting session with {subject}')
        os.chdir(subject_folder)
        S = sim_struct.SESSION()
        S.subpath = subject
        S.pathfem = 'tms_simu'

        tms = S.add_tmslist()
        tms.fnamecoil = os.path.join('legacy_and_other','Magstim_70mm_Fig8.ccd')

        pos = tms.add_position()

        pos.centre = simnibs.mni2subject_coords([-34, 24, 44], subject) 
        pos.pos_ydir = simnibs.mni2subject_coords([-34, 24-10, 44], subject)
        pos.distance = 4
        run_simnibs(S)
        print(f'Simulation finished with {subject}')
        # Pause to allow Simnibs to read-in data and create head meshes
        os.sleep(15)
    except Exception as e:
        print(f'Error running simulation for {subject}: {e}')
def move_results(subject_folder, subject):
    original_results_path = os.path.join(subject_folder, 'tms_simu')
    new_results_name = subject[4:]
    # Replace 'new_name' with your desired new name
    new_results_path = os.path.join(results_folder, new_results_name)
    if os.path.exists(original_results_path):
        shutil.move(original_results_path, new_results_path)
        print(f"Moved and renamed directory: {original_results_path} to {new_results_path}")
    else:
        print(f"Tried finding results at: {original_results_path}, didn't exist")
def run_simulation(subjects):
    for subject_dir, subject in subjects.items():
        try:
            sim(subject_dir, subject)
            move_results(subject_dir, subject)
        except Exception as e:
            print(f'Error running simulation for {subject}: {e}')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run simulations on subjects.')
    parser.add_argument('--s', nargs='+', help='List of subjects to run the simulation on')
    parser.add_argument('--a', action='store_true', help='Run the simulation on all subjects')

    args = parser.parse_args()

    if args.a:
        subjects = get_subjects(None)
    else:
        subjects = get_subjects(args.s)

    if subjects:
        run_simulation(subjects)
        compile_results(subjects, results_folder, results_file)
    else:
        print('No subjects found to run the simulation on.')