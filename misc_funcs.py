import json
import os
import csv
import pandas as pd


def get_csv(path):
    """This function loads and returns the contents of a csv file"""
    with open(path) as f:
        a = [{k: v for k, v in row.items()}
             for row in csv.DictReader(f, skipinitialspace=True)]
    return a


def get_json(path):
    """This function loads and returns the contents of a json file"""
    json_file = open(path)
    json_file = json_file.read()
    return json.loads(json_file)


def reformat_data(prefix="MEGp", data_dir='./raw_data', processed_dir='./processed', trial_name='choice'):
    """This function takes the stimuli jsons and the response jsons for each subject and combines them into one big
    dataframe with all the subjects and all the trials"""

    # this will hold all of the trials for *all* of the subjects
    data = []

    # gets all the folders who fit the prefix of the task sets. Each folder is the data of a single subject.
    subjects = [{'id': x, 'dir': data_dir + "/" + x + "/csv"} for x in os.listdir(data_dir) if (x.startswith(prefix))]

    # iterates through all of the subjects:
    for subject in subjects:
        # grabs the paths of the stimuli files for all of the blocks
        stimuli_files = [f for f in os.listdir(subject['dir']) if os.path.isfile(os.path.join(subject['dir'], f)) and (
                f.startswith("block") and f.endswith(".json"))]

        # grabs the paths of the response files for all of the blocks
        resp_files = [subject['id'] + "_" + f for f in stimuli_files]

        if len(stimuli_files) == 0:
            # If the subject folder is empty, move to the next subject
            continue

        if not len(resp_files) == len(stimuli_files):
            # if subject did not complete the task (fewer response files than stimuli files), skip to next subject.
            continue

        # Iterate block by block
        for block_num in range(len(stimuli_files)):
            # load the json for the stimuli
            stim_block_json = get_json(subject['dir'] + "/" + stimuli_files[block_num])
            try:
                # attempt to grab the json for the responses
                resp_block_json = get_json(subject['dir'] + "/" + resp_files[block_num])
            except:
                # if there was an error, move on to the next iteration.
                continue
            # From the response files only keep the entries holding the relevant trial types (we don't need data about
            # fixation crosses or instructions displayed)
            resp_block_json = [entry for entry in resp_block_json if entry['name'] == trial_name]
            # Iterate trial by trial
            for trial_num in range(len(stim_block_json)):
                # combine the contents of the trial data from the stimuli file as well as the trial data from the
                # response file.
                trial = stim_block_json[trial_num] | resp_block_json[trial_num]  # merging the files

                # add a field called "chose" who explicitly states what the subject chose (shifted/swapped/neither)
                if trial['response'] == '1st':
                    trial['chose'] = trial['order'][0]
                elif trial['response'] == '2nd':
                    trial['chose'] = trial['order'][1]
                elif trial['response'] == 'neither':
                    trial['chose'] = "neither"
                else:  # If somehow some other value appeared, show an error. This shouldn't happen.
                    print("error")

                # Add a field that specifies the length of the melody in that trial
                trial['length'] = len(trial['probe'])
                data.append(trial)  # append the data

    # Now we will save the contents of "data" into a json file.

    # First we convert it to a JSON string.
    json_export = json.dumps(data)

    # Then we make the destination directory if it doesn't exist.
    try:
        os.mkdir(processed_dir)
    except:
        print("")
    else:
        print("Created directory: " + processed_dir)

    # we give the file a name
    filename = prefix + "_all_subjects.json"
    full_path = processed_dir + "/" + filename
    f = open(full_path, "w")
    f.write(json_export)
    f.close()
    print("Reformatted data.")

    # we save everything, and return some basic data/
    return {'filename': filename, 'folder': processed_dir, 'full_path': full_path}


def csv_to_pandas(file_path, format):
    """This script takes a csv file, and makes a pandas out of it, but structuring it in the way specified by
    'format' """

    subjects = get_csv(file_path)

    data = []
    for subject in subjects:
        for category in format:
            structure = {}
            for el in category['static']:
                structure[el] = category['static'][el]
            for el in category['dynamic']:
                structure[el] = subject[category['dynamic'][el]]
            data.append(structure)
    return pd.DataFrame(data)
