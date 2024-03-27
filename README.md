# 图像增强

重构了整个代码，在适配矩形框识别的基础上，支持了语义分割。

考虑使用难度，删除了依靠类创建图像增强工具包的方法，直接使用`yaml`文件构建工具包。（~~主要是参数太多了懒得写了~~）

重构后的代码主要适用于将多个图片组成一个大图片，适合图片中有一个部分是标签的情况，但并不适合整个图片作为一个标签的情况。

所以，适用于：

- [x] 遥感影像
- [x] 目标识别
- [x] 语义分割
- [ ] ......

但是目前并不适用于：

- [ ] 数字水印

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
$ python sakebow-enhancer.py
```

## ~~安装包使用（并不是Github最新版）~~

```shell
$ pip install sakebow-enhancer
```

# 自定义

## 目录结构

在执行之前，最好按照如下方式固定文件夹。

当然，如果你觉得你对你的相对路径能力具有绝对的自信，可以通过修改配置文件的方式解决。同样的，你对`Windows`的编码问题相当熟悉，也可以直接在配置文件中用`\\`代替`/`。

显然，我没有自信，所以我推荐大家这样组织目录结构：

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
|- my.yaml # 你的配置文件（可以没有）
"""下面都是必须存在的文件，当然也是源码默认附带的"""
|- default.yaml
|- datadealer.py
|- reinforce.py
|- sakebow-enhancer.py
|- sakebow-enhancer-cli.py
|- transform.py
|- validate.py
```

## ~~源码自定义（从0.2.0版本删除）~~

## 修改配置文件 + 修改代码入口

如果你需要修改配置文件，最好是复制一份`default.yaml`，并命名为`my.yaml`或者什么的，并修改需要自定义的参数，然后在`datadealer.py`中传入你的配置文件路径即可。

传入路径的方式就是修改`sakebow-enhancer.py`文件，修改最后一行里`run`方法的参数：

```python
run(yaml_path="my.yaml")
```

然后直接运行`sakebow-enhancer.py`文件：

```shell
$ python sakebow-enhancer.py
```

## 修改配置文件 + 命令行直接完成

当然，我也明白有些人对命令行的执着。所以我也给了一个方案。

首先修改你的`default.yaml`文件，然后执行如下命令：

```shell
$ python sakebow-enhancer-cli.py --yaml=my.yaml
```

## 仅修改配置文件

其实不难发现，`datadealer.py`文件中的`main`函数内容也具备执行的能力。所以，还有一种非常直接的方式：直接修改`default.yaml`文件。修改好了之后，我们就直接执行：

```shell
$ python datadealer.py
```

# 目前的Bug

- [ ] 不支持`Windows`系统中带有空格的文件路径
- [ ] 有待发现...