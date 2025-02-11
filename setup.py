from setuptools import setup, find_packages

setup(
    name="kahinbot",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'python-telegram-bot>=13.0',
        'python-dotenv>=0.19.0', 
    ],
    entry_points={
        'console_scripts': [
            'kahinbot=kahinbot.bot:main',
        ],
    },
    author="Şeyma Yardım",
    author_email="seyma.yardim@ogr.iu.edu.tr",
    description="A Telegram bot that provides characteristic features based on birthdates",
    long_description=open('README.md').read() if os.path.exists('README.md') else '',
    long_description_content_type='text/markdown',
    keywords='telegram bot astrology birthdate',
    url="https://github.com/Seymapro/Kahinbot/",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.11', 
    ],
    python_requires='>=3.11.2', 
)
