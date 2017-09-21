# Team BIASES
*Repository for Team BIASES*

## Getting Started
This section describes how to clone the repository and install the dependencies for the project.

 1. Make sure [Python 3](https://www.python.org/downloads/) and [Git](https://git-scm.com/downloads) are installed.
 2. Open a terminal and clone this repository with `git clone https://github.com/teambiases/team-biases.git`.
 3. Enter the team-biases directory and run `pip3 install -r requirements.txt`. This should install all the python libraries needed.

## Organization
This section contains information about how the files and packages in this project are laid out.

### Directory layout
The main directories and files are as follows:

 * `src-python`—this directory contains the bulk of the Python code in the `biases` package. See the section [package layout](#package-layout) for more information about how the code is laid out.
 * `scripts`—this directory contains scripts meant to be run directly from the command line. It also contains the `_path_config` module, which when included at the top of a script file configures the `PYTHONPATH` to allow the `biases` package to be included.
 * `README.md`—the file you're reading. It contains basic information about the project.
 * `.gitignore`—used by git to know what types of files it should ignore (for instance, compiled python files). More information [here](https://git-scm.com/docs/gitignore).
 * `requirements.txt`—a list of python libraries in the PyPI repository that are requirements for the project. More information [here](https://pip.pypa.io/en/stable/user_guide/#requirements-files).

### Package layout
The packages and modules in `src-python` are all located under an overarching `biases` package. To learn more about python modules, read [this](https://docs.python.org/3/tutorial/modules.html). These are the current packages in `src-python`:

 * `biases.bias`—bias detection code
 * `biases.wiki`—tools for working with Wikipedia
 * `biases.utils`—various utilies in areas such as math or databases
 
## Building
This section describes how to build the results from Wikipedia dump files.

 1. Make a directory `data/wikipedia/dump` and download the following files into that directory:
   - From https://dumps.wikimedia.org/enwiki/20170901/, download `enwiki-20170120-pages-articles.xml.bz2`.
   - From https://dumps.wikimedia.org/ruwiki/20170901/, download `ruwiki-20170120-pages-articles.xml.bz2`.
   - From https://dumps.wikimedia.org/eswiki/20170901/, download `eswiki-20170120-pages-articles.xml.bz2` and `eswiki-20170120-langlinks.sql.gz`.
 2. From the `team-biases` directory, run `make topicscorpus`. This will probably take ~24 hours to run.
 3. Run `python3 scripts/topics_demo.py data/wikipedia/corpus/coldwar.es-en-ru-wiki-20170901.400topics.pickle`. If everything worked, a web page should pop up where you can inspect the topic distributions of various articles!
