import glob
import os
import pathlib
import shutil

import model
from termcolor import colored


def get_diff_folders(
    folder: model.Folder, intermediate_path: list[str] | None = None
) -> tuple[list[list[str]], list[list[str]]]:
    """Returns path parts for added, deleted. Relative to model.PATH_TO_FICS"""
    intermediate_path = intermediate_path or []
    added = []
    deleted = []
    actual_path = pathlib.Path(*[model.PATH_TO_FICS, *intermediate_path])

    dirs_present = next(os.walk(actual_path))[1]  # only current sub-dirs
    folders = [name for name in folder.folders]

    overlap = [fold for fold in folders if fold in dirs_present]
    new_folders = [fold for fold in folders if fold not in dirs_present]
    old_dirs = [dirr for dirr in dirs_present if dirr not in folders]

    for fold in new_folders:
        added.append(intermediate_path + [fold])

    for dirr in old_dirs:
        deleted.append(intermediate_path + [dirr])

    for overlapped in overlap:
        subpath = intermediate_path + [overlapped]
        new, old = get_diff_folders(folder.folders[overlapped], subpath)
        added.extend(new)
        deleted.extend(old)

    return added, deleted


def delete_all(deleted: list[list[str]]) -> None:
    """From model.PATH_TO_FICS by relative paths"""
    for path_parts in deleted:
        path = os.path.join(*([model.PATH_TO_FICS] + path_parts))
        if os.path.isdir(path):
            shutil.rmtree(path)
        else:
            os.remove(path)


def get_filepaths_on_disk() -> list[list[str]]:
    result = []
    skip_n_parts = len(pathlib.Path(model.PATH_TO_FICS).parts)

    all_subpaths = glob.glob(model.PATH_TO_FICS + "/**", recursive=True)[1:]

    for sub in all_subpaths:
        if os.path.isfile(sub):
            path_parts = pathlib.Path(sub).parts[skip_n_parts:]
            result.append(list(path_parts))

    return result


def get_filepath_diff(
    root_folder: model.Folder, on_disk: list[list[str]]
) -> tuple[list[list[str]], list[list[str]], list[list[str]]]:
    """Same, added(new in bookmarks), deleted(old in files)."""
    same = []
    added = []
    deleted = []

    def does_link_exist_recursive(folder: model.Folder, path_parts: list[str]) -> bool:
        if len(path_parts) == 1:
            return bool(
                next(
                    (link for link in folder.links if link.name == path_parts[0]), False
                )
            )
        else:
            if subfolder := folder.folders.get(path_parts[0]):
                return does_link_exist_recursive(subfolder, path_parts[1:])
            else:
                return False

    for bookmark_path in root_folder.get_linknames():
        if bookmark_path not in on_disk:
            added.append(bookmark_path)

    for disk_path in on_disk:
        if does_link_exist_recursive(root_folder, disk_path):
            same.append(disk_path)
        else:
            deleted.append(disk_path)

    return same, added, deleted


def pretty_print_compare_folders(
    added: list[list[str]], deleted: list[list[str]]
) -> None:
    for add in added:
        print(colored(f"+ {model.DELIMITER.join(add)}", "green"))
    if not deleted:
        print(colored("\nNothing deleted.", "blue"))
    else:
        print("---------------------")
        for del_ in deleted:
            print(colored(f"DELETED:  {model.DELIMITER.join(del_)}", "red"))
        print("---------------------")


def pretty_print_compare_files(
    added: list[list[str]], deleted: list[list[str]]
) -> None:
    for add in added:
        print(colored(f"+ {model.DELIMITER.join(add)}", "green"))
    if not deleted:
        print(colored("\nNothing deleted.", "blue"))
    else:
        print("---------------------")
        for del_ in deleted:
            print(colored(f"DELETED:  {model.DELIMITER.join(del_)}", "red"))
        print("---------------------")
