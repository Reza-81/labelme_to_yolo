# Dataset Conversion Tool

This is a Python script that helps you convert a dataset in LabelMe JSON format to YOLO format. It provides functionality to split the dataset into train, validation, and test subsets, and creates the necessary folder structure and YAML file required for training an object detection model using YOLO.

## Prerequisites

Before using this tool, make sure you have the following:

- Python 3 installed on your system

- The required Python packages installed. You can install them by running the following command:

  ```shell
  pip install -r requirements.txt

## Usage

To use this tool, follow the steps below:

1. Clone this repository to your local machine:

   ```shell
   git clone https://github.com/Reza-81/labelme_to_yolo.git

2. Navigate to the project directory:

   ```shell
   cd labelme_to_yolo

3. Run the script with the required arguments:

    ```shell
    python labelme_to_yolo.py --source /path/to/dataset --output /path/to/output --format image_format --labels label1 label2 ... --train-ratio train_ratio --validation-ratio validation_ratio --random-seed random_seed
    ```

    Replace the `/path/to/dataset` with the path to your dataset in LabelMe JSON format. The `/path/to/output` should be the directory where the converted dataset will be saved. The `image_format` should be the format of the images in the dataset, such as 'jpg' or 'png'. The `label1`, `label2`, ... should be the labels used in the JSON files. The `train_ratio` and `validation_ratio` should be the ratios (between 0 and 1) for splitting the dataset into train and validation subsets. The `random_seed` is an optional argument that sets the random seed for shuffling the dataset (default is 42).

4. After running the script, the dataset will be split into train, validation, and test subsets. The converted dataset will be saved in the specified output directory, with the following folder structure:

    ```shell
    output/
    ├── train/
    │   ├── images/
    │   │   ├── image1
    │   │   ├── image2
    │   │   └── ...
    │   └── labels/
    │       ├── image1.txt
    │       ├── image2.txt
    │       └── ...
    ├── valid/
    │   ├── images/
    │   │   ├── image1
    │   │   ├── image2
    │   │   └── ...
    │   └── labels/
    │       ├── image1.txt
    │       ├── image2.txt
    │       └── ...
    └── test/
        ├── images/
        │   ├── image1
        │   ├── image2
        │   └── ...
        └── labels/
            ├── image1.txt
            ├── image2.txt
            └── ...
    ```

    The train folder contains the images and corresponding label files for the train subset. The valid folder contains the images and label files for the validation subset, and the test folder contains the images and label files for the test subset.

5. Additionally, a data.yaml file will be created in the output directory. This file contains the configuration information for the dataset, including the paths to the train, validation, and test subsets, the number of classes, and the list of labels.
