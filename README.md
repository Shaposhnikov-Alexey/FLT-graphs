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

*Seventh assignment*

[![Build Status](https://travis-ci.org/Shaposhnikov-Alexey/FLT-graphs.svg?branch=assignment_7)](https://travis-ci.org/Shaposhnikov-Alexey/FLT-graphs)


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

## Script graph database queries language's syntax
There are 3 statements you can use in script. They are divided by new line, tokens and keywords - with white space. Note that *parentheses should be separated with white space*!

Allowed type of strings is: ```(/, ., _, 0-9, a-z)```.

Available commands are:

- ** `connect "[db_name]"`** - set database directory
    - ` connect "/src/data" `

- `[production_head] : [production_body]` - adds production to grammar which is being saved and can be called as a Graph - for intersection or selecting. Body can be a regular expression with keywords **{ } alt; { } opt; { } plus; { } star", you can also use special eps symbol - "e" 

    #### Examples: ```
      a: term (a) star concat term (b)
      c: nonterm (b) star
      f: nonterm (b) alt nonterm (c) star concat term (s)
      d: e
        ```