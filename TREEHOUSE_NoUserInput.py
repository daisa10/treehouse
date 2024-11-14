import os
import zipfile
import shutil
import subprocess
import re
import time
import threading
import glob


#unzips a file given and then puts all files in all subfolders into one main folder
def unzip_and_gather_files():
    # Step 1: Ask user for the zipped file
    zip_path = "/Users/sundaisa_khan/Desktop/elegant 4.zip" #### CHANGE PATH TO FILE YOU WANT TO UNZIP ! 

    # Step 2: Unzip the file
    if not zipfile.is_zipfile(zip_path):
        print(f"{zip_path} is not a valid zip file.")
        return

    extract_dir = "unzipped_files"
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_dir)
        print(f"Files extracted to: {extract_dir}")

    # Step 3: Gather all files in subfolders into one main folder
    output_dir = "main_folder"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Walk through the extracted directory and move files to the main folder
    for root, _, files in os.walk(extract_dir):
        for file in files:
            file_path = os.path.join(root, file)
            # Skip hidden files like .DS_Store or any that already exist
            if file.startswith('.') or os.path.exists(os.path.join(output_dir, file)):
                continue
            shutil.move(file_path, output_dir)

    print(f"All files have been moved to the folder: {output_dir}")

#adds 'main_folder/' to each lattice path in .ele files
def modify_lattice_paths():
    folder_path = "main_folder"
    for file in os.listdir(folder_path):
        if file.endswith('.ele'):
            ele_file_path = os.path.join(folder_path, file)
            with open(ele_file_path, 'r') as f:
                lines = f.readlines()
            
            with open(ele_file_path, 'w') as f:
                for line in lines:
                    if "lattice=" in line and ".lte" in line:
                        # Extract the original lattice file name and ignore any numerical prefixes
                        original_lattice = line.split('=')[1].strip().rstrip(',').split('/')[-1]  # Remove path and take just the filename
                        original_lattice = original_lattice.replace('main_folder/', '').replace('17_', '')  # Remove any number prefixes
                        new_lattice = f"main_folder/{original_lattice},"
                        f.write(f"\tlattice={new_lattice}\n")
                    else:
                        f.write(line)
    print(f"All .ele files in {folder_path} have been modified with updated lattice paths.")


# gathering result files into folder output_data
def gather_files_to_output():
    output_folder = "output_data"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    extensions = ['.cen', '.fin', '.flr', '.mat', '.parms', '.twi', '.out']

    while True:
        for root, _, files in os.walk("."):
            for file in files:
                if any(file.lower().endswith(ext) for ext in extensions):
                    file_path = os.path.join(root, file)
                    shutil.move(file_path, os.path.join(output_folder, file))
        time.sleep(5)  # Wait 5 seconds before checking again


#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

class Accelerator:
    def __init__(self):
        pass

    def SLACaccelerator(self):
        return 1

    def JLABaccelerator(self):
       
        #SEQUENCE FUNCTION:
        #inputSTART = input("Starting Point: ")
        #inputEND = input("Ending Point: ")
        #self.sequence(inputSTART, inputEND)
        
        #TWISS FUNCTION:
        #STARTING POINT: 
        #inputSTART = 
        #ENDING POINT:
        #inputEND = 
        #self.twiss(inputSTART, inputEND)
        
        #ERROR ANALYSIS FUNCTION:
        #Name the file you would like to run Error Analysis on:
        #inputSTART = 
        #self.error_analysis(inputSTART)
               

        #OPTIMIZATION FUNCTION:
        #location = "NL1" 
        #element_types = ["KQUAD"]  
        #optimization_functions = ["betax"] 
        #goal_values = [100]  
        #self.optimization(location, element_types, optimization_functions, goal_values)
        
        return 2 # comment this out when u run program, this is only for no errors when first coping and pasting code  
    
    def TRIUMFaccelerator(self):
            return 3




    def sequence(self, start, end):
        # Define the order of sequence and paths
        sequence_order = [
            "LERFTONL", "NL1", "ARC1", "SL2", "ARC2", "REINJ3", "NL3", "ARC3",
            "SL4", "ARC4", "REINJ5", "NL5", "ARC5", "SL6", "REINJ7", "NL7",
            "ARC7", "SL8", "ARC8A", "REINJ9", "NL9"
        ]
        folder_path = "main_folder"
        elegant_executable1 = "/Users/sundaisa_khan/elegant/elegant"
        elegant_executable2 = "-rpnDefns=/Users/sundaisa_khan/elegant/defns.rpn"

        # Verify that 'start' is in the sequence order
        if start not in sequence_order:
            print(f"Error: '{start}' is not in the sequence order.")
            return

        # Determine the indices for the start and end points in the sequence
        start_index = sequence_order.index(start)
        end_index = sequence_order.index(end) if end in sequence_order else start_index

        # If 'end' is 0, only run the 'start' file
        if end == 0:
            end_index = start_index

        # Track which files were successfully run
        files_ran = []

        # Iterate through the sequence from start to end
        for i in range(start_index, end_index + 1):
            file_key = sequence_order[i]

            # Search for a .ele file matching the sequence name in the folder
            ele_file = next((f for f in os.listdir(folder_path) if f.endswith(".ele") and file_key in f), None)

            if ele_file:
                ele_file_path = os.path.join(folder_path, ele_file)
                print(f"Running {ele_file_path}...")

                try:
                    # Execute the .ele file with Elegant
                    subprocess.run(
                        [elegant_executable1, elegant_executable2, ele_file_path],
                        check=True
                    )
                    files_ran.append(ele_file)
                except subprocess.CalledProcessError as e:
                    print(f"Error running {ele_file_path}: {e}")
            else:
                print(f"File for {file_key} not found in {folder_path}.")

        # Print the names of the files that were successfully run
        if files_ran:
            print("The following .ele files were run in sequence:")
            for file_name in files_ran:
                print(file_name)
        else:
            print("No files were run.")




    def twiss(self, inputSTART, inputEND):
        # Define the ordered sequence
        ordered_sequence = [
            "LERFTONL", "NL1", "ARC1", "SL2", "ARC2", "REINJ3", "NL3", "ARC3",
            "SL4", "ARC4", "REINJ5", "NL5", "ARC5", "SL6", "REINJ7", "NL7",
            "ARC7", "SL8", "ARC8A", "REINJ9", "NL9"
        ]

        # Get the subsequence from inputSTART to inputEND
        try:
            start_index = ordered_sequence.index(inputSTART)
            end_index = ordered_sequence.index(inputEND) + 1
            subsequence = ordered_sequence[start_index:end_index]
        except ValueError as e:
            print(f"Error: {e}")
            return

        folder_path = "main_folder"
        elegant_executable = "/Users/sundaisa_khan/elegant/elegant"
        rpn_defns = "-rpnDefns=/Users/sundaisa_khan/elegant/defns.rpn"

        # Initialize lists to store original content and outputs
        original_contents = {}
        tmp_files = []

        for i, seq_item in enumerate(subsequence):
            # Search for an exact match for .ele files in main_folder by matching sequence name before the .ele extension
            matching_files = [f for f in os.listdir(folder_path) if f.endswith('.ele') and f.split('_')[-1] == f"{seq_item}.ele"]
            if not matching_files:
                print(f"No file found for {seq_item}")
                continue
            original_file_path = os.path.join(folder_path, matching_files[0])

            # Create a backup of the original file to restore later
            backup_file_path = original_file_path + ".backup"
            shutil.copyfile(original_file_path, backup_file_path)

            # Run the first file normally without modifying Twiss parameters
            if i == 0:
                subprocess.run([elegant_executable, rpn_defns, original_file_path], check=True)

                # Process output and save Twiss parameters for the first file
                twi_file = original_file_path.replace('.ele', '.twi')
                tmp_file = original_file_path.replace('.ele', '.tmp')
                tmp_files.append(tmp_file)

                # Check if the .twi file was created
                if not os.path.exists(twi_file):
                    print(f"No .twi file found for {seq_item}")
                    continue

                # Extract Twiss parameters
                with open(tmp_file, "w") as f:
                    subprocess.run(
                        ["/bin/bash", "-c", f"/Users/sundaisa_khan/elegant/sdds2stream {twi_file} -col=betax,alphax,betay,alphay | sed -n '$p'"],
                        check=True,
                        stdout=f
                    )

                if not os.path.exists(tmp_file):
                    print(f"No .tmp file created for {seq_item}")
                    continue

                with open(tmp_file, "r") as f:
                    twiss_string = f.read().strip()

            else:
                with open(original_file_path, 'r') as file:
                    lines = file.readlines()

                # Remove existing Twiss parameter lines with beta_x, beta_y, alpha_x, and alpha_y
                updated_lines = [line for line in lines if 'beta_x' not in line and 'beta_y' not in line and 'alpha_x' not in line and 'alpha_y' not in line]

                prev_tmp_file = os.path.join(folder_path, f"{subsequence[i - 1]}.tmp")
                if not os.path.exists(prev_tmp_file):
                    print(f"No .tmp file found for {subsequence[i - 1]}")
                    continue

                with open(prev_tmp_file, 'r') as tmp_file:
                    twiss_string = tmp_file.read().strip()
                    betax, alphax, betay, alphay = twiss_string.split()

                twiss_string = f'beta_x={betax}, alpha_x={alphax}, beta_y={betay}, alpha_y={alphay}  !From {subsequence[i - 1]} exit\n'

                for index, line in enumerate(lines):
                    if 'beta_x' in line or 'beta_y' in line:
                        updated_lines.insert(index, twiss_string)
                        break

                with open(original_file_path, 'w') as file:
                    file.writelines(updated_lines)

                subprocess.run([elegant_executable, rpn_defns, original_file_path], check=True)

                twi_file = original_file_path.replace('.ele', '.twi')
                tmp_file = original_file_path.replace('.ele', '.tmp')
                tmp_files.append(tmp_file)

                if not os.path.exists(twi_file):
                    print(f"No .twi file found for {seq_item}")
                    continue

                with open(tmp_file, "w") as f:
                    subprocess.run(
                        ["/bin/bash", "-c", f"/Users/sundaisa_khan/elegant/sdds2stream {twi_file} -col=betax,alphax,betay,alphay | sed -n '$p'"],
                        check=True,
                        stdout=f
                    )

                if not os.path.exists(tmp_file):
                    print(f"No .tmp file created for {seq_item}")
                    continue

        # Revert all .ele files to their original content from backups and remove backup files
        for seq_item in subsequence:
            original_file_path = os.path.join(folder_path, f"{seq_item}.ele")
            backup_file_path = original_file_path + ".backup"
            if os.path.exists(backup_file_path):
                shutil.move(backup_file_path, original_file_path)

        # Delete all .tmp files
        for tmp_file in tmp_files:
            os.remove(tmp_file)

        print("Twiss function completed. Original files restored.")





    def error_analysis(self, user_input):
        # Set the relative path to the folder where .ele files are stored
        main_folder = "main_folder"

        # Initialize lattice_file_path for later use in reversion
        lattice_file_path = None

        # Search for the file containing the user input in the main_folder directory
        file_to_run = None
        for file in os.listdir(main_folder):
            if f"_{user_input}.ele" in file:
                file_to_run = os.path.join(main_folder, file)  # This will now be a relative path
                break

        if not file_to_run:
            print(f"No file found with the name containing '_{user_input}.ele'.")
            return

        # Ask user for the type of error to run
        print("Which error would you like to run?")
        print("1: Spatial")
        print("2: Angular")
        print("3: FSE")
        print("4: Energy")
        print("5: Twiss")

        error_choice = input("Enter the corresponding number for the error type: ")

        # Backup original content of .ele file for possible reversion
        with open(file_to_run, "r") as f:
            original_ele_content = f.readlines()
        
        # Read the .ele file for modification
        file_lines = original_ele_content.copy()

        # Condition for REINJ files with error choice 4 or 5
        if re.match(r"^REINJ\d+[A-Z]?$", user_input):
            if error_choice == "4":
                # Insert 'n_indices=1' after 'n_steps=1' for Energy error
                for i, line in enumerate(file_lines):
                    if line.strip() == "n_steps=1":
                        file_lines.insert(i + 1, "\tn_indices=1\n")
                        break

                # Locate .lte file and modify it
                lattice_file_match = re.search(r'lattice=main_folder/(\d{4}-\d{2}-\d{2}_REINJ\d+[A-Z]?\.lte),', ''.join(file_lines))
                if lattice_file_match:
                    lattice_file_name = lattice_file_match.group(1)
                    lattice_file_path = os.path.join(main_folder, lattice_file_name)

                    # Backup .lte file content
                    with open(lattice_file_path, "r") as f:
                        original_lte_content = f.readlines()

                    # Modify .lte file for Energy error
                    modified_lte_content = ["ERROR_ENERGY: MALIGN\n"] + [
                        line.replace("LINE=(", "LINE=(ERROR_ENERGY,") if "LINE=(" in line else line
                        for line in original_lte_content
                    ]

                    # Write modified .lte file
                    with open(lattice_file_path, "w") as f:
                        f.writelines(modified_lte_content)

            elif error_choice == "5":
                # Insert 'n_indices=1' after 'n_steps=1' for Twiss error
                for i, line in enumerate(file_lines):
                    if line.strip() == "n_steps=1":
                        file_lines.insert(i + 1, "\tn_indices=1\n")
                        break

                # Locate .lte file and modify it for Twiss error
                lattice_file_match = re.search(r'lattice=main_folder/(\d{4}-\d{2}-\d{2}_REINJ\d+[A-Z]?\.lte),', ''.join(file_lines))
                if lattice_file_match:
                    lattice_file_name = lattice_file_match.group(1)
                    lattice_file_path = os.path.join(main_folder, lattice_file_name)

                    # Backup .lte file content
                    with open(lattice_file_path, "r") as f:
                        original_lte_content = f.readlines()

                    # Modify .lte file for Twiss error
                    error_twiss_text = (
                        "ERROR_TWISS: TWISS, BETAX0= 1, ALPHAX0=1, ETAX0=0, ETAXP0=0, &\n"
                        "                    BETAY0= 1, ALPHAY0=1, ETAY0=0, ETAYP0=0, &\n"
                        "                    BETAX = 1, ALPHAX =1, ETAX =0, ETAXP =0, &\n"
                        "                    BETAY = 1, ALPHAY =1, ETAY =0, ETAYP =0\n"
                    )
                    modified_lte_content = [error_twiss_text] + [
                        line.replace("LINE=(", "LINE=(ERROR_TWISS,") if "LINE=(" in line else line
                        for line in original_lte_content
                    ]

                    # Write modified .lte file
                    with open(lattice_file_path, "w") as f:
                        f.writelines(modified_lte_content)

        # Condition for ARC files
        elif re.match(r"^ARC\d+[A-Z]?$", user_input):
            if error_choice == "4":
                # Insert n_indices=1 for energy error
                for i, line in enumerate(file_lines):
                    if line.strip() == "n_steps=1":
                        file_lines.insert(i + 1, "\tn_indices=1\n")
                        break

                # Locate .lte file and modify it for Energy error
                lattice_file_match = re.search(r'lattice=main_folder/(\d{4}-\d{2}-\d{2}_ARC\d+[A-Z]?\.lte),', ''.join(file_lines))
                if lattice_file_match:
                    lattice_file_name = lattice_file_match.group(1)
                    lattice_file_path = os.path.join(main_folder, lattice_file_name)

                    # Backup .lte file content
                    with open(lattice_file_path, "r") as f:
                        original_lte_content = f.readlines()

                    # Modify .lte file for Energy error
                    error_energy_text = "ERROR_ENERGY: MALIGN\n"
                    modified_lte_content = [error_energy_text] + [
                        line.replace("LINE=(", "LINE=(ERROR_ENERGY,") if "LINE=(" in line else line
                        for line in original_lte_content
                    ]

                    # Write modified .lte file
                    with open(lattice_file_path, "w") as f:
                        f.writelines(modified_lte_content)

            elif error_choice == "5":
                # Insert n_indices=1 for Twiss error
                for i, line in enumerate(file_lines):
                    if line.strip() == "n_steps=1":
                        file_lines.insert(i + 1, "\tn_indices=1\n")
                        break

                # Locate .lte file and modify it for Twiss error
                lattice_file_match = re.search(r'lattice=main_folder/(\d{4}-\d{2}-\d{2}_ARC\d+[A-Z]?\.lte),', ''.join(file_lines))
                if lattice_file_match:
                    lattice_file_name = lattice_file_match.group(1)
                    lattice_file_path = os.path.join(main_folder, lattice_file_name)

                    # Backup .lte file content
                    with open(lattice_file_path, "r") as f:
                        original_lte_content = f.readlines()

                    # Modify .lte file for Twiss error
                    error_twiss_text = (
                        "ERROR_TWISS: TWISS, BETAX0= 1, ALPHAX0=1, ETAX0=0, ETAXP0=0, &\n"
                        "                    BETAY0= 1, ALPHAY0=1, ETAY0=0, ETAYP0=0, &\n"
                        "                    BETAX = 1, ALPHAX =1, ETAX =0, ETAXP =0, &\n"
                        "                    BETAY = 1, ALPHAY =1, ETAY =0, ETAYP =0\n"
                    )
                    modified_lte_content = [error_twiss_text] + [
                        line.replace("LINE=(", "LINE=(ERROR_TWISS,") if "LINE=(" in line else line
                        for line in original_lte_content
                    ]

                    # Write modified .lte file
                    with open(lattice_file_path, "w") as f:
                        f.writelines(modified_lte_content)

        # Conditions for NL and SL files with error choice 4 or 5
        elif re.match(r"^(NL|SL)\d+$", user_input):
            if error_choice == "4" or error_choice == "5":
                # Insert n_indices=1 for Energy or Twiss error
                for i, line in enumerate(file_lines):
                    if line.strip() == "n_steps=1":
                        file_lines.insert(i + 1, "\tn_indices=1\n")
                        break

                # Locate .lte file and modify it
                lattice_file_match = re.search(r'lattice=main_folder/(\d{4}-\d{2}-\d{2}_(NL|SL)\d*\.lte),', ''.join(file_lines))
                if lattice_file_match:
                    lattice_file_name = lattice_file_match.group(1)
                    lattice_file_path = os.path.join(main_folder, lattice_file_name)

                    # Backup .lte file content
                    with open(lattice_file_path, "r") as f:
                        original_lte_content = f.readlines()

                    # Modify .lte file for Energy or Twiss error
                    error_text = "ERROR_ENERGY: MALIGN\n" if error_choice == "4" else (
                        "ERROR_TWISS: TWISS, BETAX0= 1, ALPHAX0=1, ETAX0=0, ETAXP0=0, &\n"
                        "                    BETAY0= 1, ALPHAY0=1, ETAY0=0, ETAYP0=0, &\n"
                        "                    BETAX = 1, ALPHAX =1, ETAX =0, ETAXP =0, &\n"
                        "                    BETAY = 1, ALPHAY =1, ETAY =0, ETAYP =0\n"
                    )
                    modified_lte_content = [error_text] + [
                        line.replace("LINE=(", f"LINE=({error_text.split(':')[0]},") if "LINE=(" in line else line
                        for line in original_lte_content
                    ]

                    # Write modified .lte file
                    with open(lattice_file_path, "w") as f:
                        f.writelines(modified_lte_content)

        # Define error blocks to insert in the .ele file
        error_blocks = {
            "1": '''&error_control error_log = %s.erl &end
&error_element type = gaussian, cutoff = 1.0, element_type=KQUAD, item = DX,   bind = 0, amplitude = 1e-4  &end
&error_element type = gaussian, cutoff = 1.0, element_type=KQUAD, item = DY,   bind = 0, amplitude = 1e-4  &end
&error_element type = gaussian, cutoff = 1.0, element_type=KQUAD, item = DZ,   bind = 0, amplitude = 1e-4  &end''',
            "2": '''&error_control error_log = %s.erl &end
&error_element type = gaussian, cutoff = 1.0, element_type=KQUAD, item = TILT, bind = 0, amplitude = 1e-4 &end''',
            "3": '''&error_control error_log = %s.erl &end
&error_element type = gaussian, cutoff = 1.0, element_type=KQUAD, item = FSE,  bind = 0, amplitude = 1e-2   &end''',
            "4": '''&error_control error_log = %s.erl &end
&vary_element name=ERROR_ENERGY, item=DE, initial=-0.05, final=0.05, index_number=0, index_limit=5 &end''',
            "5": '''&error_control error_log = %s.erl &end
&vary_element name=ERROR_TWISS, item=BETAX, initial=12.4578, final=37.3733, index_number=0, index_limit=5 &end
&vary_element name=ERROR_TWISS, item=ALPHAX, initial=-0.254739, final=-0.0849132, index_number=0, index_limit=5 &end
&vary_element name=ERROR_TWISS, item=BETAY, initial=1.54654, final=4.63962, index_number=0, index_limit=5 &end
&vary_element name=ERROR_TWISS, item=ALPHAY, initial=-3.07507, final=-1.02502, index_number=0, index_limit=5 &end'''
        }

        # Insert the error block in the .ele file
        insert_index = None
        for i, line in enumerate(file_lines):
            if '&floor_coordinates' in line:
                insert_index = i  # Insert before the &floor_coordinates line

        if insert_index is not None:
            error_block = error_blocks[error_choice] + '\n'
            file_lines.insert(insert_index, error_block)

        # Write the modified .ele file back
        with open(file_to_run, "w") as f:
            f.writelines(file_lines)

        # Run the .ele file using the relative path
        elegant_executable1 = "/Users/sundaisa_khan/elegant/elegant"
        elegant_executable2 = "-rpnDefns=/Users/sundaisa_khan/elegant/defns.rpn"
        subprocess.run([elegant_executable1, elegant_executable2, file_to_run], check=True)

        # Ask if user wants to revert the files
        revert = input("Would you like to revert the file back to its original form? (yes/no): ")

        if revert.lower() == "yes":
            # Revert the .ele file
            with open(file_to_run, "w") as f:
                f.writelines(original_ele_content)
            
            # Revert the .lte file if it was modified
            if lattice_file_path:
                with open(lattice_file_path, "w") as f:
                    f.writelines(original_lte_content)




    def optimization(self, location, element_types, optimization_functions, goal_values):
        # Step 1: Locate the .ele file in main_folder using a pattern match for any file ending in {location}.ele
        main_folder = 'main_folder'
        ele_file_pattern = os.path.join(main_folder, f"*{location}.ele")
        ele_files = glob.glob(ele_file_pattern)
        
        # Check if any file matches the pattern
        if not ele_files:
            print(f"Error: No file found matching pattern *{location}.ele in {main_folder}.")
            return
        ele_file_path = ele_files[0]  # Take the first match

        # Step 2: Open .lte file
        with open(ele_file_path, 'r') as file:
            content = file.read()
        lattice_line = re.search(r"lattice=(main_folder/[\w-]+\.lte)", content)
        if not lattice_line:
            print("Error: Lattice line not found in .ele file.")
            return
        lte_filename = lattice_line.group(1).split('/')[-1]
        lte_file_path = os.path.join(main_folder, lte_filename)

        # Step 2a to 2c: Extract element names for each type in element_types
        element_names = []
        for i, element_type in enumerate(element_types):
            cmd = f"awk '/{element_type}/' {lte_file_path} | awk '{{print $1}}' | awk '{{gsub(/:/, \"\"); print}}'"
            try:
                result = subprocess.check_output(cmd, shell=True).decode().strip().split('\n')
                element_names.append(result)
            except subprocess.CalledProcessError as e:
                print(f"Error executing command for element type {element_type}: {e}")
                return

        # Step 2d: Construct &optimization_term vector
        optimization_term = []
        for i, (opt_func, goal_val) in enumerate(zip(optimization_functions, goal_values)):
            term = f'&optimization_term term = "{opt_func} {goal_val} 1e-6 sene",weight=1 &end'
            optimization_term.append(term)

        # Step 2e and 2f: Construct &optimization_variable vector
        optimization_variable = []
        for i, names in enumerate(element_names):
            for name in names:
                var = f"&optimization_variable\n        name = {name}, item=K1, lower_limit=-100.0, upper_limit=100.0, step_size = 0.001 &end"
                optimization_variable.append(var)

        # Step 3a: Modify the .ele file by removing specific lines and adding optimization terms/variables
        with open(ele_file_path, 'r') as file:
            lines = file.readlines()

        start_run_control = None
        end_floor_coordinates = None
        for idx, line in enumerate(lines):
            if '&run_control' in line:
                start_run_control = idx
            elif '&floor_coordinates' in line:
                end_floor_coordinates = idx - 1  # The line before '&floor_coordinates'
                break

        if start_run_control and end_floor_coordinates:
            del lines[start_run_control+3:end_floor_coordinates + 1] # Donish
            insertion_index = start_run_control

            # Insert &optimization_term and &optimization_variable between '&run_setup' and '&floor_coordinates'
            new_lines = optimization_term + optimization_variable
            for term in new_lines:
                lines.insert(insertion_index, term + "\n")
                insertion_index += 1

            # Step 4: Replace '&track' and '&end' with new optimization commands
            for idx, line in enumerate(lines):
                if '&track' in line and idx + 1 < len(lines) and '&end' in lines[idx + 1]:
                    lines[idx] = "&optimize summarize_setup=1 &end\n"
                    lines[idx + 1] = "&save_lattice filename = %s.new &end\n"
                    break

            # Write the updated content back to the file
            with open(ele_file_path, 'w') as file:
                file.writelines(lines)

            print(f"{location} file has been optimized.")
        else:
            print("Error: Couldn't find &run_control or &floor_coordinates in the .ele file.")
            return

        # Step 5: Run the optimized .ele file using the specified elegant executable
        elegant_executable1 = "/Users/sundaisa_khan/elegant/elegant"
        elegant_executable2 = "-rpnDefns=/Users/sundaisa_khan/elegant/defns.rpn"
        
        try:
            subprocess.run([elegant_executable1, elegant_executable2, ele_file_path], check=True)
            print(f"Successfully ran the optimized file: {ele_file_path}")
        except subprocess.CalledProcessError as e:
            print(f"Error running the optimized .ele file: {e}")


# MAIN PROGRAM $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$


if __name__ == "__main__":
    # Start file gathering in the background
    file_mover_thread = threading.Thread(target=gather_files_to_output, daemon=True)
    file_mover_thread.start()

  
    unzip_and_gather_files() #function to unzip a file insert file name inside function: comment this line out after file has been unzipped 
    modify_lattice_paths() 
   

   

    # Initialize the Accelerator class
    job = Accelerator()

    # Run the selected accelerator function based on user input

    #job.SLACaccelerator()
   
    job.JLABaccelerator() #go to JLABaccelerator and un-comment the Testing fucntion u want to do 

    #job.TRIUMFaccelerator()









