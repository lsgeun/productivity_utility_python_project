# Note
## MD 파일
### 현재 경로의 MD 파일과 폴더를 찾아주는 쿼리 작성, 경로에 독립
[create_folder_file_and_insert_sub_folder_and_md_file_in_folder_file.py](create_folder_file_and_insert_sub_folder_and_md_file_in_folder_file.py)는 폴더 파일에 현재 경로의 MD 파일과 폴더를 찾아주는 Obsidian Dataview 플러그인의 쿼리를 작성한다. 경로가 바뀌더라도 기존의 쿼리를 그대로 사용할 수 있다.

### 사용하지 않는 파이썬 파일
#### tag와 TARGET DECK 작성
[insert_tag_target_deck.py](insert_tag_target_deck.py)는 MD 파일 내용의 맨 처음에 properties의 tag와 TARGET DECK 옵션을 넣는다.

#### 현재 경로의 MD 파일을 찾아주는 쿼리 작성, 경로에 의존
[update_current_md_file_in_file_folder.py](update_current_md_file_in_file_folder.py)는 폴더 파일에 현재 경로의 MD 파일을 찾아주는 Obsidian Dataview 플러그인의 쿼리를 작성한다. 이 쿼리는 폴더 파일의 경로가 바뀌면 다시 작성해야 한다. 이 경우에도 이 파이썬 파일을 이용하면 쿼리를 자동으로 다시 작성해준다.

하지만, [create_folder_file_and_insert_sub_folder_and_md_file_in_folder_file.py](create_folder_file_and_insert_sub_folder_and_md_file_in_folder_file.py)에서는 경로가 바뀌더라도 기존의 쿼리를 사용하면 된다.
