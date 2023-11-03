import re
import os

vault_directory = "/Users/isgeun/Library/Mobile Documents/iCloud~md~obsidian/Documents/NOTE-iCloud_Drive"

# Layer 0 종류
layer0_suffix = ["웹 클립", "유튜브"]
# Layer 0의 MD 파일을 찾는 Dataview 정규식
layer0_regex_in_dataview = "";
layer0_regex_in_dataview += ".* - ("
for i, _ in enumerate(layer0_suffix):       
    layer0_regex_in_dataview += _
    if i != len(layer0_suffix) - 1:
        layer0_regex_in_dataview += '|'
layer0_regex_in_dataview += ")$"

# 폴더 파일('0 '으로 시작하는 MD 파일)을 찾을 디렉토리들을 저장하는 스택
directory_paths = [vault_directory]
while not (directory_paths == []):
    # 현재 폴더 파일을 찾고자하는 디렉토리
    current_directory_path = directory_paths.pop()
    
    # * 폴더 파일 생성
    # "0 Inbox"에서 "0 "와 같은 순서를 뺀 디렉토리 이름
    current_directory_name_without_order = re.sub(r"^\d+? ", "", os.path.basename(current_directory_path))
    folder_file = f"{current_directory_path}/0 {current_directory_name_without_order}.md"
    # 폴더 파일 생성(있다면 그대로 놔두고, 없다면 새로 생성)
    os.system(f"touch \"{folder_file}\"")

    # * 하위 폴더, MD 파일 제목 기본 문자열
    # 폴더 파일에서 Folder heading default string
    sub_directory_default_str = "\n# Folder\n```dataview\nTABLE file.mday as 수정일, file.cday as 생성일, file.size as \"파일 크기\"\nWHERE\n\tlength(split(regexreplace(replace(file.folder, this.file.folder, \"\"), \"^/\", \"\"),  \"/\")) = 1\n\tAND startswith(file.name, \"0 \")\n\tAND startswith(file.folder, this.file.folder)\n\tAND file.name != this.file.name\nSORT file.name ASC\n```\n"
    # 폴더 파일에서 MD File heading default string
    sub_md_file_default_str = f"\n# MD File\n```dataview\nTABLE file.mday as 수정일, file.cday as 생성일, file.size as \"파일 크기\"\nWHERE\n\tfile.folder = this.file.folder\n\tAND file.name != this.file.name\n\tAND !regexmatch(\"{layer0_regex_in_dataview}\", file.name)\nSORT file.mday DESC\n```\n"
    # 폴더 파일에서 Layer 0 heading default string
    sub_layer0_default_str = f"\n# Layer 0\n```dataview\nTABLE file.mday as 수정일, file.cday as 생성일, file.size as \"파일 크기\"\nWHERE\n\tfile.folder = this.file.folder\n\tAND file.name != this.file.name\n\tAND regexmatch(\"{layer0_regex_in_dataview}\", file.name)\nSORT file.mday DESC\n```\n"
    
    # * 하위 폴더, MD 파일 제목 정규식 패턴
    # Folder heading regex pattern
    sub_directory_pattern = re.compile(r"^# Folder\n```dataview\n(.*?\n)*?```", re.MULTILINE)
    # MD File heading regex pattern
    sub_md_file_pattern = re.compile(r"^# MD File\n```dataview\n(.*?\n)*?```", re.MULTILINE)
    # Layer 0 heading regex pattern
    sub_layer0_pattern = re.compile(r"^# Layer 0\n```dataview\n(.*?\n)*?```", re.MULTILINE)
    
    # * 파일을 문자열로 불러와 문자열을 변경함
    ## * 폴더 파일을 문자열로 불러옴
    folder_file_lines = None
    # 파일 내용을 문자열로 불러오기
    with open(folder_file, "r") as f:
        folder_file_lines = f.readlines(); folder_file_lines = "".join(folder_file_lines)
    
    ## * 하위 폴더, MD 파일 제목 모두 없애기
    # 하위 폴더 제목 모두 없애기
    match_sub_directory = re.search(sub_directory_pattern, folder_file_lines)
    while match_sub_directory != None:
        folder_file_lines = folder_file_lines[:match_sub_directory.start(0)] + folder_file_lines[match_sub_directory.end(0):]
        
        match_sub_directory = re.search(sub_directory_pattern, folder_file_lines)
    # 하위 MD 파일 제목 모두 없애기
    match_sub_md_file = re.search(sub_md_file_pattern, folder_file_lines)
    while match_sub_md_file != None:
        folder_file_lines = folder_file_lines[:match_sub_md_file.start(0)] + folder_file_lines[match_sub_md_file.end(0):]
        
        match_sub_md_file = re.search(sub_md_file_pattern, folder_file_lines)
    # 하위 Layer 0 제목 모두 없애기
    match_sub_md_file = re.search(sub_layer0_pattern, folder_file_lines)
    while match_sub_md_file != None:
        folder_file_lines = folder_file_lines[:match_sub_md_file.start(0)] + folder_file_lines[match_sub_md_file.end(0):]
        
        match_sub_md_file = re.search(sub_md_file_pattern, folder_file_lines)
        
    # * 하위 폴더, MD 파일 제목 파일 끝에 차례대로 삽입
    folder_file_lines = folder_file_lines + sub_directory_default_str + sub_md_file_default_str + sub_layer0_default_str
    
    # ! 개행 문자 변경
    # '\n{3,}'을 '\n\n'로 바꿈
    folder_file_lines = re.sub(r"\n{3,}", "\n\n", folder_file_lines)
    # '^\n{2}'를 '\n'로 바꿈
    folder_file_lines = re.sub(r"^\n{2}", "\n", folder_file_lines)
    
    # * 폴더 파일에 최신화된 파일 내용 저장
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
