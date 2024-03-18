import cv2
import numpy as np

class ReinforceFactory:
  def __init__(self, image):
    self.image = image.copy()
  def add_noise(self, strength = 5e-2):
    # 添加随机噪声
    assert 0 <= strength <= 1
    row, col, ch = self.image.shape
    gauss = np.random.randn(row, col, ch)
    gauss = gauss.reshape(row, col, ch)
    noisy = self.image + self.image * gauss * strength  # 调整噪声强度
    self.image =  np.clip(noisy, 0, 255).astype(np.uint8)
    return self
  def adjust_colors(self, saturation = 15):
    # 饱和度在0到100之间
    assert 0 <= saturation <= 100
    # 调整色彩
    hsv = cv2.cvtColor(self.image, cv2.COLOR_BGR2HSV)
    hue, sat, val = cv2.split(hsv)
    sat = cv2.add(sat, saturation)  # 增加饱和度
    final_hsv = cv2.merge((hue, sat, val))
    self.image = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
    return self
  def build(self):
    return self.image
  