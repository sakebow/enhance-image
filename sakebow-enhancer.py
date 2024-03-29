from tqdm import trange
from datadealer import DataDealer
def run(yaml_path = './default.yaml'):
  my_data = DataDealer(yaml_path=yaml_path)
  for epoch in trange(my_data.get_epoch()):
    image, label = my_data.random_choose_images(my_data.get_input_image_path())
    my_data.save_transforms(idx = epoch, transformed_image = image, transformed_labels = label)

run(yaml_path='./default.yaml')