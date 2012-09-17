# Author Affliations Script
Script to handle the complexities of figuring out which superscript number goes with which authors and which institution. Useful for multi-author publications (> 20) with complex affiliations.

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

Lines that start with # are ignored. The order of the output list is given by the order of authors in the affiliations file. Authors are grouped together in author blocks which consist of one line of authors and then one line per affiliation. Each name is immediately followed, without space, by a comma seperated list of their affiliations. Example:

    Dent Earl1,2, Keith Bradnam4, John St. John1,2, Aaron Darling4

So this group consists of four authors which span four affiliations (the highest number is 4). This line would be followed by four lines listing each affiliation. These must be led by the corresponding number, enclosed in parenthesis, and a space. Example:

    (1) Center for Biomolecular Science and Engineering, University of California Santa Cruz, CA, USA
    (2) Biomolecular Engineering Department, University of California Santa Cruz, CA, USA
    (3) Howard Hughes Medical Institute, Bethesda, MD, USA
    (4) Genome Center, University of California Davis, CA, USA

The numbers from the author line must match the numbers that are present in the affilation lines. The benefit of this approach is that you can use these "local" numbers for each group, starting at 1, and the script will figure out the ultimate numbering for you.

If an author is a PI and should be listed at the end of the paper you can put "PI: " in front of their name and push them to the back of the list. ALL names listed after the first "PI: " are considered PIs. Example: 

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

The result of the script is a block of text you can paste into a document (re-formatted to look correct in github's markdown viewer):

Dent Earl1,2, Keith Bradnam3, John St. John1,2, Aaron Darling3, Dawei Lin3,4, Joseph Fass3,4, Hung On Ken Yu3, Vince Buffalo3,4, Daniel Zerbino2, Mark Diekhans1,2, Ngan Nguyen1,2, Pramila Nuwantha Ariyaratne5, Wing-Kin Sung5,6, Zemin Ning7, Matthias Haimel8, Jared T. Simpson7, Nuno A. Fonseca9, İnanç Birol10, T. Roderick Docking10, Isaac Y. Ho11, Daniel S. Rokhsar11,12, Rayan Chikhi13,14, Dominique Lavenier13,14,15, Guillaume Chapuis13,14, Delphine Naquin14,15, Nicolas Maillet14,15, Michael C. Schatz16, David R. Kelley17, Adam M. Phillippy17,18, Sergey Koren17,18, Shiaw-Pyng Yang19, Wei Wu19, Wen-Chi Chou20, Anuj Srivastava20, Timothy I. Shaw20, J. Graham Ruby21,22,23, Peter Skewes-Cox21,22,23, Miguel Betegon21,22,23, Michelle T. Dimon21,22,23, Victor Solovyev24, Igor Seledtsov25, Petr Kosarev25, Denis Vorobyev25, Ricardo Ramirez-Gonzalez26, Richard Leggett27, Dan MacLean27, Fangfang Xia28, Ruibang Luo29, Zhenyu L29, Yinlong Xie29, Binghang Liu29, Sante Gnerre30, Iain MacCallum30, Dariusz Przybylski30, Filipe J. Ribeiro30, Shuangye Yin30, Ted Sharpe30, Giles Hall30, Paul J. Kersey8, Richard Durbin7, Shaun D. Jackman10, Jarrod A. Chapman11, Xiaoqiu Huang31, Joseph L. DeRisi21,22,23, Mario Caccamo26, Yingrui Li29, David B. Jaffe30, Richard E. Green2, David Haussler1,2,23, Ian Korf3,32, Benedict Paten1,2, 

(1) Center for Biomolecular Science and Engineering, University of California Santa Cruz, CA, USA  
(2) Biomolecular Engineering Department, University of California Santa Cruz, CA, USA  
(3) Genome Center, University of California Davis, CA, USA  
(4) Bioinformatics Core, Genome Center, University of California Davis, CA, USA  
(5) Computational & Mathematical Biology Group, Genome Institute of Singapore, Singapore  
(6) School of Computing, National University of Singapore, Singapore  
(7) Wellcome Trust Sanger Institute, Wellcome Trust Genome Campus, Hinxton, UK  
(8) EMBL-EBI, Wellcome Trust Genome Campus, Hinxton, UK  
(9) CRACS-INESC Porto LA, Universidade do Porto, Portugal  
(10) Genome Sciences Centre, British Columbia Cancer Agency, Vancouver, British Columbia, Canada  
(11) DOE Joint Genome Institute, Walnut Creek, CA, USA  
(12) UC Berkeley, Dept, of Molecular and Cell Biology, Berkeley, CA, USA  
(13) Computer Science department, ENS Cachan/IRISA, Rennes, France  
(14) CNRS/Symbiose, IRISA, Rennes, France  
(15) INRIA, Rennes Bretagne Atlantique, Rennes, France  
(16) Simons Center for Quantitative Biology, Cold Spring Harbor Laboratory, Cold Spring Harbor, NY, USA  
(17) Center for Bioinformatics and Computational Biology, University of Maryland, College Park, MD, USA  
(18) National Biodefense Analysis and Countermeasures Center, Fredrick, MD, USA  
(19) Monsanto Company, 700 Chesterfield Parkway, Chesterfield, MO, USA  
(20) Institute of Bioinformatics, University of Georgia, Athens, GA, USA  
(21) Department of Biochemistry and Biophysics, University of California San Francisco, CA, USA  
(22) Biological and Medical Informatics Program, University of California, San Francisco, CA, USA  
(23) Howard Hughes Medical Institute, Bethesda, MD, USA  
(24) Department of Computer Science, Royal Holloway, University of London, UK  
(25) Softberry Inc., 116 Radio Circle, Suite 400, Mount Kisco, NY, USA  
(26) The Genome Analysis Centre, Norwich Research Park, Norwich, UK  
(27) The Sainsbury Laboratory, Norwich Research Park, Norwich, UK  
(28) Computation Institute, University of Chicago, IL, USA  
(29) BGI-Shenzhen, Shenzhen 518083, China  
(30) Broad Institute, Cambridge, MA, USA  
(31) Department of Computer Science, Iowa State University, Ames, IA, USA  
(32) Molecular and Cellular Biology, Genome Center, University of California Davis, CA, USA  


## References
1 Earl et al. Assemblathon 1: A competitive assessment of de novo short read assembly methods. Genome Res (2011) vol. 21 (12) pp. 2224-41 http://genome.cshlp.org/content/21/12/2224
