# FLT-graphs
Repository for assignments from Formal Language Theory course

## Status

*First assignment*

[![Build Status](https://travis-ci.org/Shaposhnikov-Alexey/FLT-graphs.svg?branch=master)](https://travis-ci.org/Shaposhnikov-Alexey/FLT-graphs)

*Second assignment*

[![Build Status](https://travis-ci.org/Shaposhnikov-Alexey/FLT-graphs.svg?branch=assignment_2_re)](https://travis-ci.org/Shaposhnikov-Alexey/FLT-graphs)

*Fourth assignment*

[![Build Status](https://travis-ci.org/Shaposhnikov-Alexey/FLT-graphs.svg?branch=assignment_4)](https://travis-ci.org/Shaposhnikov-Alexey/FLT-graphs)

*Fifth assignment*

[![Build Status](https://travis-ci.org/Shaposhnikov-Alexey/FLT-graphs.svg?branch=assignment_5)](https://travis-ci.org/Shaposhnikov-Alexey/FLT-graphs)


## Install

```bash
conda config --append channels conda-forge
conda create -q -n flt-env --file requirements_conda.txt
conda activate flt-env

export PYTHONPATH="${PYTHONPATH}:./"

# if you have python 3.8 or higher, use pip3 instead
pip install -r requirements_pip.txt
```
# Assignments

To run tests
```bash
pytest
```

#### Analysis
To see experimental analysis of performance for transitive closure (squaring and adjency matrix), check report_assignment_3.pdf in **reports** directory

To see experimental analysis of performance for CFPQ with matrix multiplication, CFPQ with tensor production, CFPQ with tensor production and optimized grammar, Hellings algo, check report_assignment_6.pdf in **src/reports** directory

To see experimental data for CFPQ analysis, check [google drive](https://drive.google.com/drive/folders/1yghCOVHcOqG4TTsLqcp4UnIpfwx_ZCxv?usp=sharing])
