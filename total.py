import os
import datetime

def get_file_timeline(root_path):
    """
    Scans a directory recursively and prints a timeline of all files and folders
    based on their last modification time.

    Args:
        root_path (str): The absolute or relative path to the directory you want to scan.
    """
    # Check if the provided path is a valid directory
    if not os.path.isdir(root_path):
        print(f"Error: The path '{root_path}' is not a valid directory.")
        return

    # Create a list to hold file/folder paths and their modification times
    timeline_items = []

    # os.walk recursively goes through the directory tree
    for dirpath, dirnames, filenames in os.walk(root_path):
        # Get timeline for subdirectories
        for dirname in dirnames:
            full_path = os.path.join(dirpath, dirname)
            try:
                # Get the modification time (st_mtime)
                mod_time = os.stat(full_path).st_mtime
                timeline_items.append((mod_time, full_path))
            except OSError as e:
                print(f"Could not access {full_path}: {e}")

        # Get timeline for files
        for filename in filenames:
            full_path = os.path.join(dirpath, filename)
            try:
                mod_time = os.stat(full_path).st_mtime
                timeline_items.append((mod_time, full_path))
            except OSError as e:
                print(f"Could not access {full_path}: {e}")

    # Sort the list by modification time (the first element of the tuple)
    timeline_items.sort(key=lambda x: x[0])

    # Print the sorted timeline
    print(f"--- File Timeline for '{os.path.abspath(root_path)}' ---")
    for mod_time, path in timeline_items:
        # Convert timestamp to a readable date-time format
        readable_time = datetime.datetime.fromtimestamp(mod_time).strftime('%Y-%m-%d %H:%M:%S')
        print(f"{readable_time} - {path}")


# --- How to use the function ---

# IMPORTANT: Replace '.' with the path you want to scan.
# For example:
# - To scan the current directory: path_to_scan = '.'
# - To scan your user's home directory on Windows: path_to_scan = 'C:/Users/YourUsername'
# - To scan your user's home directory on macOS/Linux: path_to_scan = '/home/YourUsername'

path_to_scan = 'C:/Users/acer/Desktop/python projects/ai model'  # Scans the directory where the script is running
get_file_timeline(path_to_scan)