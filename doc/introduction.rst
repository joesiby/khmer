.. vim: set filetype=rst

=====================
Introduction to khmer
=====================

Introduction
============

khmer is a library and toolkit for doing k-mer-based dataset analysis and 
transformations.  Our focus in developing it has been on scaling assembly of 
metagenomes and mRNA.

khmer can be used for a number of transformations, include inexact 
transformations (abundance filtering and error trimming) and exact 
transformations (graph-size filtering, to throw away disconnected reads; and 
partitioning, to split reads into disjoint sets).  Of these, only partitioning 
is not constant memory.  In all cases, the memory required for assembly with 
Velvet or another de Bruijn graph assembler will be more than the memory 
required to use our software. Our software will not increase the memory required 
for Velvet, either, although we may not be able to *decrease* the memory 
required for assembly for every data set.

Most of khmer relies on an underlying probabilistic data structure known as a 
`Bloom filter <http://en.wikipedia.org/wiki/Bloom_filter>`__ (also see 
`Count-Min Sketch <http://dimacs.rutgers.edu/~graham/pubs/papers/cm-full.pdf>`__ 
and `These Are Not The k-mers You're Looking For 
<http://www.ncbi.nlm.nih.gov/pmc/articles/PMC4111482/>`__), which is essentially 
a set of hash tables, each of different size, with no collision detection. These 
hash tables are used to store the presence of specific k-mers and/or their 
count.  The lack of collision detection means that the Bloom filter may report a 
k-mer as being "present" when it is not, in fact, in the data set; however, it 
will never incorrectly report a k-mer as being absent when it *is* present.  
This one-sided error makes the Bloom filter very useful for certain kinds of 
operations.

khmer is also independent of K, and currently works for K <= 32.  We will be 
integrating code for up to K=64 soon.

khmer is implemented in C++ with a Python wrapper, which is what all of the 
scripts use.

Some important documentation for khmer is provided on the Web sites for 
`khmer-protocols <http://khmer-protocols.readthedocs.org>`__ and `khmer-recipes 
<http://khmer-recipes.readthedocs.org>`__. khmer-protocols provides detailed 
protocols for using khmer to analyze either a transcriptome or a metagenome; 
khmer-recipes provides individual recipes for using khmer in a variety of 
sequence-oriented tasks such as extracting reads by coverage, estimating a 
genome or metagenome size from unassembled reads, and error-trimming reads via 
streaming k-mer abundance.

Using khmer
===========

khmer comes "out of the box" with a number of scripts that make it
immediately useful for a few different operations, including:

 - normalizing read coverage ("digital normalization")

 - dividing reads into disjoint sets that do not connect ("partitioning")

 - eliminating reads that will not be used by a de Bruijn graph assembler;

 - removing reads with low- or high-abundance k-mers;

 - trimming reads of certain kinds of sequencing errors;

 - counting k-mers and estimating data set coverage based on k-mer counts;

 - running Velvet and calculating assembly statistics;

 - optimizing assemblies on various parameters;

 - converting FASTA to FASTQ;

and a few other random functions.

Practical considerations
========================

The most important thing to think about when using khmer is whether or not the 
transformation or filter you're applying is appropriate for the data you're 
trying to assemble.  Two of the most powerful operations available in khmer, 
graph-size filtering and graph partitioning, only make sense for assembly 
datasets with many theoretically unconnected components.  This is typical of 
metagenomic data sets.

The second most important consideration is memory usage.  The effectiveness of 
all of the Bloom filter-based functions (which is everything interesting in 
khmer!) depends critically on having enough memory to do a good job.  See 
:doc:`user/choosing-table-sizes` for more information.

Copyright and license
=====================

Portions of khmer are Copyright California Institute of Technology,
where the exact counting code was first developed; the remainder is
Copyright Michigan State University.  The code is freely available for
use and re-use under the BSD License.
