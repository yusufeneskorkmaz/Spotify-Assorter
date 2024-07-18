import os
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='[%(asctime)s]: %(message)s:')

project_name = "spotify_assorter"

list_of_files = [
    f"src/{project_name}/__init__.py",
    f"src/{project_name}/data_loader.py",
    f"src/{project_name}/classifier.py",
    f"src/{project_name}/playlist_manager.py",
    f"src/{project_name}/config.py",
    f"src/{project_name}/image_generator.py",
    "app.py",
    "main.py",
    "requirements.txt",
    ".gitignore",
    "README.md"
]

for filepath in list_of_files:
    filepath = Path(filepath)
    filedir, filename = os.path.split(filepath)
    if filedir != "":
        os.makedirs(filedir, exist_ok=True)
        logging.info(f"Creating directory: {filedir} for the file {filename}")
    if (not os.path.exists(filepath)) or (os.path.getsize(filepath) == 0):
        with open(filepath, 'w') as f:
            pass
        logging.info(f"Creating empty file: {filepath}")
    else:
        logging.info(f"{filename} already exists")

# Create directories
for dir in ["cover_images", "logs"]:
    os.makedirs(dir, exist_ok=True)
    logging.info(f"Created '{dir}' directory")

print("Project structure created successfully!")
