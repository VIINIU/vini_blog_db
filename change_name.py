import os

def rename_extensions_to_png(target_directory):
    # 폴더 존재 여부 확인
    if not os.path.exists(target_directory):
        print(f"경로를 찾을 수 없습니다: {target_directory}")
        return

    # 변경 대상 확장자 (대소문자 구분 없이 처리하기 위해 소문자로 정의)
    target_extensions = ('.jpeg', '.jpg')
    count = 0

    # 숨김 파일 제외하고 목록 가져오기
    files = [f for f in os.listdir(target_directory) if not f.startswith('.')]

    for filename in files:
        # 파일명과 확장자 분리
        name, ext = os.path.splitext(filename)
        
        # 확장자가 .jpeg 또는 .jpg인지 확인 (소문자로 변환하여 비교)
        if ext.lower() in target_extensions:
            # 새로운 파일명 생성 (.png로 고정)
            new_filename = name + ".png"
            
            old_path = os.path.join(target_directory, filename)
            new_path = os.path.join(target_directory, new_filename)

            try:
                # 동일한 이름의 png 파일이 이미 존재하는지 확인 로직을 추가할 수 있으나, 여기서는 덮어쓰기/변경을 수행합니다.
                os.rename(old_path, new_path)
                print(f"✅ 변경: {filename} ➔ {new_filename}")
                count += 1
            except Exception as e:
                print(f"❌ 오류 발생 ({filename}): {e}")

    print(f"\n--- 총 {count}개의 파일 확장자가 .png로 변경되었습니다. ---")

# --- 설정 및 실행 ---
# Canvas 보고서용 이미지 경로를 그대로 유지합니다.
target_dir = '/Users/viniu/vini_dir/vini_blog_db/images/telechips_internship' 

rename_extensions_to_png(target_dir)