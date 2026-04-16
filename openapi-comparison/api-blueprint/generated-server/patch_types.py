import os
import re

SRC_DIR = "src"

def clean_pydantic_imports(match):
    import_list = match.group(1).split(",")
    clean_list = [imp.strip() for imp in import_list if imp.strip() not in ["int", "float", "str"]]
    if not clean_list:
        return "" 
    return f"from pydantic import {', '.join(clean_list)}"

def patch_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content
    content = re.sub(r'\bStrictInt\b', 'int', content)
    content = re.sub(r'\bStrictFloat\b', 'float', content)
    content = re.sub(r'\bStrictStr\b', 'str', content)
    content = content.replace("Union[float, int]", "float")
    content = re.sub(r'^from pydantic import (.*?)$', clean_pydantic_imports, content, flags=re.MULTILINE)

    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

def main():
    if not os.path.exists(SRC_DIR):
        print("Vui lòng chạy tại đường dẫn gốc chứa 'src'")
        return
    for root, _, files in os.walk(SRC_DIR):
        for file in files:
            if file.endswith('.py'):
                patch_file(os.path.join(root, file))
    print("✅ Đã vá lỗi StrictType thành công!")

if __name__ == "__main__":
    main()
