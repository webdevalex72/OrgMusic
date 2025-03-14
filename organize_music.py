import os
import shutil
from tinytag import TinyTag
from pathvalidate import sanitize_filepath
import traceback

def transform_genre(genre):
    # Select substring up to the first delimiter (comma or slash)
    genre = genre.split(',')[0].split('/')[0].strip()
    # Capitalize the first word
    genre = genre.capitalize()
    return genre

def organize_music(source_dir, dest_base):
    for root, _, files in os.walk(source_dir):
        for file in files:
            if file.lower().endswith(('.mp3', '.flac', '.ogg', '.m4a')):
                file_path = os.path.join(root, file)
                try:
                    tag = TinyTag.get(file_path)
                    # Extract tags or use defaults
                    album_artist = tag.albumartist or 'Unknown Album Artist'
                    genre = transform_genre(tag.genre or '')
                    album = tag.album or 'Unknown Album'
                    
                    # Sanitize folder names for filesystem compatibility
                    safe_album_artist = sanitize_filepath(album_artist, replacement_text='-')
                    safe_genre = sanitize_filepath(genre, replacement_text='-')
                    safe_album = sanitize_filepath(album, replacement_text='-')
                    
                    # Build target directory path
                    if genre:
                        target_dir = os.path.join(dest_base, safe_album_artist, safe_genre, safe_album)
                    else:
                        target_dir = os.path.join(dest_base, safe_album_artist, safe_album)
                    
                    # Ensure the target directory exists
                    os.makedirs(target_dir, exist_ok=True)
                    
                    # Move file
                    shutil.move(file_path, os.path.join(target_dir, file))
                    
                except Exception as e:
                    print(f"Error processing {file}: {str(e)}")
                    traceback.print_exc()
        
        # Remove the source directory if it is empty
        try:
            os.removedirs(root)
        except OSError as e:
            # Directory is not empty
            pass

if __name__ == "__main__":
    # Example usage:
    organize_music('/mnt/d/Test/', '/mnt/d/Music/')
