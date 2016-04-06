#!/usr/bin/env python
import os
import subprocess
import ConfigParser
import urllib2
import zipfile
from StringIO import StringIO
try:
    from setuptools import setup
    from setuptools.command.install import install as _install
except ImportError:
    from distutils.core import setup
    from distutils.command.install import install as _install


class CustomInstall(_install):
    def run(self):
        # download the binaries
        self.execute(CustomInstall._setup_binaries, (),
                     msg="Downloaded the binaries from tomato_binaries.")

        # install tomato
        _install.run(self)

        # install requirements
        subprocess.call(["pip install -r requirements"], shell=True)

    @staticmethod
    def _setup_binaries():
        """
        Downloads the binaries compiled by MATLAB Runtime Compiler from
        tomato_binaries
        """
        bin_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                  'tomato', 'bin')

        # find os, linux or macosx
        sys_os = CustomInstall._get_os()

        # read configuration file
        config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                   'tomato', 'config', 'bin.cfg')

        config = ConfigParser.ConfigParser()
        config.optionxform = str
        config.read(config_file)

        # Download binaries
        for bin_name, bin_url in config.items(sys_os):
            bin_path = os.path.join(bin_folder, bin_name)
            CustomInstall._download_binary(bin_path, bin_url, sys_os)

    @staticmethod
    def _get_os():
        process_out = subprocess.check_output(['uname']).lower()
        if any(ss in process_out for ss in ['darwin', 'macosx']):
            sys_os = 'macosx'
        elif 'linux' in process_out:
            sys_os = 'linux'
        else:
            raise OSError("Unsupported OS.")

        return sys_os

    @staticmethod
    def _download_binary(fpath, bin_url, sys_os):
        print("- Downloading binary: " + bin_url)
        response = urllib2.urlopen(bin_url)
        if fpath.endswith('.zip'):  # binary in zip
            with zipfile.ZipFile(StringIO(response.read())) as z:
                z.extractall(os.path.dirname(fpath))
            if sys_os == 'macosx':  # mac executables are actually in an app
                fpath = os.path.splitext(fpath)[0] + '.app'
            else:  # remove the zip extension
                fpath = os.path.splitext(fpath)[0]
        else:  # binary itself
            with open(fpath, 'w+') as fp:
                fp.write(response.read())

        # make the binary executalbe
        subprocess.call(["chmod -R +x " + fpath], shell=True)


setup(name='tomato',
      version='0.4',
      author='Sertan Senturk',
      author_email='contact AT sertansenturk DOT com',
      maintainer='Sertan Senturk',
      maintainer_email='contact AT sertansenturk DOT com',
      url='http://sertansenturk.com',
      description='Turkish-Ottoman Makam (M)usic Analysis TOolbox',
      long_description="""\
Turkish-Ottoman Makam (M)usic Analysis TOolbox
----------------------------------------------
tomato is a comprehensive and easy-to-use toolbox for the analysis of audio
recordings and music scores of Turkish-Ottoman makam music.
The aim of the toolbox is to allow the user to easily analyze large-scale
audio recording and music score collections of Turkish-Ottoman makam music,
using the state of the art methodologies specifically designed for the
necessities of this tradition. The analysis results can then be further used
for several tasks such as automatic content description, music
discovery/recommendation and musicological analysis.
      """,
      download_url='https://github.com/sertansenturk/tomato/releases/tag/v0.2',
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Environment :: Console',
          'Intended Audience :: Science/Research',
          'Intended Audience :: Information Technology',
          'License :: OSI Approved :: GNU Affero General Public License v3 or '
          'later (AGPLv3+)',
          'Natural Language :: English'
          'Operating System :: MacOS :: MacOS X',
          'Operating System :: POSIX :: Linux',
          'Programming Language :: Python',
          'Topic :: Multimedia :: Sound/Audio :: Analysis',
          'Topic :: Scientific/Engineering :: Information Analysis',
          ],
      platforms='Linux, MacOS X',
      license='agpl 3.0',
      packages=['tomato'],
      include_package_data=True,
      install_requires=[
      ],
      cmdclass={'install': CustomInstall},
      )
