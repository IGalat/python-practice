import bookmarks_parser
import model
import state


def stage1_folder_diff(folders: model.Folder) -> None:
    added_folders, deleted_folders = state.get_diff_folders(folders)
    state.pretty_print_compare_folders(added_folders, deleted_folders)
    print("STAGE 1 Folder compare DONE")
    if deleted_folders:
        input_result = input("Delete dirs that are deleted in bookmarks? y/n:")
        if input_result == "y":
            state.delete_all(deleted_folders)
    else:
        input()


def stage2_file_diff(added: list[list[str]], deleted_links: list[list[str]]) -> None:
    state.pretty_print_compare_files(added, deleted_links)
    print("STAGE 2 File diff DONE")
    if deleted_links:
        input_result = input("Delete stories that are deleted in bookmarks? y/n:")
        if input_result == "y":
            state.delete_all(deleted_links)
    else:
        input()


def main() -> None:
    root_folder = bookmarks_parser.parse("bookmarks.html")
    # print(json.dumps(asdict(result), indent=2, ensure_ascii=False))

    stage1_folder_diff(root_folder)

    filepaths_on_disk = state.get_filepaths_on_disk()
    same, added, deleted = state.get_filepath_diff(root_folder, filepaths_on_disk)
    stage2_file_diff(added, deleted)


if __name__ == "__main__":
    main()
