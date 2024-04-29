import model


is_line_comment = lambda line: "<!--" in line
is_line_list_start = lambda line: "<DL>" in line
is_line_list_end = lambda line: "</DL>" in line
is_line_header = lambda line: "<DT><H3" in line
is_line_link = lambda line: "<DT><A HREF" in line


def extract_name(line: str) -> str:
    start = line.rfind(">", None, -1) + 1
    end = line.find("</", start)
    return line[start:end]


def extract_link(line: str) -> model.Link:
    name = extract_name(line).replace("&#39;", "'")
    link_line = line.split('<A HREF="')[1]
    link = link_line[: link_line.find('"')]
    return model.Link(name, link)


def recursive_extract(lines: list[str], header_n: int) -> tuple[model.Folder, int]:
    """
    :param lines: All html lines, immutable
    :param header_n: line number of folder name
    :return: Folder, and closing line number in folder: </DL>
    """
    result = model.Folder()
    current_n = header_n + 1
    if not is_line_list_start(lines[current_n]):
        raise ValueError(
            f"Line {current_n}, '{lines[current_n] = }', is not list start"
        )
    while current_n < len(lines):
        current_n += 1
        current_line = lines[current_n]
        if is_line_comment(current_line):
            continue
        elif is_line_header(current_line):
            name = extract_name(current_line)
            subfolder, current_n = recursive_extract(lines, current_n)
            result.folders[name] = subfolder
        elif is_line_link(current_line):
            result.links.append(extract_link(current_line))
        elif is_line_list_end(current_line):
            return result, current_n
        else:
            raise ValueError(f"Unknown line type {current_n}, '{current_line = }'")
    raise ValueError("End of file")


def parse(filename: str) -> model.Folder:
    with (open(filename, encoding="utf-8") as bookmarks):
        bookmarks_str = bookmarks.read()
    lines = bookmarks_str.split("\n")
    knigi_n = next(line_n for line_n, line in enumerate(lines) if "книги" in line)
    return recursive_extract(lines, knigi_n)[0]
