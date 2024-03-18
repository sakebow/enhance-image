import os, cv2, yaml, math
import numpy as np
from tqdm import trange

from reinforce import ReinforceFactory

class DataLoader:
    def __init__(self, yaml_path = './default.yaml', size = 320, batch = 4, deal = 5, epoch = 1000, noise_upper = 15,
                 noise_lower = 1, saturation_upper = 100, saturation_lower = 1):
        """
        @function: data loader
        @param
        str - yaml_path - relative path of yaml file
        int - size - target size of image
        batch - a batch of images
        deal - add noise and adjust color times
        epoch - times to run
        """
        self.data = None
        self.base_path = os.getcwd()
        self.size, self.batch, self.deal, self.epoch = 0, 0, 0, 0
        self.noise_upper, self.noise_lower, self.saturation_upper, self.saturation_lower = 0, 0, 0, 0
        if not os.path.exists(yaml_path):
            assert 0 <= noise_lower < noise_upper <= 100 and 0 <= saturation_lower < saturation_upper <= 100
            self.size = size
            self.batch = batch
            self.deal = deal
            self.epoch = epoch
            self.noise_upper = noise_upper
            self.noise_lower = noise_lower
            self.saturation_upper = saturation_upper
            self.saturation_lower = saturation_lower
        else:
            self.data = self.yaml_reader(yaml_path)
            print(self.data)
            self.base_path = os.path.dirname(os.path.abspath(yaml_path))
            self.size = self.data['config']['size']
            self.batch = self.data['config']['batch']
            self.epoch = self.data['config']['epoch']
            self.deal = self.data['config']['deal']
            self.noise_upper = self.data['config']['noise']['upper']
            self.noise_lower = self.data['config']['noise']['lower']
            self.saturation_upper = self.data['config']['saturation']['upper']
            self.saturation_lower = self.data['config']['saturation']['lower']

        
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
        return self.data["size"]
    def get_batch(self):
        return self.data["batch"]
    def get_operation(self):
        return self.data["operations"]
    def get_files_in_directory(self, directory, extension: list):
        """
        read files in directory with extensions in extension list
        """
        results = []
        for i in range(len(extension)):
            results += [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith(extension[i])]
        return results
    def get_input_image_path(self):
        return os.path.join(self.base_path, self.data["input"]["image"])
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
        return {
            "max_width": max(widths), "avg_width": sum(widths) / len(widths), "min_width": min(widths),
            "max_height": max(heights), "avg_height": sum(heights) / len(heights), "min_height": min(heights),
            "max_area": max(areas), "avg_area": sum(areas) / len(areas), "min_area": min(areas)
        }
    def get_input_label_path(self):
        return os.path.join(self.base_path, self.data["input"]["label"])
    def label_info(self):
        """
        @function: get label count info
        @return: dict of count
        """
        label_directory = self.get_files_in_directory(
            directory = self.get_input_label_path(), extension = ['.txt']
        )
        count = 0
        for f in os.listdir(label_directory):
            with open(f, "r") as file:
                for _ in file:
                    count += 1
        return { "label_count": count }
    def get_output_image_path(self):
        return os.path.join(self.base_path, self.data["output"]["image"])
    def get_output_label_path(self):
        return os.path.join(self.base_path, self.data["output"]["label"])
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
    def random_choose_images(self, image_folder_path):
        """
        @function: random choose images for a batch
        @param
            str - image_folder_path - a folder path of images
            int - num - number of images - **should be a square**
        @return
        """
        assert isinstance(image_folder_path, str)
        assert os.path.exists(image_folder_path)
        square_size = math.sqrt(self.batch)
        assert square_size.is_integer()
        square_size = int(square_size)
        positions = range(self.batch) # index of a square container
        image_paths = self.get_files_in_directory(
            directory = image_folder_path, extension = ['.jpg', '.png', '.jpeg', '.JPG', '.PNG', '.JPEG']
        )
        image_paths = np.random.choice(image_paths, self.batch)
        operations = np.random.choice(self.get_operation(), self.batch)
        images = np.zeros((square_size * self.size , square_size * self.size, 3), dtype=np.uint8)
        labels = []
        for image_path, position, operation in zip(image_paths, positions, operations):
            image, label = self.load_image(image_path)
            image, label = self.transform_image_and_labels(image, label, operation, square_size, (self.size, self.size))
            images[
                math.floor(position / square_size) * self.size : (math.floor(position / square_size) + 1) * self.size,
                (position % square_size) * self.size : ((position % square_size) + 1) * self.size
            ] = image
            label = self.place_label_item(label, square_size, position)
            labels.append(label)
        return images, labels

    def transform_image_and_labels(self, image, labels, operation, square_size, target_size = (320, 320)):
        """根据指定的操作对图像和标签进行变换"""
        assert operation in ['rotate_90', 'rotate_180', 'rotate_270', 'flip_x', 'flip_y']
        assert len(target_size) == 2 and isinstance(target_size[0], int) and isinstance(target_size[1], int)
        assert (
            isinstance(target_size, list) or
            isinstance(target_size, tuple) or
            (isinstance(target_size, np.ndarray) and len(target_size.shape) == 1)
        )
        transformed_image, transformed_labels = None, None
        image = cv2.resize(image, target_size)
        if operation == 'rotate_90':
            # 旋转90度
            transformed_image = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
            transformed_labels = [
                [label[0], 1 - label[2], label[1], label[4] / square_size, label[3] / square_size]
                for label in labels]
        elif operation == 'rotate_180':
            # 旋转180度
            transformed_image = cv2.rotate(image, cv2.ROTATE_180)
            transformed_labels = [
                [label[0], 1 - label[1], 1 - label[2], label[3] / square_size, label[4] / square_size]
                for label in labels
            ]
        elif operation == 'rotate_270':
            # 旋转270度
            transformed_image = cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)
            transformed_labels = [
                [label[0], label[2], 1 - label[1], label[4] / square_size, label[3] / square_size]
                for label in labels
            ]
        elif operation == 'flip_x':
            # X轴翻转
            transformed_image = cv2.flip(image, 0)
            transformed_labels = [
                [label[0], label[1], 1 - label[2], label[3] / square_size, label[4] / square_size]
                for label in labels
            ]
        elif operation == 'flip_y':
            # Y轴翻转
            transformed_image = cv2.flip(image, 1)
            transformed_labels = [
                [label[0], 1 - label[1], label[2], label[3] / square_size, label[4] / square_size]
                for label in labels
            ]
        return transformed_image, transformed_labels
    
    def place_label_item(self, label, square_size, position_idx):
        assert 0 <= position_idx < square_size ** 2
        new_label = []
        for rect in label:
            cls, x, y, w, h = rect
            x = (position_idx % square_size + x) / square_size
            y = (math.floor(position_idx / square_size) + y) / square_size
            new_label.append([cls, x, y, w, h])
        return new_label
    
    def reinforce_image(self, image, noise = 5e-2, saturation = 15):
        reinforce_factory = ReinforceFactory(image)
        return reinforce_factory.add_noise(noise).adjust_colors(saturation).build()

    def save_transform(self, idx, transformed_image, transformed_labels):
        # 保存调整后的图像
        cv2.imwrite(os.path.join(self.get_output_image_path(), f'image_{idx}.jpg'), transformed_image)
        # 保存调整后的标签
        with open(os.path.join(self.get_output_label_path(), f'image_{idx}.txt'), 'w') as label_file:
            for batch in transformed_labels:
                for labels in batch:
                    label_file.write(' '.join([str(label) for label in labels]) + '\n')
    
    def run_epochs(self):
        noise_strengths = np.random.choice([i / 100. for i in range(self.noise_lower, self.noise_upper)], self.deal)
        saturations = np.random.choice([i * 1. for i in range(self.saturation_lower, self.saturation_upper)], self.deal)
        for epoch in trange(self.epoch):
            for noise, saturation in zip(noise_strengths, saturations):
                image, label = self.random_choose_images(self.get_input_image_path())
                self.save_transform(
                    f"{epoch}_{noise}_{saturation}", self.reinforce_image(image, noise=noise, saturation=saturation), label
                )

if __name__ == '__main__':
    dataLoader = DataLoader(
        yaml_path = "default.yaml"
    )
    dataLoader.run_epochs()