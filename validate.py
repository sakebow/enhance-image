import glob, os, re

# 检查一行是否只包含6个整数或小数
def check_line_format(line):
  # 使用正则表达式匹配整数或小数
  pattern = re.compile(r'^\s*(-?\d+(\.\d+)?\s+){4}-?\d+(\.\d+)?\s*$')
  return bool(pattern.match(line))

# 检查文件是否符合条件
def check_file(file_path):
  with open(file_path, 'r') as file:
    for line in file:  # 检查每一行
      if not check_line_format(line):
        return -1  # 如果行包含非数字字符
  return 1  # 文件满足条件

# 检查文件夹下的所有txt文件
def check_folder(folder_path):
  # 获取文件夹中所有的.txt文件
  txt_files = glob.glob(os.path.join(folder_path, '*.txt'))
  for file_path in txt_files:
    result = check_file(file_path)
    if result != 1:
      return -1  # 如果发现不符合条件的文件，立即返回
  return 1  # 所有文件都符合条件

if __name__ == '__main__':
  # 设置文件夹路径
  folder_path = '/path/to/your/folder'

  # 执行检查并输出结果
  result = check_folder(folder_path)
  print(result)
