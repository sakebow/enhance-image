import cv2, math
from abc import ABC, abstractmethod

class Transform(ABC):
  def __init__(self) -> None:
    super().__init__()
  @abstractmethod
  def transform_image_and_labels(self):
    ...
  @abstractmethod
  def place_label_item(self):
    ...

class SegementTransform(Transform):
  def __init__(self, square_size = 2, target_size = 320):
    super().__init__()
    self.target_size = (target_size, target_size)
    self.square_size = square_size
  def transform_image_and_labels(self, image, labels, operation):
    """根据指定的操作对图像和标签进行变换"""
    transformed_image, transformed_labels = None, None
    image = cv2.resize(image, self.target_size)
    if operation == 'rotate_90':
      # 旋转90度
      transformed_image = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
      transformed_labels = [
        [label[0]] + [label[index - 1] if index % 2 == 0 else 1 - label[index + 1] for index in range(1, len(label))]
        for label in labels]
    elif operation == 'rotate_180':
      # 旋转180度
      transformed_image = cv2.rotate(image, cv2.ROTATE_180)
      transformed_labels = [
        [label[0]] + [1 - label[index] for index in range(1, len(label))]
        for label in labels]
    elif operation == 'rotate_270':
      # 旋转270度
      transformed_image = cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)
      transformed_labels = [
        [label[0]] + [1 - label[index - 1] if index % 2 == 0 else label[index + 1] for index in range(1, len(label))]
        for label in labels]
    elif operation == 'flip_x':
      # X轴翻转
      transformed_image = cv2.flip(image, 0)
      transformed_labels = [
        [label[0]] + [1 - label[index] if index % 2 == 0 else label[index] for index in range(1, len(label))]
        for label in labels]
    elif operation == 'flip_y':
      # Y轴翻转
      transformed_image = cv2.flip(image, 1)
      transformed_labels = [
        [label[0]] + [label[index] if index % 2 == 0 else 1 - label[index] for index in range(1, len(label))]
        for label in labels]
    return transformed_image, transformed_labels
  def place_label_item(self, label, position_idx):
    assert 0 <= position_idx < self.square_size ** 2, "position_idx must be in range [0, square_size ** 2)"
    new_label = []
    for rect in label:
      new_label_item = rect.copy()
      for index in range(1, len(rect)):
        if not (index % 2 == 0):
          new_label_item[index] = (new_label_item[index] + position_idx % self.square_size) / self.square_size
        else:
          new_label_item[index] = (new_label_item[index] + math.floor(position_idx / self.square_size)) / self.square_size
      new_label.append(new_label_item)
    return new_label

class DetectTransform(Transform):
  def __init__(self, square_size = 2, target_size = 320):
    super().__init__()
    self.square_size = square_size
    self.target_size = (target_size, target_size)
  def transform_image_and_labels(self, image, labels, operation):
    """根据指定的操作对图像和标签进行变换"""
    transformed_image, transformed_labels = None, None
    image = cv2.resize(image, self.target_size)
    if operation == 'rotate_90':
      # 旋转90度
      transformed_image = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
      transformed_labels = [
        [label[0], 1 - label[2], label[1], label[4] / self.square_size, label[3] / self.square_size]
        for label in labels]
    elif operation == 'rotate_180':
      # 旋转180度
      transformed_image = cv2.rotate(image, cv2.ROTATE_180)
      transformed_labels = [
        [label[0], 1 - label[1], 1 - label[2], label[3] / self.square_size, label[4] / self.square_size]
        for label in labels
      ]
    elif operation == 'rotate_270':
      # 旋转270度
      transformed_image = cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)
      transformed_labels = [
        [label[0], label[2], 1 - label[1], label[4] / self.square_size, label[3] / self.square_size]
        for label in labels
      ]
    elif operation == 'flip_x':
      # X轴翻转
      transformed_image = cv2.flip(image, 0)
      transformed_labels = [
        [label[0], label[1], 1 - label[2], label[3] / self.square_size, label[4] / self.square_size]
        for label in labels
      ]
    elif operation == 'flip_y':
      # Y轴翻转
      transformed_image = cv2.flip(image, 1)
      transformed_labels = [
        [label[0], 1 - label[1], label[2], label[3] / self.square_size, label[4] / self.square_size]
        for label in labels
      ]
    return transformed_image, transformed_labels
  def place_label_item(self, label, position_idx):
    assert 0 <= position_idx < self.square_size ** 2, "position_idx must be in range [0, square_size ** 2)"
    new_label = []
    for rect in label:
      cls, x, y, w, h = rect
      x = (position_idx % self.square_size + x) / self.square_size
      y = (math.floor(position_idx / self.square_size) + y) / self.square_size
      new_label.append([cls, x, y, w, h])
    return new_label