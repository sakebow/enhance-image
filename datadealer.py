import os, cv2, yaml, math
import numpy as np
from tabulate import tabulate

from validate import check_folder
from transform import Transform, DetectTransform, SegementTransform
from reinforce import ReinforceFactory

class DataDealer:
  def __init__(self, yaml_path = './default.yaml'):
    """
    @function: data loader
    @param
    str - yaml_path - relative path of yaml file
    int - size - target size of image
    batch - a batch of images
    deal - add noise and adjust color times
    epoch - times to run
    """
    self.base_path, self.type, self.transform = os.getcwd(), None, None
    self.size, self.batch, self.deal, self.epoch, self.reinforce = 0, 0, 0, 0, None
    self.noise_upper, self.noise_lower, self.saturation_upper, self.saturation_lower = 0, 0, 0, 0
    if os.path.exists(yaml_path):
      self.init_with_yaml(yaml_path)
    else:
      self.init_with_yaml('default.yaml')
    self.init_transform()
  def init_transform(self) -> Transform:
    self.transform = (
      SegementTransform(self.square_size, self.size)
      if self.type == 'segment' else DetectTransform(self.square_size, self.size)
    )
  def init_with_yaml(self, yaml_path):
    data = self.yaml_reader(yaml_path)
    self.base_path = os.path.dirname(os.path.abspath(yaml_path))
    self.size = data['config']['size']
    self.batch = data['config']['batch']
    assert math.sqrt(data['config']['batch']).is_integer(), "batch must can be square"
    self.square_size = math.floor(math.sqrt(data['config']['batch']))
    self.epoch = data['config']['epoch']
    self.deal = data['config']['deal']
    self.type = data['config']['type']
    noise_type = data['config']['noise_type']
    noises = data['noise']
    noise_item = list(filter(lambda x: x['type'] == noise_type, noises))[0]
    self.noise_upper = noise_item['upper']
    self.noise_lower = noise_item['lower']
    self.saturation_upper = data['saturation']['upper']
    self.saturation_lower = data['saturation']['lower']
    self.operations = data['operations']
    self.input_image_path = data['input']['image']
    self.input_label_path = data['input']['label']
    self.output_image_path = data['output']['image']
    self.output_label_path = data['output']['label']
  def yaml_reader(self, yaml_path):
    """
    @function: read yaml files
    @param
    str - yaml_path - relative path of yaml file
    @return
    dict - yaml data - a dict of config
    """
    yaml_path = os.path.join(self.base_path, yaml_path)
    with open(yaml_path, "r") as file:
      data = yaml.load(file, Loader = yaml.FullLoader)
    return data
  def get_size(self):
    return self.size
  def get_batch(self):
    return self.batch
  def get_square_size(self):
    return self.square_size
  def get_operations(self):
    return self.operations
  def get_epoch(self):
    return self.epoch
  def get_files_in_directory(self, directory, extension: list):
    """
    read files in directory with extensions in extension list
    """
    results = []
    for i in range(len(extension)):
      results += [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith(extension[i])]
    return results
  def get_input_image_path(self):
    return os.path.join(self.base_path, self.input_image_path)
  def image_info(self):
    """
    @function: get image size info
    @return: dict of width, height and area
    """
    image_paths = self.get_files_in_directory(
      directory = self.get_input_image_path(), extension = ['.jpg', '.png', '.jpeg', '.JPG', '.PNG', '.JPEG']
    )
    widths, heights, areas = [], [], []
    for f in image_paths:
      image = cv2.imread(f)
      widths.append(image.shape[1])
      heights.append(image.shape[0])
      areas.append(image.shape[1] * image.shape[0])
    # 输出到命令行，默认会自适应列宽
    print(tabulate([
        ["", "宽", "高", "面积"],
        ["最大", max(widths), max(heights), max(areas)],
        ["平均", sum(widths) / len(widths), sum(heights) / len(heights), sum(areas) / len(areas)],
        ["最小", min(widths), min(heights), min(areas)]
    ], headers="firstrow"))
    return {
      "max_width": max(widths), "avg_width": sum(widths) / len(widths), "min_width": min(widths),
      "max_height": max(heights), "avg_height": sum(heights) / len(heights), "min_height": min(heights),
      "max_area": max(areas), "avg_area": sum(areas) / len(areas), "min_area": min(areas)
    }
  def get_input_label_path(self):
    return os.path.join(self.base_path, self.input_label_path)
  def label_info(self):
    """
    @function: get label count info
    @return: dict of count
    """
    count = 0
    # go through label_directory
    if self.check_type():
      for f in self.get_files_in_directory(directory = self.get_input_label_path(), extension = ['.txt']):
        with open(f, 'r') as file:
          for _ in file:
            count += 1
    else:
      count = -1
    print(f"==> label_count: {count}")
    return { "count": count, "type": self.type }
  
  def check_type(self):
    """
    @function: check label format if it is segment or detect
    @return: True if check equals input, else False
    """
    detected_type, consist = None, True
    try:
      # to detect if the label_directory is legal
      detected_type = 'segment' if check_folder(self.get_input_label_path()) < 0 else 'detect'
      if detected_type != self.type:
        raise TypeError
    except ValueError:
      consist = False
      print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
      print("@  Warning: Your Data is not in the right format.  @")
      print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    except TypeError:
      consist = False
      print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
      print("@    Warning: Your Data is not for current use.    @")
      print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
      print("==> Current Use: {}, please check.".format(self.type))
    except Exception:
      consist = False
      print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
      print("@ Warning: code error, call Administrator for help @")
      print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    finally:
      if consist:
        print("@@@@@@@@@@@@@")
        print("@ Good Try! @")
        print("@@@@@@@@@@@@@")
    return consist
  
  def get_output_image_path(self):
    return os.path.join(self.base_path, self.output_image_path)
  def get_output_label_path(self):
    return os.path.join(self.base_path, self.output_label_path)
  def load_image(self, image_path):
    """
    read single image and its label
    """
    label_path = os.path.basename(image_path).split(".")[0]
    label_path = os.path.join(self.get_input_label_path(), label_path + ".txt")
    image_path = os.path.join(self.get_input_image_path(), image_path)
    labels = []
    with open(label_path, "r") as file:
      for line in file:
        parts = line.split()
        labels.append([int(parts[0])] + [float(x) for x in parts[1:]])
    image = cv2.imread(image_path)
    return image, labels
  def random_deal_images(self, image, rand = True):
    if self.deal > 0 and rand:
      strength = np.random.choice([i / 100 for i in range(16)], size = self.deal, replace = False)
      saturation = np.random.choice([i for i in range(101)], size = self.deal, replace = False)
      return ReinforceFactory(image).add_noise(strength).adjust_colors(saturation).build()
    else:
      return ReinforceFactory(image).add_noise().adjust_colors().build()
  def random_choose_images(self, image_folder_path):
    """
    @function: random choose images for a batch
    @param
        str - image_folder_path - a folder path of images
        int - num - number of images - **should be a square**
    @return
    """
    assert isinstance(image_folder_path, str), "image_folder_path should be a str"
    assert os.path.exists(image_folder_path), "image_folder_path should be a valid path"
    positions = range(self.batch) # index of a square container
    image_paths = self.get_files_in_directory(
      directory = image_folder_path, extension = ['.jpg', '.png', '.jpeg', '.JPG', '.PNG', '.JPEG']
    )
    image_paths = np.random.choice(image_paths, self.batch)
    operations = np.random.choice(self.get_operations(), self.batch)
    images = np.zeros((self.square_size * self.size , self.square_size * self.size, 3), dtype=np.uint8)
    labels = []
    for image_path, position, operation in zip(image_paths, positions, operations):
      image, label = self.load_image(image_path)
      image, label = self.transform.transform_image_and_labels(image, label, operation)
      images[
        math.floor(position / self.square_size) * self.size : (math.floor(position / self.square_size) + 1) * self.size,
        (position % self.square_size) * self.size : ((position % self.square_size) + 1) * self.size
      ] = self.random_deal_images(image)
      label = self.transform.place_label_item(label, position)
      labels.append(label)
    return images, labels
  def save_transforms(self, idx, transformed_image, transformed_labels):
    # 保存调整后的图像
    cv2.imwrite(os.path.join(self.get_output_image_path(), f'image_{idx}.jpg'), transformed_image)
    # 保存调整后的标签
    with open(os.path.join(self.get_output_label_path(), f'image_{idx}.txt'), 'w') as label_file:
      for batch in transformed_labels:
        for labels in batch:
          label_file.write(' '.join([str(label) for label in labels]) + '\n')
  
if __name__ == "__main__":
  my_data = DataDealer()
  for epoch in range(my_data.get_epoch()):
    image, label = my_data.random_choose_images(my_data.get_input_image_path())
    my_data.save_transforms(idx = epoch, transformed_image = image, transformed_labels = label)