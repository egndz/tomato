# tomato

**T**urkish-**O**ttoman **M**akam (M)usic **A**nalysis **TO**olbox

[![Build Status](https://travis-ci.com/sertansenturk/tomato.svg?branch=master)](https://travis-ci.com/sertansenturk/tomato) [![GitHub version](https://badge.fury.io/gh/sertansenturk%2Ftomato.svg)](https://badge.fury.io/gh/sertansenturk%2Ftomato) [![Code Climate](https://codeclimate.com/github/sertansenturk/tomato/badges/gpa.svg)](https://codeclimate.com/github/sertansenturk/tomato) [![DOI](https://zenodo.org/badge/21104/sertansenturk/tomato.svg)](https://zenodo.org/badge/latestdoi/21104/sertansenturk/tomato) [![License: AGPL v3](https://img.shields.io/badge/License-AGPL%20v3-ff69b4.svg)](http://www.gnu.org/licenses/agpl-3.0) [![License: CC BY-NC-SA 4.0](https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-ff69b4.svg)](http://creativecommons.org/licenses/by-nc-sa/4.0/)

## Introduction

`tomato` is a comprehensive and easy-to-use toolbox in Python for the analysis of audio recordings and music scores of Turkish-Ottoman makam music. The toolbox includes the state of art methodologies applied to this music tradition. The analysis tasks include:

- **Symbolic Analysis:** score metadata extraction, score section extraction, score phrase segmentation, semiotic section, and phrase analysis
- **Audio Analysis:** audio metadata crawling, predominant melody extraction, tonic and transposition identification, makam recognition, pitch distribution computation, tuning analysis, melodic progression analysis
- **Joint Analysis:** score-informed tonic identification and tempo estimation, section linking, note-level audio-score alignment, predominant melody octave correction, note modeling

The toolbox aims to facilitate the analysis of large-scale audio recording and music score collections of Turkish-Ottoman makam music, using the state of the art methodologies designed for the culture-specific characteristics of this tradition. The analysis results can then be further used for several tasks such as automatic content description, music discovery/recommendation, and musicological analysis.

If you are using `tomato` in your work, please cite the dissertation:

> Şentürk, S. (2016). [Computational Analysis of Audio Recordings and Music Scores for the Description and Discovery of Ottoman-Turkish Makam Music](http://sertansenturk.com/research/works/phd-thesis/). Ph.D. thesis, Universitat Pompeu Fabra, Barcelona, Spain.

For the sake of __reproducibility__, please also state the version you used as indexed at [Zenodo](https://zenodo.org/search?page=1&size=20&q=conceptrecid:%22597862%22&sort=-version&all_versions=True).

For the descriptions of the methodologies in the toolbox, please refer to the papers listed in the [References](#references).

## tomato in a Nutshell

```python
# import ...
from tomato.joint.completeanalyzer import CompleteAnalyzer
from matplotlib import pyplot as plt

# score input
symbtr_name = 'makam--form--usul--name--composer'
txt_score_filename = 'path/to/txt_score'
mu2_score_filename = 'path/to/mu2_score'

# audio input
audio_filename = 'path/to/audio'
audio_mbid = '11111111-1111-1111-1111-11111111111'  # MusicBrainz Recording Identifier

# instantiate analyzer object
completeAnalyzer = CompleteAnalyzer()

# Apply the complete analysis. The resulting tuple will have
# (summarized_features, score_features, audio_features,
# score_informed_audio_features, joint_features) in order
results = completeAnalyzer.analyze(
    symbtr_name=symbtr_name, symbtr_txt_filename=txt_score_filepath,
    symbtr_mu2_filename=mu2_score_filepath, audio_filename=audio_filepath,
    audio_metadata=audio_mbid)

# plot the summarized features
fig, ax = completeAnalyzer.plot(results[0])
ax[0].set_ylim([50, 500])
plt.show()
```

You can refer to the jupyter notebooks in [demos](https://github.com/sertansenturk/tomato/blob/master/demos) folder for detailed, interactive examples.

## Installation

There are four steps in the installation:

1. [Installing tomato](#installing-tomato)
2. [Installing Essentia](#installing-essentia)
3. [Installing MATLAB Runtime](#installing-matlab-runtime)
4. [Installing LilyPond](#installing-lilypond) (optional)

### Installing tomato

`tomato` may require several packages to be installed depending on your operating system. For example, in *Ubuntu 16.04* using *Python 3.5*, you have to install the _python 3_, _libxml2, libxslt1, freetype_, and _png_ development packages. You can install them by:

```bash
sudo apt-get install python3 python3.5-dev python3-pip libxml2-dev libxslt1-dev libfreetype6-dev libpng12-dev
```

It is recommended to install `tomato` and its dependencies into a virtualenv. In the terminal, do the following:

```bash
virtualenv --no-site-packages -p python3 env
source env/bin/activate
```

Then change the current directory to the repository folder and install by:

```bash
cd path/to/tomato
python setup.py install
```

The requirements are installed during the setup. If that step does not work for some reason, you can install the requirements by calling:

```bash
pip install -r requirements.txt
```

If you want to edit files in the package and want the changes reflected, you should call:

```bash
cd path/to/tomato
pip install -e .
```

### Installing Essentia

__tomato__ uses several audio signal processing modules in *Essentia*. **Linux** users can skip this section, since the library is automatically installed during setup.

For **Mac OSX**, please follow the [instructions](https://essentia.upf.edu/installing.html#mac-osx) to install the library.

If you are running `tomato` on a `virtualenv`, you might need to link the python bindings of Essentia:

```bash
ln -s path_to_essentia_bindings path_to_env/lib/python3.x/site-packages
```

Don't forget to change the `path_to_essentia_bindings`, `path_to_env`, and `python3.x` with the actual path of the installed Essentia Python bindings, the path of your virtualenv, and your Python version in the virtual environment, respectively. Depending on the Essentia version, the default installation path of the Essentia bindings is either `/usr/local/lib/python3.x/dist-packages/essentia` or `/usr/local/lib/python3.x/site-packages/essentia`.

### Installing MATLAB Runtime

The score phrase segmentation, score-informed joint tonic identification and tempo estimation, section linking, and note-level audio-score alignment algorithms are implemented in MATLAB and compiled as binaries. They need **MATLAB Runtime for R2015a (8.5)** to run. You should download and install this specific version  (links for [Linux](http://www.mathworks.com/supportfiles/downloads/R2015a/deployment_files/R2015a/installers/glnxa64/MCR_R2015a_glnxa64_installer.zip) and [Mac OSX](http://www.mathworks.com/supportfiles/downloads/R2015a/deployment_files/R2015a/installers/maci64/MCR_R2015a_maci64_installer.zip)).

We recommend you to install MATLAB Runtime in the default installation path, as `tomato` searches them automatically. Otherwise, you have to specify your own path in the MATLAB Runtime configuration file, [tomato/config/mcr_path.cfg](https://github.com/sertansenturk/tomato/blob/master/tomato/config/mcr_path.cfg).

### Installing LilyPond

`tomato` uses LilyPond under the hood to convert the music scores to SVG format. To install LilyPond in Mac OSX, go to the [Download](http://lilypond.org/download.html) page on the LilyPond website and follow the instructions for your operating system.

In most Linux distributions, you can install LilyPond from the software repository of your distribution (e.g. `sudo apt install lilypond` in Debian-based distributions). However, the version might be outdated. If the version is below 2.18.2, we recommend you to download the latest stable version from the [LilyPond website](http://lilypond.org/download.html). If you had to install LilyPond this way, you should enter the LilyPond binary path to the "custom" field in [tomato/config/lilypond.cfg](https://github.com/sertansenturk/tomato/tree/master/tomato/config) (the default location is ```$HOME/bin/lilypond```).

## Running tomato via Docker

XX

```bash
docker build . -t sertansenturk/tomato && docker run -v "$PWD/demos/":/home/tomato_user/demos/ -it sertansenturk/tomato bash
```

## Documentation

Coming soon...

## License

The source code hosted in this repository is licensed under [Affero GPL version 3](https://www.gnu.org/licenses/agpl-3.0.en.html).

Any data (the music scores, extracted features, training models, figures, outputs, etc.) are licensed under [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License](http://creativecommons.org/licenses/by-nc-sa/4.0/).

## FAQ

1. **The notes aligned by `JointAnalyzer.align_audio_score(...)` seems shifted. What is the problem?**

    Your audio input is probably a compressed format such as *mp3*. There are typically shifts between different decoders (and even different versions of the same decoder) when they decode the same compressed audio file. In the predominant melody extraction step (`AudioAnalyzer.extract_pitch(...)`), Essentia has to decode the recording for processing. You observe a shift when the application you use another decoder.

    These shifts are typically small (e.g., 50 samples ~1ms), so they are not very problematic. Nevertheless, there is no guarantee that the shift will be prominent. If you need "perfect" synchronization, you should use an uncompressed format such as *wav* as the audio input.

    **Note:** In demos, we use *mp3*, because it would be too bulky to host a *wav* file.

2. **Which operating systems are supported?**

    The algorithms, which are written purely in Python, are platform-independent. However, [compiling Essentia in Windows](http://essentia.upf.edu/documentation/installing.html#building-essentia-on-windows) is not straightforward yet. Therefore we have only compiled the MATLAB binaries for **Mac OSX** and **Linux**.
    If you have compiled Essentia for Windows somehow or if you have any OS -1specific problems, please let us know by submitting an [issue](https://github.com/sertansenturk/tomato/issues).

3. **What are the supported Python versions?**

    `tomato` supports all Python versions above 3.5. If you want to run `tomato` on Python 2.7, please install [v0.13.0](https://github.com/sertansenturk/tomato/releases/tag/v0.13.0) or below.

4. **Where are the MATLAB binaries?**

    The binaries are not stored in `tomato` because they are relatively big. It would take too much space to store them here, including the versions introduced in each modification. Instead, the binaries are provided within the releases of the relevant packages. The binaries are downloaded to [tomato/bin](https://github.com/sertansenturk/tomato/blob/master/tomato/bin) during the installation process of `tomato`.
    Please refer to [tomato/config/bin.cfg](https://github.com/sertansenturk/tomato/blob/master/tomato/config/bin.cfg) for the relevant releases.

5. ```ScoreConverter``` says that "The lilypond path is not found." How can I fix the error?

    There can be similar problems regarding this issue:

    - The user-provided file path (the music score input) does not exist.

        Check your input MusicXML-score path.

    - LilyPond is not installed.

        [Install](#installing-lilypond) the latest stable version for your OS.

    - The binary path exists, but it is not used.

        The path is not searched by the defaults defined in ```tomato/config/lilypond.cfg```. Add the path of the LilyPond binary to the configuration file.

6. Is `tomato` a fruit or vegetable?

    It has a culture-specific answer.

## Authors

Sertan Şentürk
contact@sertansenturk.com

## Acknowledgements

We would like to thank [Harold Hagopian](https://en.wikipedia.org/wiki/Harold_Hagopian), the founder of [Traditional Crossroads](http://traditionalcrossroads.com/About-Us), for allowing us to use Tanburi Cemil Bey's performance of [Uşşak Sazsemaisi](http://musicbrainz.org/recording/f970f1e0-0be9-4914-8302-709a0eac088e) in our demos.

## References

_The toolbox has been realized as part of the thesis:_

[1] Şentürk, S. (2016). *Computational analysis of audio recordings and music scores for the description and discovery of Ottoman-Turkish makam music.* Ph.D. thesis, Universitat Pompeu Fabra, Barcelona, Spain.  

_The methods used in the toolbox are described in the papers:_

__Score Phrase Segmentation__  
[1] Bozkurt, B., Karaosmanoğlu, M. K., Karaçalı, B., and Ünal, E. (2014). *Usul and makam driven automatic melodic segmentation for Turkish music.* Journal of New Music Research. 43(4):375–389.

__Score Section Extraction; Semiotic Section and Phrase Analysis__  
[2] Şentürk S., and Serra X. (2016). *A method for structural analysis of Ottoman-Turkish makam music scores.* In Proceedings of 6th International Workshop on Folk Music Analysis (FMA 2016), pages 39–46, Dublin, Ireland.

__Audio Predominant Melody Extraction__
[3] Atlı, H. S., Uyar, B., Şentürk, S., Bozkurt, B., and Serra, X. (2014). *Audio feature extraction for exploring Turkish makam music.* In Proceedings of 3rd International Conference on Audio Technologies for Music and Media (ATMM 2014), pages 142–153, Ankara, Turkey.

__Audio Pitch Filter__  
[4] Bozkurt, B. (2008). *An automatic pitch analysis method for Turkish maqam music.* Journal of New Music Research. 37(1):1–13.

__Audio Tonic and Transposition Identification, Makam Recognition, Pitch Distribution Computation, Tuning Analysis__  
[4] Bozkurt, B. (2008). *An automatic pitch analysis method for Turkish maqam music.* Journal of New Music Research. 37(1):1–13.
[5] Gedik, A. C., and Bozkurt, B. (2010). *Pitch-frequency histogram-based music information retrieval for Turkish music.* Signal Processing. 90(4):1049–1063.  
[6] Chordia, P. and Şentürk, S. (2013). *Joint recognition of raag and tonic in North Indian music.* Computer Music Journal. 37(3):82–98.  

__Audio Tonic Identification from the Last Note__  
[7] Atlı, H. S., Bozkurt, B., and Şentürk, S. (2015). *A method for tonic frequency identification of Turkish makam music recordings.* In Proceedings of 5th International Workshop on Folk Music Analysis (FMA 2015), pages 119–122, Paris, France.

__Audio Melodic Progression (Seyir) Analysis__  
[8] Bozkurt B. (2015). *Computational analysis of overall melodic progression for Turkish Makam Music.* In Penser l’improvisation, pages 289–298, Delatour France, Sampzon.

__Score-Informed Audio Tonic Identification__  
[9] Şentürk, S., Gulati, S., and Serra, X. (2013). *Score informed tonic identification for makam music of Turkey.* In Proceedings of 14th International Society for Music Information Retrieval Conference (ISMIR 2013), pages 175–180, Curitiba, Brazil.

__Score-Informed Audio Tempo Estimation__  
[10] Holzapfel, A., Şimşekli U., Şentürk S., and Cemgil A. T. (2015). *Section-level modeling of musical audio for linking performances to scores in Turkish makam music.* In Proceedings of 40th IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP 2015), pages 141–145, Brisbane, Australia.

__Audio-Score Section Linking__  
[11] Şentürk, S., Holzapfel, A., and Serra, X. (2014). *Linking scores and audio recordings in makam music of Turkey.* Journal of New Music Research, 43(1):34–52.

__Note-Level Audio-Score Aligment__  
[12] Şentürk, S., Gulati, S., and Serra, X. (2014). *Towards alignment of score and audio recordings of Ottoman-Turkish makam music.* In Proceedings of 4th International Workshop on Folk Music Analysis (FMA 2014), pages 57–60, Istanbul, Turkey.

__Score-Informed Audio Predominant Melody Correction; Note Modeling__  
[13] Şentürk, S., Koduri G. K., and Serra X. (2016). *A score-informed computational description of svaras using a statistical model.* In Proceedings of 13th Sound and Music Computing Conference (SMC 2016), pages 427–433, Hamburg, Germany.
