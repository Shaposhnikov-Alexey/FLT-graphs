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

*Eighth assignment*

[![Build Status](https://travis-ci.org/Shaposhnikov-Alexey/FLT-graphs.svg?branch=assignment_8)](https://travis-ci.org/Shaposhnikov-Alexey/FLT-graphs)

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
### Current language's syntax version is **1.1**
#### Changes from 1.0 version:
 - statements now are separated by ';'
 - patterns are defined with ```def [production_head]: [production body]```
 - there is no more need in white spaces between special characters like '(', ')', ',', ';', '*', '+', '?', '|', '.'
 - regexps now support standard form (with spec. chars like above) as long as old one 
    - example: ```def S: nonterm (b) concat (term (a) plus opt term (c)``` now corresponds to ```def S: nonterm(b).(term(a)+|term(c)))``` and both can be used
 - uppercase letters are now legit
 
### Current syntax:
There are 3 statements you can use in script. They are divided by ';' and you can use tabulation;

Allowed type of strings is: ```(/, ., _, 0-9, a-z)```.

Available commands are:

- `connect "[db_name]"` - set database directory
    #### Example:
    ` connect "/src/data.txt";`

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
                - `set(1, 2, 3, ..., 10)` -  set
                - `range n , m` - range
                - `none` if you don't want to specify

    #### Example:
    ``` 
    connect "src/data/graph.txt";

    def s: nonterm (b) star concat term (f) opt;
    def f: nonterm (a) alt nonterm (b) concat term (q);
    def q: nonterm(c)*;

    select filter edges with (24, edge, 26)
        satisfies (24 labelIs first)
            and not (26 labelIs first or isFinal 26)
                from name "graph";

    select count filter edges
        with (first, label, second)
            satisfies (isStart first  or isFinal second)
                from name "grammar_1";
    ```

- `def [production_head] : [production_body]` - adds production to grammar which is being saved and can be called as a Graph - for intersection or selecting. Body can be a regular expression with keywords **{ } alt; { } opt; { } plus; { } star", you can also use special eps symbol - "e" 
    - and since version 1.1 you can also use special characters like '*', '?', '+', '|', '.'
    #### Examples: 
      def a: term (a) star concat term (b);
      def c: nonterm (b) star;
      def f: nonterm (b) alt nonterm (c) star concat term (s);
      def d: e;
      def S1: term(a)?.term(b).(term(c)|term(d))*;
        
## ANTLR and DOT visualization
See query language's syntax from above for antlr grammar reference.

Notice that this grammar corresponds to syntax's version 1.1 and above whilst .txt grammar corresponds to syntax's version 1 (check older commits).

To test your script first ensure you have antlr4 downloaded:
```bash
sudo apt-get update
sudo apt-get install antlr4
``` 
and that you have all modules from **requirements_pip.txt** installed.

After that, run the following:
```bash
cd src/antlr && antlr4 -Dlanguage=Python3 db_grammar.g4 && cd ../ ../
```

To generate AST visualization:
```bash
ast.py [-h] (-i --input inputFile) (-o --output outputFile) (-v --view showView)

positional arguments:
  inputFile     Path to query script file
  outputFile    Path to output visualization (.dot file)
  showView      Open visualization
optional arguments:
  -h, --help  show this help message 
```

#### ANTLR analyzing and DOT visualization example
if you run 
```bash
python script_ast.py -i src/antlr/script_example.txt -o visualization.dot -v
```
the AST will be saved in **[visualization.dot]** and you will see pdf representation: You can download it here or check file **[visualization.dot.pdf]**

[Download Example AST](https://raw.githubusercontent.com/Shaposhnikov-Alexey/FLT-graphs/283bba133618c76e75caec9e26c4b5f536c33456/visualization.dot.pdf)
