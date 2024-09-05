import subprocess
import os

import ctypes  # An included library with Python install.   

ctypes.windll.user32.MessageBoxW(0, "Starting...", "", 1)

image_dir = 'images'
database_path = "database.db"
sparse_dir = "sparse"
dense_dir = "dense"
meshed_dir = "meshed"
os.makedirs(sparse_dir, exist_ok=True)

project_ini = os.path.join(sparse_dir, "0")
project_ini = os.path.join(project_ini, "project.ini")

colmap_executable = r"C:\Users\noahv\Downloads\colmap-x64-windows-nocuda\COLMAP.bat"

ctypes.windll.user32.MessageBoxW(0, "feature extractor...", "", 1)

subprocess.run([
    colmap_executable, "feature_extractor", 
    "--database_path", database_path,
    "--image_path", image_dir
], check=True)

ctypes.windll.user32.MessageBoxW(0, "image matcher...", "", 1)

subprocess.run([
    colmap_executable, "exhaustive_matcher",
    "--database_path", database_path
], check=True)

ctypes.windll.user32.MessageBoxW(0, "image mapper...", "", 1)

subprocess.run([
    colmap_executable, "mapper",
    "--database_path", database_path,
    "--image_path", image_dir,
    "--output_path", sparse_dir
], check=True)

ctypes.windll.user32.MessageBoxW(0, "converting model...", "", 1)
for i in range(100):
    try:
        subprocess.run([
            colmap_executable, "model_converter",
            "--input_path", os.path.join(sparse_dir, f"{i}"),
            "--output_path", os.path.join(sparse_dir, f"{i}"),
            "--output_type", "TXT"
        ], check=True)
        os.remove(f'sparse/{i}/cameras.bin')
        os.remove(f'sparse/{i}/images.bin')
        os.remove(f'sparse/{i}/points3D.bin')
    except:
        break

# os.chdir(r"C:\Users\noahv\Downloads\colmap-x64-windows-nocuda")

# subprocess.run(['COLMAP.bat'])