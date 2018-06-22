
from distutils.core import setup

setup(name='Kankei',
      version='0.1',
      description='Python Kanji Database Project',
      author='Jérémie Bigras-Dunberry',
      author_email='Bigjerbd@gmail.com',
      url='https://github.com/BigJerBD/Kankei',
      packages=[
          'distutils',
          'distutils.command'
      ], requires=['jaconv', 'kanaconv', 'PyYAML']
      )