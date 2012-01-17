# Author Affliations Script
Script to handle the complexities of figuring out which superscript number goes with which authors and which institution. Useful for multi-author publications (> 20)

## Author
[Dent Earl](https://github.com/dentearl/)

## Dependencies
* Python

## Installation
1. Download package.
2. Type <code>make</code>.

## Usage
<code>authorAffiliations.py affiliations.txt [options]</code>

authorAffiliations.py takes an affiliations file and parses it into different output formats

Options:

* <code>-h, --help</code>        show this help message and exit
* <code>--format=FORMAT</code>   Controls output format. Options are raw or paper. default=paper

## Example
<code>bin/authorAffiliations.py example/affiliations.txt > pasteIntoPaper.txt</code>

## Affiliations file format

An example file (the one used to generate the author affiliations for the [Assemblathon 1](http://genome.cshlp.org/content/21/12/2224) paper) is included in the <code>example/</code> directory.

Lines that start with # are ignored. The order of the output list is given by the order of authors in the affiliations file. Authors are grouped together in author blocks which consist of one line of authors and then one line per affiliation. Each name is immediatle followed, without space, by a comma seperated list of their affiliations. Example:

    Dent Earl1,2, Keith Bradnam4, John St. John1,2, Aaron Darling4

So this group consists of four authors which span four affiliations (the highest number is 4). This line would be followed by four lines listing each affiliation. These must be led by the corresponding number, enclosed in parenthesis, and a space. Example:

    (1) Center for Biomolecular Science and Engineering, University of California Santa Cruz, CA, USA
    (2) Biomolecular Engineering Department, University of California Santa Cruz, CA, USA
    (3) Howard Hughes Medical Institute, Bethesda, MD, USA
    (4) Genome Center, University of California Davis, CA, USA

The numbers from the author line must match the numbers that are present in the affilation lines. The benefit of this approach is that you can use these "local" numbers for each group, starting at 1, and the script will figure out the ultimate numbering for you.

If an author is a PI and should be listed at the end of the paper you can put "PI: " in front of their name and push them to the back of the list. Example: 

    Jared T. Simpson1, PI: Richard Durbin1
    (1) Wellcome Trust Sanger Institute, Wellcome Trust Genome Campus, Hinxton, UK

If there is an important ordering to the end of the list (i.e. the last three authors should appear in a certain order) you may create a PI: group at the end of the affiliations file. Example:

    ...
    PI: Richard E. Green2 , David Haussler1,2,3, Ian Korf4,5, Benedict Paten1,2
    (1) Center for Biomolecular Science and Engineering, University of California Santa Cruz, CA, USA
    (2) Biomolecular Engineering Department, University of California Santa Cruz, CA, USA
    (3) Howard Hughes Medical Institute, Bethesda, MD, USA
    (4) Molecular and Cellular Biology, Genome Center, University of California Davis, CA, USA
    (5) Genome Center, University of California Davis, CA, USA


## References
1 Earl et al. Assemblathon 1: A competitive assessment of de novo short read assembly methods. Genome Res (2011) vol. 21 (12) pp. 2224-41 http://genome.cshlp.org/content/21/12/2224
