import sys
import tkinter
from tkinter import filedialog

# 英語表記の辞書を作成する関数
def load_english_names(filename):
    english_dict = {}
    with open(filename, encoding="utf-8") as f:
        section_found = (section_name == "")
        for line in f:
            line = line.strip()
            if line == section_name:
                section_found = True
                continue
            if section_found:
                if line.startswith("["):
                    break
                if "=" in line:
                    key, value = line.split("=", 1)
                    english_dict[key] = value
    return english_dict

# 書き換えする関数
def rewrite_file(input_file, english_dict):
    new_lines = []
    section_found = (section_name == "")
    with open(input_file, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line == section_name:
                section_found = True
                new_lines.append(line)
                continue
            if section_found:
                if line.startswith("["):
                    section_found = False
            if section_found and "=" in line:
                key, value = line.split("=", 1)
                english_name = english_dict.get(key)
                if english_name:
                    new_lines.append(f"{key}={value} ({english_name})")
                else:
                    new_lines.append(line)
            else:
                new_lines.append(line)

    # 書き出し
    with open(overwrite_file, "w", encoding="utf-8") as f:
        f.write("\n".join(new_lines) + "\n")



# ファイル名の指定
tkinter.Tk().withdraw()
# 英語のcfgを選択
english_file = filedialog.askopenfile().name
if english_file is None:
    sys.exit()
# 他言語のcfgを選択
overwrite_file = filedialog.askopenfile().name
if overwrite_file is None:
    sys.exit()

# セクション名。 MODでセクションがない場合は、[""]にする
section_names = ["[item-name]", "[entity-name]", "[equipment-name]", "[fluid-name]", "[fuel-category-name]", "[recipe-name]", "[asteroid-chunk-name]"]

for name in section_names:
    section_name = name
    # 実行処理
    english_dict = load_english_names(english_file)
    rewrite_file(overwrite_file, english_dict)

print(f"complete!")
