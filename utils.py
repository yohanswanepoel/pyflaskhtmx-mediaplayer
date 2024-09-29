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

def get_first_playable_item(listing):
    for item in listing:
        if item['isfile']:
            return item
    return None

def find_previous_item(listing, previous_id):
    last_item_found = None
    for item in listing:
        if item['id'] == previous_id:
            return last_item_found
        if item['isfile']:
            last_item_found = item
    return last_item_found    

def find_next_item(listing, current_id):
    # Create a list of just the ids
    found = False
    done = False
    current_item = None
    for item in listing:
        if item['isfile']:
            if found == True:
                return item
            if item['id'] == current_id:
                found = True
                current_item = item
    return current_item

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
                    id = item.replace(" ","_").replace(".","_")
                    listing.append(dict(id=id, name=item, path=item_path, size=0, isfile=False))
    newlist = sorted(listing, key=lambda d: d['id'])
    return newlist