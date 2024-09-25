import os
from os import listdir
from os.path import isfile, join

def get_curent_path():
    return os.getcwd()

def get_file_size(file_path):
    # Get file size in bytes
    size_bytes = os.path.getsize(file_path)
    
    # Convert to a more readable format
    if size_bytes < 1024:
        return f"{size_bytes} bytes"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.2f} KB"
    elif size_bytes < 1024 * 1024 * 1024:
        return f"{size_bytes / (1024 * 1024):.2f} MB"
    else:
        return f"{size_bytes / (1024 * 1024 * 1024):.2f} GB"

def list_files(mypath, filter_str):
    listing = []
    matches = ["jpg", "jpeg", "mp4", "gif", "webp", "webm"]
    items = listdir(mypath)
    for item in items:
        if not item.startswith((".","_")): 
            item_path = os.path.join(mypath, item)
            if filter_str in item:
                if os.path.isfile(item_path):
                    if any(x in item.lower() for x in matches):
                        size = get_file_size(item_path)
                        id = item.replace(" ","_").replace(".","_")
                        listing.append(dict(id=id, name=item, path=item_path, size=size, isfile=True))
                elif os.path.isdir(item_path):
                    listing.append(dict(name=item, path=item_path, size=0, isfile=False))

    return listing