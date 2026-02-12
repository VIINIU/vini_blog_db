import os

def rename_files_mac(target_directory, old_text, new_text):
    # 폴더 존재 여부 확인
    if not os.path.exists(target_directory):
        print(f"경로를 찾을 수 없습니다: {target_directory}")
        return

    # 숨김 파일(예: .DS_Store)은 제외하고 목록 가져오기
    files = [f for f in os.listdir(target_directory) if not f.startswith('.')]
    count = 0

    for filename in files:
        if old_text in filename:
            new_filename = filename.replace(old_text, new_text)
            
            old_path = os.path.join(target_directory, filename)
            new_path = os.path.join(target_directory, new_filename)

            try:
                os.rename(old_path, new_path)
                print(f"✅ 변경: {filename} ➔ {new_filename}")
                count += 1
            except Exception as e:
                print(f"❌ 오류 발생 ({filename}): {e}")

    print(f"\n--- 총 {count}개의 파일명이 변경되었습니다. ---")

# --- macOS 설정 예시 ---
# 팁: 터미널에서 폴더를 드래그해서 이 위치에 놓으면 경로가 자동으로 입력됩니다.
target_dir = '/Users/viniu/vini_dir/vini_blog_db/images/verilog_study' 
search_for = 'image '
replace_with = 'image'

rename_files_mac(target_dir, search_for, replace_with)