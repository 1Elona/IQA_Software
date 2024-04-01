#Ex1
# PyInstaller 的 datas 选项在指定文件的移动路径时，只能识别和移动单个文件，而不能直接处理文件夹。为了打包整个文件夹和其子文件，你需要使用 Python 脚本来生成一个文件列表，然后将这个列表传递给 datas 选项。
#
# 以下是一个可以用来生成文件列表的 Python 脚本片段：

# import os
#
#
# # 获取文件夹中所有文件的绝对路径
# def get_all_files_in_directory(directory):
#     for foldername, subfolders, filenames in os.walk(directory):
#         for filename in filenames:
#             print(os.path.join(foldername, filename))
#             yield os.path.join(foldername, filename)
#
#
# # 文件夹路径
# directory = 'need'
#
# # 生成文件列表
# datas = [(f, os.path.relpath(f, directory)) for f in get_all_files_in_directory(directory)]
# 这个脚本首先定义了一个函数 get_all_files_in_directory ，用于遍历指定文件夹和其子文件夹，并返回所有文件的绝对路径。然后，脚本定义了一个文件夹路径（directory），并生成了一个文件列表（datas）。每个文件都有一个源路径（文件的绝对路径）和一个目标路径（文件相对于 directory 的相对路径）。
#
# 然后，你可以将这个文件列表传递给 datas 选项，例如：
#
# python
# Copy
# a = Analysis(['your_script.py'],
#              pathex=['/path/to/your/python/script'],
#              binaries=[],
#              datas=datas,
#              hiddenimports=[],
#              hookspath=[],
#              runtime_hooks=[],
#              excludes=[],
#              win_no_prefer_redirects=False,
#              win_private_assemblies=False,
#              cipher=block_cipher,
#              noarchive=False)
# 这样，当你运行
# PyInstaller
# 时，它会将指定文件夹中的所有文件打包到.app
# 的
# resources
# 文件夹中。
import os

# 获取文件夹及其子文件夹下的所有文件的路径
def get_all_files_in_directory(directory, relative_to):
    for foldername, _, filenames in os.walk(directory):
        for filename in filenames:
            absolute_path = os.path.join(foldername, filename)
            relative_path = os.path.relpath(absolute_path, relative_to)
            yield absolute_path, relative_path

# 文件夹路径
directories = ['img',  'need']

# 生成文件列表
datas = [(f, os.path.join('Contents/Resources', d)) for d in directories for f, r in get_all_files_in_directory(d, d)]
for i in datas:
    print(i)