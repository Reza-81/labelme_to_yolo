import os
import yaml
import json
import random
import shutil
import argparse

#-------------------------------------------------------------------------------------------------------
def find_json_files(path, arr):
    """Find all JSON files in the given path.
    
    Args:
        path (str): The path to search for JSON files.
        arr (list): A list to store the paths of the found JSON files.
    """
    if os.path.isdir(path):
        for item in os.listdir(path):
            item_path = os.path.join(path, item)
            find_json_files(item_path, arr)
    elif path.endswith('json'):
        arr.append(path)

#-------------------------------------------------------------------------------------------------------
def convert_json_to_txt(json_path, txt_path, labels_list):
    """Converts a LabelMe JSON file to a YOLO format TXT file.(only rectangle and polygon shapes)
    
    Args:
        json_path (str): The path to the LabelMe JSON file.
        txt_path (str): The path where the resulting TXT file will be saved.
        labels_list (list): A list of labels used in the JSON file.
    """
    with open(json_path, 'r') as json_file:
        data = json.load(json_file)

    txt_file_name = os.path.basename(json_path)[:-5]

    with open(f'{txt_path}/{txt_file_name}.txt', 'a') as output_file:
        for shape in data['shapes']:
            new_line = str(labels_list.index(shape['label']))
            if shape['shape_type'] == 'polygon':
                for point in shape['points']:
                    new_line += f' {point[0] / data["imageWidth"]} {point[1] / data["imageHeight"]}'
            if shape['shape_type'] == 'rectangle':
                point_1 = shape['points'][0]
                point_2 = shape['points'][1]
                center_x = (point_2[0] + point_1[0]) / (2*data["imageWidth"])
                center_y = (point_2[1] + point_1[1]) / (2*data["imageHeight"])
                width = (point_2[0] - point_1[0]) / (data["imageWidth"])
                height = (point_2[1] - point_1[1]) / (data["imageHeight"])
                new_line += f' {center_x} {center_y} {width} {height}'
            output_file.write(new_line + '\n')

#-------------------------------------------------------------------------------------------------------
def split_dataset(train_ratio, valid_ratio, json_list, seed=42):
    """Split the dataset into train, validation, and test subsets.
    
    Args:
        train_ratio (float): The ratio of data to be allocated for the train subset.
        valid_ratio (float): The ratio of data to be allocated for the validation subset.
        json_list (list): A list of JSON file paths representing the dataset.
        seed (int, optional): The seed value used for random shuffling. Defaults to 42.
    
    Returns:
        tuple: A tuple containing three lists representing the train, validation, and test subsets, respectively.
    """
    random.seed(seed)
    random.shuffle(json_list)

    json_list_train = json_list[:int(train_ratio*len(json_list))]
    json_list_valid = json_list[int(train_ratio*len(json_list)):int(train_ratio*len(json_list) + valid_ratio*len(json_list))]
    json_list_test = json_list[int(train_ratio*len(json_list) + valid_ratio*len(json_list)):]

    return json_list_train, json_list_valid, json_list_test

#-------------------------------------------------------------------------------------------------------
def create_yaml_file(output_path, labels_list):
    '''create yaml file for dataset'''
    data = {
        'train': f'{output_path}/train/images',
        'test': f'{output_path}/test/images',
        'val': f'{output_path}/valid/images',
        'nc': len(labels_list),
        'names': labels_list
        }
    # Write the data to the YAML file
    with open(f'{output_path}/data.yaml', 'w') as yaml_file:
        yaml.dump(data, yaml_file)

#-------------------------------------------------------------------------------------------------------
if '__main__' == __name__:
    # Create an ArgumentParser object
    parser = argparse.ArgumentParser(description='My Python Program')

    # Define arguments
    parser.add_argument('--source', type=str, help='Source path')
    parser.add_argument('--output', type=str, help='Output path')
    parser.add_argument('--format', type=str, help='Image format')
    parser.add_argument('--labels', nargs='+', help='List of labels')
    parser.add_argument('--train-ratio', type=float, help='Train ratio (0 to 1)')
    parser.add_argument('--validation-ratio', type=float, help='Validation ratio (0 to 1)')
    parser.add_argument('--random-seed', type=int, default=42, help='Random seed')

    # Parse the command-line arguments
    args = parser.parse_args()

    # Access the argument values
    source_path = args.source
    output_path = args.output
    images_format = args.format
    labels_list = args.labels
    train_ratio = args.train_ratio
    validation_ratio = args.validation_ratio
    random_seed = args.random_seed

    # find json fils
    list_of_files = []
    find_json_files(source_path, list_of_files)

    # split to train, test, validation
    json_list_train, json_list_valid, json_list_test = split_dataset(train_ratio, validation_ratio, list_of_files, random_seed)

    # create train folder
    images_train_path = f'{output_path}/train/images'
    labels_train_path = f'{output_path}/train/labels'
    os.makedirs(images_train_path, exist_ok=True)
    for json_train in json_list_train:
        shutil.copy(json_train[:-4] + images_format, images_train_path)
    os.makedirs(labels_train_path, exist_ok=True)
    for json_train in json_list_train:
        convert_json_to_txt(json_train, labels_train_path, labels_list)

    # create validation folder
    images_valid_path = f'{output_path}/valid/images'
    labels_valid_path = f'{output_path}/valid/labels'
    os.makedirs(images_valid_path, exist_ok=True)
    for json_train in json_list_valid:
        shutil.copy(json_train[:-4] + images_format, images_valid_path)
    os.makedirs(labels_valid_path, exist_ok=True)
    for json_train in json_list_valid:
        convert_json_to_txt(json_train, labels_valid_path, labels_list)
    
    # create test folder
    images_test_path = f'{output_path}/test/images'
    labels_test_path = f'{output_path}/test/labels'
    os.makedirs(images_test_path, exist_ok=True)
    for json_train in json_list_test:
        shutil.copy(json_train[:-4] + images_format, images_test_path)
    os.makedirs(labels_test_path, exist_ok=True)
    for json_train in json_list_test:
        convert_json_to_txt(json_train, labels_test_path, labels_list)
    
    # create data.yaml
    create_yaml_file(output_path, labels_list)