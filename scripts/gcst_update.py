import os, subprocess
import shutil, filecmp
from pathlib import Path

GCST_NAME = "CMakeAutoBuild"
HERE = Path(__file__).resolve().parent
gcst_path = Path(subprocess.check_output(['git', '-C', HERE, 'rev-parse', '--show-toplevel'], text = True).strip()).absolute()
superproject_path = Path(subprocess.check_output(['git', '-C', HERE, 'rev-parse', '--show-superproject-working-tree'], text = True).strip()).absolute()

files_to_update = [
    "./.github/workflows",
    "./cmake",
    "./build.bat",
    "./build.sh",
    "./CMakeLists.txt",
    "./conanfile.py",
    "./configure.py",
    "./presets.json",
    "./scripts/gcst_update.py"
]

def get_updating_files():
    global files_to_update, gcst_path
    root = gcst_path
    all_files = []
    for entry in files_to_update:
        path = Path(gcst_path / entry).absolute()
        if not path.is_dir():
            all_files.append(path.relative_to(root, walk_up = True))
            continue

        for file in path.rglob("*"):
            if file.is_dir():
                continue
            all_files.append(file.relative_to(root, walk_up = True))

    matches, mismatches, errors = filecmp.cmpfiles(superproject_path, gcst_path, all_files, shallow=False)
    all_files = [name for name in all_files if (name in (set(mismatches) | set(errors))) and ((gcst_path / name).exists())]

    return all_files


def find_gcst_submodule():
    global NAME
    submodules = subprocess.check_output(['git', 'config', '--file', '.gitmodules', '--get-regexp', 'url'], text = True).strip().split("\n")
    for sm in submodules:
        data = sm.split()
        if data[1].removesuffix('.git') == f'https://github.com/Gaymocoder/{GCST_NAME}':
            return Path(data[0][len('submodule.'):-len('.url')]).absolute()
    return ''


def main():
    global superproject_path, gcst_path
    if (superproject_path == gcst_path):
        gcst_path = find_gcst_submodule()
        if (gcst_path == ''):
            print("The gcstemplate is not a submodule of any repo. Merging impossible")
            return 1

    mismatches = get_updating_files()
    if (mismatches == []):
        print("Everything is up-to-date")
        return 0

    files_list = ''.join(f'  .{os.sep}{p}\n' for p in mismatches)
    print(f"WARNING! The gcstemplate files will replace these files in your root repo directory:\n{files_list}")
    confirm = input("Make sure you've backuped all important edits from the files before updating them\nDo you want to continue? [Y/n] ")
    if confirm.lower() != "y":
        print("Aborted.")
        return 0

    for file in mismatches:
        ifile = gcst_path / file
        ofile = superproject_path / file

        print(f'Copying "./{(ifile).relative_to(superproject_path, walk_up = True)}" to "./{(ofile).relative_to(gcst_path, walk_up = True)}"')
        shutil.copy(ifile, ofile)

if __name__ == '__main__':
    main()