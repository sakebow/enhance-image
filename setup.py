from setuptools import find_packages, setup

setup(
    name='sakebow-enhancer',
    version="0.0.2",
    description='enhance datasets with rotate, flip and adjustion with color and noise',
    keywords='enhance datasets',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: Utilities',
    ],
    url='https://github.com/sakebow/enhance-image',
    author='sakebow',
    author_email='sakebowljx@gmail.com',
    python_requires='>=3.5',
    include_package_data=True,
    packages=find_packages(include=['src/dataloader.py', 'src/reinforce.py', 'src/__init__.py', 'src/default.yaml']),
    install_requires=['numpy', 'opencv-python', 'tqdm', 'PyYAML'],
    zip_safe=False)