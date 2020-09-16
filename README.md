# FLT-graphs
Repository for assignments from Formal Language Theory course

## Status
*First assignment*

[![Build Status](https://travis-ci.org/Shaposhnikov-Alexey/FLT-graphs.svg?branch=assignment_1)](https://travis-ci.org/Shaposhnikov-Alexey/FLT-graphs)

*Second assignment*

[![Build Status](https://travis-ci.org/Shaposhnikov-Alexey/FLT-graphs.svg?branch=assignment_2)](https://travis-ci.org/Shaposhnikov-Alexey/FLT-graphs)

## Install

```bash
conda config --append channels conda-forge
conda create -q -n ftl-env --file requirements_conda.txt
conda activate ftl-env
export PYTHONPATH="${PYTHONPATH}:./"
# if you have python 3.8 or higher, use pip3 instead
pip install -r requirements_pip.txt
```
# Assignments
To run tests
```bash
pytest
```

# API
#### 1) Intersection 
- **returns** labels and their occurrences in the intersection received from specified graph and regexp
- **'from'** and **'to'** parameters will be supported later
```bash
python src/main/main.py {graph_path.txt} {regexpt_path.txt}
```