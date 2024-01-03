import re
import os

vault_directory = "/Users/isgeun/Library/Mobile Documents/iCloud~md~obsidian/Documents/NOTE-iCloud_Drive"

# Layer 0 File 종류
layer0_suffix = ["웹 클립", "유튜브", "웹 문서"]
# Layer 0의 MD 파일을 찾는 Dataview 정규식
layer0_regex_in_dataview = "";
layer0_regex_in_dataview += ".* - ("
for i, _ in enumerate(layer0_suffix):       
    layer0_regex_in_dataview += _
    if i != len(layer0_suffix) - 1:
        layer0_regex_in_dataview += '|'
layer0_regex_in_dataview += ")$"

# 디렉토리 파일('0 '으로 시작하는 MD 파일)을 찾을 디렉토리들을 저장하는 스택
directory_paths = [vault_directory]
while not (directory_paths == []):
    # 현재 디렉토리 파일을 찾고자하는 디렉토리
    current_directory_path = directory_paths.pop()
    
    # * 디렉토리 파일 생성
    # "0 Inbox"에서 "0 "와 같은 순서를 뺀 디렉토리 이름
    current_directory_name_without_order = re.sub(r"^\d+? ", "", os.path.basename(current_directory_path))
    directory_file = f"{current_directory_path}/0 {current_directory_name_without_order}.md"
    # 디렉토리 파일 생성(있다면 그대로 놔두고, 없다면 새로 생성)
    os.system(f"touch \"{directory_file}\"")

    # * 디렉토리 파일을 문자열로 불러옴
    directory_file_lines = None
    # 파일 내용을 문자열로 불러오기
    with open(directory_file, "r") as f:
        directory_file_lines = f.readlines(); directory_file_lines = "".join(directory_file_lines)
    
    # * 디렉토리 파일에 아이콘 넣기
    # 디렉토리 파일 아이콘 문자열
    directory_file_icon_str = ""
    # properties pattern
    properties_pattern = re.compile(r"\A(---\n(?:.+?\n)+?)(---)")
    # properties_match
    properties_match = properties_pattern.search(directory_file_lines)
    # 디렉토리 파일에 아이콘 추가하기
    ## * properties가 없다면 properties를 만들고 아이콘 추가
    if properties_match == None:
        if directory_file_icon_str == "":
            pass
        else:
            directory_file_lines = f"---\nicon: {directory_file_icon_str}\n---\n" + directory_file_lines
    ## * properties가 있을 때, 기존 property들을 유지한 채 icon property가 없다면  icon property를 추가, icon property가 있다면 icon property를 변경
    else:
        # properties 문자열
        properties = properties_match.group(0)
        # icon property pattern
        icon_property_pattern = re.compile(r"icon: (.+?)(?=\n)")
        # icon property match
        icon_property_match = icon_property_pattern.search(properties)
        # icon property가 없다면 icon property를 추가
        if icon_property_match == None:
            if directory_file_icon_str == "":
                pass
            else:
                directory_file_lines = directory_file_lines[:properties_match.end(1)] + f"icon: {directory_file_icon_str}\n" + directory_file_lines[properties_match.start(2):]
        # icon property가 있다면 icon property를 변경
        else:
            if directory_file_icon_str == "":
                directory_file_lines = directory_file_lines[:properties_match.start(0) + icon_property_match.start(0)] + directory_file_lines[properties_match.start(0) + icon_property_match.end(0)+1:]
            else:
                directory_file_lines = directory_file_lines[:properties_match.start(0) + icon_property_match.start(1)] + f"{directory_file_icon_str}" + directory_file_lines[properties_match.start(0) + icon_property_match.end(1):]

    # * 하위 디렉토리, MD 파일 제목 기본 문자열
    # 디렉토리 파일에서 Directory heading default string
    sub_directory_default_str = "\n# Directory\n```dataview\nTABLE file.mday as 수정일, file.cday as 생성일, file.size as \"파일 크기\"\nWHERE\n\tlength(split(regexreplace(replace(file.folder, this.file.folder, \"\"), \"^/\", \"\"),  \"/\")) = 1\n\tAND replace(file.folder, this.file.folder, \"\") != \"\"\n\tAND startswith(file.name, \"0 \")\n\tAND startswith(file.folder, this.file.folder)\n\tAND file.name != this.file.name\nSORT file.name ASC\n```\n"
    # 디렉토리 파일에서 MD File heading default string
    sub_md_file_default_str = f"\n# MD File\n```dataview\nTABLE file.mday as 수정일, file.cday as 생성일, file.size as \"파일 크기\"\nWHERE\n\tfile.folder = this.file.folder\n\tAND file.name != this.file.name\n\tAND !regexmatch(\"{layer0_regex_in_dataview}\", file.name)\nSORT file.mday DESC\n```\n"
    # 디렉토리 파일에서 Layer 0 File heading default string
    sub_layer0_default_str = f"\n# Layer 0 File\n```dataview\nTABLE file.mday as 수정일, file.cday as 생성일, file.size as \"파일 크기\"\nWHERE\n\tfile.folder = this.file.folder\n\tAND file.name != this.file.name\n\tAND regexmatch(\"{layer0_regex_in_dataview}\", file.name)\nSORT file.mday DESC\n```\n"
    
    # * 하위 디렉토리, MD 파일 제목 정규식 패턴
    # Directory heading regex pattern
    sub_directory_pattern = re.compile(r"^# Directory\n```dataview\n(.*?\n)*?```", re.MULTILINE)
    # MD File heading regex pattern
    sub_md_file_pattern = re.compile(r"^# MD File\n```dataview\n(.*?\n)*?```", re.MULTILINE)
    # Layer 0 File heading regex pattern
    sub_layer0_pattern = re.compile(r"^# Layer 0 File\n```dataview\n(.*?\n)*?```", re.MULTILINE)
    
    # * 하위 디렉토리, MD 파일 제목 모두 없애기
    # 하위 디렉토리 제목 모두 없애기
    match_sub_directory = re.search(sub_directory_pattern, directory_file_lines)
    while match_sub_directory != None:
        directory_file_lines = directory_file_lines[:match_sub_directory.start(0)] + directory_file_lines[match_sub_directory.end(0):]
        
        match_sub_directory = re.search(sub_directory_pattern, directory_file_lines)
    # 하위 MD 파일 제목 모두 없애기
    match_sub_md_file = re.search(sub_md_file_pattern, directory_file_lines)
    while match_sub_md_file != None:
        directory_file_lines = directory_file_lines[:match_sub_md_file.start(0)] + directory_file_lines[match_sub_md_file.end(0):]
        
        match_sub_md_file = re.search(sub_md_file_pattern, directory_file_lines)
    # 하위 Layer 0 File 제목 모두 없애기
    match_sub_md_file = re.search(sub_layer0_pattern, directory_file_lines)
    while match_sub_md_file != None:
        directory_file_lines = directory_file_lines[:match_sub_md_file.start(0)] + directory_file_lines[match_sub_md_file.end(0):]
        
        match_sub_md_file = re.search(sub_md_file_pattern, directory_file_lines)
        
    # * 하위 디렉토리, MD 파일 제목 파일 끝에 차례대로 삽입
    directory_file_lines = directory_file_lines + sub_directory_default_str + sub_md_file_default_str + sub_layer0_default_str
    
    # * 개행 문자 변경
    # '\n{3,}'을 '\n\n'로 바꿈
    directory_file_lines = re.sub(r"\n{3,}", "\n\n", directory_file_lines)
    # '^\n{2}'를 '\n'로 바꿈
    directory_file_lines = re.sub(r"^\n{2}", "\n", directory_file_lines)
    
    # * 디렉토리 파일에 최신화된 파일 내용 저장
    with open(directory_file, "w") as f:
        f.writelines(directory_file_lines)
    
    # * 다음 탐색할 디렉토리 directory_paths에 append
    # 현재 디렉토리에 있는 하위 파일 및 디렉토리
    current_sub_names = os.listdir(current_directory_path)
    # 현재 디렉토리에 있는 하위 디렉토리
    current_sub_directory_names = [_ for _ in current_sub_names if os.path.isdir(f"{current_directory_path}/{_}")]
    # "0 Attachment"를 제외한 현재 디렉토리에 있는 숨겨지지 않은 하위 디렉토리
    current_sub_directory_names_without_hidden = [_ for _ in current_sub_directory_names if _.find(".") == -1]; current_sub_directory_names_without_hidden = [_ for _ in current_sub_directory_names_without_hidden if _ != "0 Attachment"]
    # directory_paths에 현재 디렉토리의 하위 디렉토리(current_sub_directory_names_without_hidden) 모두 넣음
    for _ in current_sub_directory_names_without_hidden:
        directory_paths.append(f"{current_directory_path}/{_}")
