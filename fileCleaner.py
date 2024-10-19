import os
import shutil
from pathlib import Path
import ctypes
from ctypes import wintypes, byref, POINTER


# get the path
def get_downloads_folder():
    class GUID(ctypes.Structure):
        _fields_ = [
            ("Data1", wintypes.DWORD),
            ("Data2", wintypes.WORD),
            ("Data3", wintypes.WORD),
            ("Data4", wintypes.BYTE * 8)
        ]

    FOLDERID_Downloads = GUID(0x374DE290, 0x123F, 0x4565, (0x91, 0x64, 0x39, 0xC4, 0x92, 0x5E, 0x46, 0x7B))
    SHGetKnownFolderPath = ctypes.windll.shell32.SHGetKnownFolderPath
    SHGetKnownFolderPath.argtypes = [POINTER(GUID), wintypes.DWORD, wintypes.HANDLE, POINTER(ctypes.c_wchar_p)]
    SHGetKnownFolderPath.restype = ctypes.HRESULT
    path_ptr = ctypes.c_wchar_p()

    result = SHGetKnownFolderPath(byref(FOLDERID_Downloads), 0, None, byref(path_ptr))
    if result == 0:
        return path_ptr.value
    else:
        raise FileNotFoundError(f"Failed to retrieve Downloads folder path. HRESULT: {result}")

# path to downloads directory
downloads_path = get_downloads_folder()

categories = {
    "Images": [".png", ".jpg", ".jpeg", ".gif", ".bmp", ".tiff", ".webp"],
    "Documents": [".pdf", ".docx", ".doc", ".xlsx", ".pptx", ".txt", ".csv"],
    "Executables": [".exe", ".msi", ".bat"],
    "Zip_Packages": [".zip", ".rar", ".7z", ".tar", ".gz"],
    "Videos": [".mp4", ".avi", ".mkv", ".mov", ".wmv", ".flv"],
    "Torrents": [".torrent"]
}


# create directories for each category
def create_category_folders():
    for category in categories:
        folder_path = os.path.join(downloads_path, category)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)


# move files to directory
def move_files():
    for file_name in os.listdir(downloads_path):
        file_path = os.path.join(downloads_path, file_name)

        # skip directories
        if os.path.isdir(file_path):
            continue

        # Find the appropriate category for each file extension
        file_extension = os.path.splitext(file_name)[1].lower()
        for category, extensions in categories.items():
            if file_extension in extensions:
                destination_folder = os.path.join(downloads_path, category)
                shutil.move(file_path, destination_folder)
                print(f"Moved: {file_name} to {category}")
                break


def main():
    create_category_folders()
    move_files()
    print("Downloads directory cleaned up successfully!")


if __name__ == "__main__":
    main()
