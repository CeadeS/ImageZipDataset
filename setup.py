from setuptools import setup, find_packages

setup(
    name='imagezipdataset',
    version='0.0.1',
    packages=find_packages(),
    url='https://github.com/CeadeS/ImageZipDataset',
    license='BSD-3-Clause License',
    author='Martin Hofmann',
    author_email='Martin.Hofmann@tu-ilmenau.de',
    description='Loading Images from Zipfiles Directly.',
    install_requires=[
       'numpy',
       'torch',
       'Pillow'
       ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX :: Linux',
        'Operating System :: Microsoft :: Windows :: Windows 10',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
)
