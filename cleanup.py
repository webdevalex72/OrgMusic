import os
import shutil

def organize_audio(root_dir, audio_extensions=('.mp3', '.wav', '.flac')):
    # First move files
    for current_dir, subdirs, files in os.walk(root_dir):
        if not subdirs:  # Leaf directory
            relative_path = os.path.relpath(current_dir, root_dir)
            path_components = relative_path.split(os.sep)
            
            if len(path_components) > 1:
                target_folder = os.path.join(root_dir, path_components[0])
                os.makedirs(target_folder, exist_ok=True)
                
                for file in files:
                    if file.lower().endswith(audio_extensions):
                        src = os.path.join(current_dir, file)
                        dst = os.path.join(target_folder, file)
                        
                        if os.path.exists(dst):
                            base, ext = os.path.splitext(file)
                            counter = 1
                            while os.path.exists(dst):
                                new_name = f"{base}_{counter}{ext}"
                                dst = os.path.join(target_folder, new_name)
                                counter += 1
                        
                        shutil.move(src, dst)

    # Then delete empty folders
    delete_empty_folders(root_dir)

def delete_empty_folders(root):
    """Recursively delete empty folders from deepest level upwards"""
    removed = set()
    for dirpath, dirnames, filenames in os.walk(root, topdown=False):
        current_dir = dirpath
        if not dirnames and not filenames:
            try:
                os.rmdir(current_dir)
                removed.add(current_dir)
            except OSError:
                pass
    
    # Clean parent directories that became empty
    for dirpath, dirnames, filenames in os.walk(root, topdown=False):
        current_dir = dirpath
        if current_dir not in removed:
            try:
                if not os.listdir(current_dir):
                    os.rmdir(current_dir)
            except (OSError, FileNotFoundError):
                pass

if __name__ == "__main__":
    organize_audio("/mnt/d/Test/")  # Example usage
