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

- `connect "[db_name]"` - set database directory
    - ` connect "/src/data" `

- `select [object] from [graph]` - get queried info from graph
    - `[object]` can be **count**, **edges** or **filter**. **Count** returns number of edges; **edges** return all triples (u, lbl, v) from graph; **filter** filters with defined condition `[BOOL_EXPR]'
    - `[BOOL_EXPR]` is one or combination of:
        - `isStart [vert]`
        - `isFinal [vert]` 
        - `[edge] labelIs [label]`

    - `[graph]` can be invoked with given name, grammar, regex or graph intersection
        - `"[graph_name]"` loads a graph file from connected database
        - `grammar` invokes saved grammar with defined productions (see below)
        - `[pattern]` will take regex of a given pattern 
        - `[graph] intersect [other_graph]` takes intersection
        - `setStartAndFinal ([vertices] ; [vertices]) [graph]` will take a graph with specified start and final vertices
            - `[vertices]` can be represented in following formats:
                - `1, 2, 3, ...` -  set
                - `n , m` - range
                - `none` 

    #### Examples:
    ``` 
    select count edges from setStartAndFinal (1, 2, 3 ; 4, 5, 6) name "graph" intersect query term (a) star concat term (b) plus
    select edges from name "graph" intersect query nonterm (a) concat nonterm (b) plus
   select filter edges with (1, edge, 2) satisfies 1 labelIs first and not 2 labelIs first from name "graph"
  select filter edges with (1, edge, 2) satisfies 1 labelIs first from name "graph"
  select filter edges with (24, edge, 26) satisfies 24 labelIs first and not 26 labelIs first or isFinal 26 
                from name "graph" intersect grammar
   select count edges from setStartAndFinal ( range  4 , 5 ; none ) name "graph" intersect name "other_graph"
  ```

- `[production_head] : [production_body]` - adds production to grammar which is being saved and can be called as a Graph - for intersection or selecting. Body can be a regular expression with keywords **{ } alt; { } opt; { } plus; { } star", you can also use special eps symbol - "e" 

    #### Examples: 
      a: term (a) star concat term (b)
      c: nonterm (b) star
      f: nonterm (b) alt nonterm (c) star concat term (s)
      d: e
        