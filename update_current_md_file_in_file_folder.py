import os
import re

vault_directory = "/Users/isgeun/Library/Mobile Documents/iCloud~md~obsidian/Documents/NOTE-iCloud_Drive"

# 폴더 파일('0 '으로 시작하는 MD 파일)을 찾을 디렉토리들을 저장하는 스택
directory_paths = [vault_directory]
while not (directory_paths == []):
    # 현재 폴더 파일을 찾고자하는 디렉토리
    current_directory_path = directory_paths.pop()
    # * 폴더 파일 만들고 md file 제목 만들기
    # "0 Inbox"에서 "0 "와 같은 순서를 뺀 디렉토리 이름
    current_directory_name_without_order = re.sub(r"^\d+? ", "", os.path.basename(current_directory_path))
    folder_file = f"{current_directory_path}/0 {current_directory_name_without_order}.md"
    # 폴더 파일 생성(있다면 그대로 놔두고, 없다면 새로 생성)
    os.system(f"touch \"{folder_file}\"")
    
    # 폴더 파일에서 MD File의 dataview에 있는 file.name에 넣은 문자열
    file_dot_folder_to_be_inserted = current_directory_path.replace(f"{vault_directory}", "").strip('/')
    
    # 폴더 파일에서 MD File heading default string
    sub_md_file_default_str = f"\n# MD File\n```dataview\nTABLE file.mday as 수정일, file.cday as 생성일, file.size as \"파일 크기\"\nWHERE\n\tfile.folder = \"{file_dot_folder_to_be_inserted}\"\n\tAND file.name != this.file.name\nSORT file.mday DESC\n```\n"
    
    ## * 폴더 파일에서 MD File의 dataview에 있는 file.name을 찾음
    # 파일 내용을 문자열로 불러오기
    with open(folder_file, "r") as f:
        folder_file_lines = f.readlines(); folder_file_lines = "".join(folder_file_lines)
        
    # MD File heading regex pattern
    md_file_pattern = re.compile(r"# MD File\n```dataview\n(.*?\n)*?WHERE\n\tfile.folder = \"(.*?)\"\n(.*?\n)*?```")
    match = re.search(md_file_pattern, folder_file_lines)
    if match != None:
        file_dot_folder_in_dataview = match.group(2)
        file_dot_folder_indexes = [match.start(2), match.end(2)]
        
    ## * match 되는지, 변경할 문자열과 삽입할 문자열이 같은지 여부에 따라 파일 내용을 변경
    if match == None:
        folder_file_lines = folder_file_lines + sub_md_file_default_str
    elif file_dot_folder_in_dataview != file_dot_folder_to_be_inserted:
            folder_file_lines = folder_file_lines[:file_dot_folder_indexes[0]] + file_dot_folder_to_be_inserted + folder_file_lines[file_dot_folder_indexes[1]:]
    else:
        pass
    ## * 폴더 파일에 최신화된 파일 내용 저장, 최신화된 파일 내용이라면 변경사항이 없음.
    with open(folder_file, "w") as f:
        f.writelines(folder_file_lines)
    
    # * 다음 탐색할 디렉토리 directory_paths에 append
    # 현재 폴더에 있는 하위 파일 및 폴더
    current_sub_names = os.listdir(current_directory_path)
    # 현재 폴더에 있는 하위 폴더
    current_sub_directory_names = [_ for _ in current_sub_names if os.path.isdir(f"{current_directory_path}/{_}")]
    # "0 Attachment"를 제외한 현재 폴더에 있는 숨겨지지 않은 하위 폴더
    current_sub_directory_names_without_hidden = [_ for _ in current_sub_directory_names if _.find(".") == -1]; current_sub_directory_names_without_hidden = [_ for _ in current_sub_directory_names_without_hidden if _ != "0 Attachment"]
    # directory_paths에 현재 폴더의 하위 폴더(current_sub_directory_names_without_hidden) 모두 넣음
    for _ in current_sub_directory_names_without_hidden:
        directory_paths.append(f"{current_directory_path}/{_}")
