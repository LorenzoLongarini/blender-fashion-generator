import json
import random
import os
import shutil
import zipfile

def split_json(input_file, val_ratio = 0.1, seed= 42):
    
    output_dir = input_file
    input_folder = os.path.join(input_file, 'transforms_train.json')
    with open(input_folder, 'r') as f:
        data = json.load(f)
    
    frames = data['frames']
    n_frames = len(frames)
    n_val = int(n_frames * val_ratio)
    
    random.seed(seed)
 
    val_indices = set(random.sample(range(n_frames), n_val))
    train_data = data.copy()
    val_data = data.copy()
    train_frames = [f for i, f in enumerate(frames) if i not in val_indices]
    val_frames = [f for i, f in enumerate(frames) if i in val_indices]
    
    train_data['frames'] = train_frames
    val_data['frames'] = val_frames
    
    with open(os.path.join(output_dir, 'transforms_train.json'), 'w') as f:
        json.dump(train_data, f, indent=4)
    
    with open(os.path.join(output_dir, 'transforms_val.json'), 'w') as f:
        json.dump(val_data, f, indent=4)
    
    print(f"File divisi con successo!")
    print(f"Training frames: {len(train_frames)}")
    print(f"Validation frames: {len(val_frames)}")


def rename_files(train_path,
                 test_path,
                 ttc= False,
                 ngp = False
                ):
    
    current_path = os.getcwd()
    print(current_path)
    output_path = os.path.abspath(os.path.join(current_path, "assets", "output"))

    print(output_path) 

    train_folder = os.path.join(output_path, train_path)
    test_folder = os.path.join(output_path, test_path)
    
    if not os.path.exists(train_folder):
        print(f"{train_folder} does not exist.")
        return
    if not os.path.exists(test_folder):
        print(f"{test_folder} does not exist.")
        if not ttc:
            return
    new_folder = train_path.replace('_train', '')


    if not ttc:
        old_image_folder = os.path.join(test_folder, 'train')
        new_image_folder = os.path.join(test_folder, 'test')
        old_transform_file = os.path.join(test_folder, 'transforms_train.json')
        new_transform_file = os.path.join(test_folder, 'transforms_test.json')

    if os.path.exists(old_image_folder) and os.path.exists(old_transform_file):
        os.rename(old_image_folder, new_image_folder)
        os.rename(old_transform_file, new_transform_file)
    else:
        print(f"Folder {old_image_folder} does not exist.")

    shutil.move(new_image_folder, train_folder)
    shutil.move(new_transform_file, train_folder)
    shutil.rmtree(test_folder)

    new_path = os.path.join(output_path, new_folder)
    os.rename(train_folder, new_path)
    print(f"{train_folder} renamed in: {new_path}.")
    return new_path


def remove_png(path, ttc):
    train_file = f'{path}/transforms_train.json'
    with open(train_file, "r") as file:
        train_data = json.load(file)
    for frame in train_data.get("frames", []):
        file_path = frame.get("file_path", "")
        if file_path.endswith(".png"):
            frame["file_path"] = file_path.replace(".png", "")
    with open(train_file, "w") as file:
        json.dump(train_data, file, indent=4)


    if not ttc: 
        test_file = f'{path}/transforms_test.json'
        with open(test_file, "r") as file:
            test_data = json.load(file)
    
        for frame in test_data.get("frames", []):
            file_path = frame.get("file_path", "")
            if file_path.endswith(".png"):
                frame["file_path"] = file_path.replace(".png", "")
        with open(test_file, "w") as file:
            json.dump(test_data, file, indent=4)


    print(f"Removed .png")


def unzip(zip_filepath):

    if not os.path.exists(zip_filepath):
        print(f"File {zip_filepath} does not exist.")
        # return

    if zip_filepath.endswith('.zip'):
        new_filepath = zip_filepath[:-4]
        os.makedirs(new_filepath, exist_ok=True)
        with zipfile.ZipFile(zip_filepath, 'r') as zip_ref:
            zip_ref.extractall(new_filepath)
            print(f"File in {new_filepath}")
        os.remove(zip_filepath)
        print(f"ZIP File {zip_filepath} removed.")
    return zip_filepath

def dataset_manager(train_zip, test_zip, ttc):
    print("il valore di ttc è ", ttc)
    unzip(f'{train_zip}.zip')
    if not ttc:
        unzip(f'{test_zip}.zip')
        new_folder = rename_files(train_zip, test_zip, ttc)
    else: 
        new_folder = train_zip
    remove_png(new_folder, ttc)
    if not ttc: 
        split_json(new_folder)