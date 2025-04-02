from setuptools import setup, find_packages

setup(
    name='ErisPulse',
    version='1.0.4',
    author='艾莉丝·格雷拉特(WSu2059)',
    author_email='wsu2059@qq.com',
    maintainer='runoneall',
    maintainer_email='runoobsteve@gmail.com',
    description='ErisPulse 是一个模块化、可扩展的异步 Python SDK 框架，主要用于构建高效、可维护的机器人应用程序。',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/wsu2059q/ErisPulse',
    packages=find_packages(),
    install_requires=["aiohttp", "rich"],
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    python_requires='>=3.7',
)
