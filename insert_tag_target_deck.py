import os
import re

directory_path = "/Users/isgeun/Library/Mobile Documents/iCloud~md~obsidian/Documents/NOTE - iCloud Drive/1 Project/해커스 토익 기출 보카/0 Attachment/0 해커스 토익 기출 보카1"

md_file_names_in_current_directory =  os.listdir(directory_path); md_file_names_in_current_directory = [_ for _ in md_file_names_in_current_directory if _[-3:] == ".md"]

for md_file_name in md_file_names_in_current_directory:
    md_file_name_except_prefix_and_extension = re.sub(r"^\d+ ", "", md_file_name); md_file_name_except_prefix_and_extension = md_file_name_except_prefix_and_extension[:-3]
    with open(f"{directory_path}/{md_file_name}", 'r') as f:
        file_lines = f.readlines(); file_lines = "".join(file_lines)
        
        lines_to_be_inserted = f"---\ntags:\n  - Obsidian_to_Anki\n---\nTARGET DECK\n1 Project::해커스 토익 기출 보카::{md_file_name_except_prefix_and_extension}\n\n"
        
        file_lines = lines_to_be_inserted + file_lines

    with open(f"{directory_path}/{md_file_name}", 'w') as f:
        f.writelines(file_lines)
