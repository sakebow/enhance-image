# 图像增强

主要是将多个图片组合成一个大图片，适用于图片较小的情况，比如数字水印中的文字图片、一些自制的256x256的图片等。

# 功能

- [x] 对图片进行旋转
  - [x] 90度
  - [x] 180度
  - [x] 270度
- [x] 对图像进行翻转
  - [x] 水平翻转
  - [x] 垂直翻转
- [x] 对图像进行组合
  - [x] 随机抽取图片
  - [x] 组合为$n{\times}n$的正方形图片
  - [x] 可以指定$n$的大小
- [x] 对组合的图像进行增强
  - [x] 增加高斯噪声
  - [x] 修改图片亮度
- [x] 参数可配置
  - [x] 使用`yaml`文件参数配置参数
  - [x] 通过创建对象的时候传值进行初始化

# 使用

## 源码使用

```shell
$ pip install -r requirements.txt
$ python dataloader.py
```

## 安装包使用

```shell
$ pip install sakebow-enhancer
```

# 自定义

## 源码自定义

如果你需要修改源码以适配自己的工具，那就直接引用`dataloader.py`，并初始化`DataLoader`对象。

其中需要自定义的参数包括：

| 参数名 | 说明 |
| --- | --- |
| `yaml_path` | 配置文件所在目录，这里有一个默认的`default.yaml` |
| `size` | 图片预期大小，这里默认是320 |
| `batch` | 每次处理的图片数量，这里默认是4 |
| `deal` | 每次修改噪声、修改对比度的数量，这里默认是5 |
| `epoch` | 处理多少次，这里默认是1000 |
| `noise_upper` | 噪声最大值，这里默认是15 |
| `noise_lower` | 噪声最小值，这里默认是1 |
| `saturation_upper` | 修改亮度最大值，这里默认是100 |
| `saturation_lower` | 修改亮度最小值，这里默认是1 |

## 文件自定义

如果你需要修改配置文件，那就直接修改`default.yaml`文件。

最好是复制一份`default.yaml`，并命名为`my.yaml`或者什么的，并修改需要自定义的参数，然后在`dataloader.py`中传入你的配置文件路径即可。

## 最佳使用方式

目前虽然打成`sakebow-enhancer`包，但是目前只支持`Linux`系统，`Windows`系统下存在编码问题。

所以，最推荐的使用方式就是下载源码使用。需要如下组织源码的目录结构：

```txt
your_dataset_dir/
|
|- images/ # 图片所在目录
|  |- image1.jpg
|  |- ...
|- labels/ # 标签所在目录
|  |- label1.txt
|  |- ...
|- output/ # 输出目录
|  |- images/ # 输出图片所在目录（空文件夹）
|  |- labels/ # 输出标签所在目录（空文件夹）
|- my.yaml（或者default.yaml） # 配置文件
|- dataloader.py # 源码中的必要文件
|- reinforce.py # 源码中的必要文件
```

按照上述结构组织文件后，你可以直接编辑`my.yaml`文件，然后执行`python dataloader.py`即可。

又或者，你可以自行创建`my-runner.py`或者`my-runner.ipynb`文件。文件内容如下：

```python
import dataloader
"""
dataloader.DataLoader所有的参数都有默认值。
如果你保持`default.yaml`文件，那么你可以直接使用`myloader = dataloader.DataLoader()`。
如果你想要修改参数，你可以直接传入`myloader = dataloader.DataLoader(yaml_path = "my.yaml")`。
"""
myloader = dataloader.DataLoader(yaml_path = "my.yaml")
myloader.run_epochs()
```

执行就行了。其实不难发现，这段代码就是`dataloader.py`文件中的`main`函数内容。

所以，当你修改好了`default.yaml`文件后，你可以直接执行`python dataloader.py`


# 目前的Bug

- [ ] 不支持`Windows`系统中带有空格的文件路径
- [ ] 有待发现...