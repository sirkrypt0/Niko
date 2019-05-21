from distutils.core import setup

setup(name="Niko",
      version="1.0",
      description="Niko, der RoboCop",
      author="Der einzig wahre Rode LK",
      author_email="s.rode@plg-berlin.de",
      url="http://www.plg-berlin.de",
      packages=['niko'],
      package_data={'niko':['dokumentation/*.pdf','resources/*.gif']})
    

'''
Run
setup.py sdist
for normal distribution.

Run
setup.py install
for installation.

Run
setup.py bdist_wininst
for windows distribution with executable installer.
'''
