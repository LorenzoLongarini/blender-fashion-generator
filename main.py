import os
import subprocess
from dotenv import load_dotenv

load_dotenv()

def add_blender_to_path(blender_path):
    os.environ["PATH"] = blender_path + os.pathsep + os.environ["PATH"]

def run_blender_script(script_path, blender_exec="blender"):
    try:
        command = [
            blender_exec,
            "--background",  
            "--python", script_path  
        ]
        subprocess.run(command, check=True)
        print("Blender executed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Error running Blender: {e}")
    except FileNotFoundError:
        print("Blender not found. Check your Blender PATH.")

if __name__ == "__main__":
    
    blender_dir = os.getenv('BLENDER_PATH')
    blender_script = r"./app.py"

    add_blender_to_path(blender_dir)

    run_blender_script(blender_script)
