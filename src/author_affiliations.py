#!/usr/bin/env python
"""
author_affiliations
17 Jan 2012
dent earl

Script to help create a superscripted author list
from an affiliation file that contains small groups
of authors and affiliations. See example/ for an
example input. See README.md for a short explanation.

"""
##############################
# Copyright (C) 2011-2013 by
# Dent Earl (dearl@soe.ucsc.edu, dentearl@gmail.com)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
##############################
from argparse import ArgumentParser
import os
import re
import sys

class BadFormat(Exception):
  pass

class Author():
  def __init__(self):
    self.name = ''
    self.affiliations_list = []  # assumed to be in correct order
    self.affiliations_set = set()
    # is the author the PI of a lab? PI's are
    # placed at the end of the author list
    self.is_PI = False


def InitArguments(parser):
  """Initialize arguments

  Args:
    parser: an argparse parser object
  """
  parser.add_argument('affiliations_file', default=None,
                      type=str, help=('The affiliations file.'))
  parser.add_argument('--format', dest='format', default='paper', type=str,
                      help=('Controls output format. Options are [raw, '
                            'paper]. default=%(default)s'))


def CheckArguments(args, parser):
  """Verifies input arguments are sufficient and correct for operation.

  Args:
    args: an argparse argument object
    parser: an argparse parser object
  """
  if not os.path.exists(args.affiliations_file):
    parser.error('The first argument needs to be the affiliations '
                 'file, %s does not exist!' % args.affiliations_file)
  if args.format not in ('paper', 'raw'):
    parser.error('Unrecognized value for --format %s. Must be `raw\' '
                 'or `paper\'' % args.format)


def ReadFile(file_path, args):
  """Read an input file and return a list of authors.

  Args:
    file_path: path to input file
    args: argparse object

  Returns:
    list of Author objects
    dictionary of Institutions, keyed on name, valued on order
  """
  authors = []
  these_authors = []
  these_institutions = {}  # key: number, value: string
  f = open(file_path, 'r')
  for line_number, line in enumerate(f, 1):
    if line.startswith('#'):
      continue
    line = line.strip()
    if line == '':
      these_authors = MergeLocalAuthorsInstitutions(
        these_authors, these_institutions)
      authors += these_authors
      continue
    if line.startswith('('):
      ParseInstitutionLine(line, these_institutions, args)
    elif line.startswith('Grants'):
      # TODO: add support for Grants
      pass
    else:
      these_institutions = {}
      these_authors = ParseAuthorLine(line, line_number, args)
  these_authors = MergeLocalAuthorsInstitutions(
    these_authors, these_institutions)
  if these_authors != []:
    authors += these_authors
  return authors


def MergeLocalAuthorsInstitutions(authors, institutions_dict):
  """Take an authors list and merge their institutions into master dict

  For each affilation an author has, record the current number that institution
  has in the master institution_dict into the author's affilations_list.

  Args:
    authors: list of Author objects
    instiutions: dictionary of instiution strings
  """
  for a in authors:
    new_list = []
    for l in a.affiliations_list:
      new_list.append(institutions_dict[l])
    a.affiliations_list = new_list
  return authors


def ParseInstitutionLine(line, institutions_dict, args):
  """Given an institution line from the input file, parse and store.

  Args:
    line: line from the input file
    institutions_dict: the master dictionary of intstitutions, keyed on string
      valued with position number.
    args: argparse argument object

  Raises:
    BadFormat if the institution line is incorrectly formatted.
  """
  regex = '^\((\d+)\)\s+(.*)'
  pattern = re.compile(regex)
  m = re.match(pattern, line)
  if not m:
    raise BadFormat('Error, unable to parse institution line, '
                    'regex:%s line:%s\n' %(regex, line))
  key = m.group(1)
  institution = m.group(2)
  if key in institutions_dict:
    raise BadFormat('Error, key %s already in institution dictionary\n' % key)
  institutions_dict[key] = institution


def CleanAffiliations(affiliations, line_number, args):
  """Given an author block affiliations list, return a list of numbers

  Args:
    affiliations: line from author block, should be comma-delmited ints
    line_number: line number of input file, for error messages
    args: argparse argument object

  Returns:
    a list of integers represting the affilations

  Raises:
    ValueError if the affilations line is incorrectly formatted.
  """
  affiliations_tmp = affiliations.split(',')
  affiliations = []
  for aff in affiliations_tmp:
    if aff != '':
      affiliations.append(aff)
    try:
      affiliations = sorted(affiliations, key=lambda x: int(x))
    except ValueError:
      sys.stderr.write('Found bad author affiliations on line number %d: %s\n'
                       % (line_number, affiliations))
      raise
  return affiliations

def ParseAuthorLine(line, line_number, args):
  """Given an author line from the input file, parse and store.

  Args:
    line: line from the input file
    line_number: the line number from the input file
    args: argparse argument object

  Returns:
    A list of Author objects.

  Raises:
    BadFormat if the author line is incorrectly formatted.
  """
  authors_list = []
  author_blocks = line.split(', ')
  regex = '^(\D+)([0-9,]+)'
  pat = re.compile(regex)
  is_PI = False
  for block in author_blocks:
    a = Author()
    if block.startswith('PI: '):
      block = block[4:]
      is_PI = True
    if is_PI:
      a.is_PI = True
    m = re.match(pat, block)
    if m == None:
      raise BadFormat('Error, unable to match author with '
                      'regex:%s author_block:%s\n' % (regex, block))
    a.name = m.group(1)
    affiliations = m.group(2)
    a.affiliations_list = CleanAffiliations(affiliations, line_number, args)
    for aff in affiliations:
      a.affiliations_set.add(aff)
    authors_list.append(a)
  return authors_list


def ProcessAuthors(authors, institutions, args):
  """Print out the authors list and repare the institutions dict for printing.

  Args:
    authors: a list of all Author objects.
    institutions: master dictionary of all institutions, keyed on string, valued
      on position number.
    args: argparse argument object.
  """
  i = -1
  pi_list = []
  for a in authors:
    if a.is_PI:
      pi_list.append(a)
      continue
    i = ReportAuthor(a, i, institutions, args)
  for p in pi_list:
    i = ReportAuthor(p, i, institutions, args)


def PrintInstitutions(institutions, args):
  """Print all of the instiutions in the order they appear in authors list.

  Args:
    institutions: master dictionary keyed by name string, valued by
      position number
    args: argparse argument object
  """
  if args.format == 'paper':
    sys.stdout.write('\n')
  # Swap dictionary to be keyed by position and valued by name string
  reverse_institutions = dict((v,k) for k, v in institutions.iteritems())
  for i in xrange(0, len(reverse_institutions)):
    print '(%d) %s' % (i + 1, reverse_institutions[i])


def ReportAuthor(a, i, institutions, args):
  """Print out the current author and record their institution placements.

  Args:
    a: an Author object
    i: the index integer of the current institution
    institutions: master dictionary, keyed name string, valued by position
    args: argparse argument object

  Returns:
    i: current institution integer
  """
  sys.stdout.write('%s' % a.name)
  institution_list = []
  for inst in a.affiliations_list:
    if inst not in institutions:
      i += 1
      institutions[inst] = i
    institution_list.append(institutions[inst])
  # print out the affiliations in sorted order
  institution_list = sorted(institution_list, key=lambda x: int(x))
  num = - 1
  for inst in institution_list:
    num += 1
    if num > 0:
      sys.stdout.write(',%d' % (inst + 1))
    else:
      sys.stdout.write('%d' % (inst + 1))
  if args.format == 'raw':
    sys.stdout.write(' PI:%s\n' % a.is_PI)
  elif args.format == 'paper':
    sys.stdout.write(', ')
  return i


def main():
  usage=('usage: %(prog)s affiliations.txt [options]\n\n'
         '%(prog)s takes an affiliations file and parses it '
         'into different output formats')
  parser = ArgumentParser(usage=usage)
  InitArguments(parser)
  args = parser.parse_args()
  CheckArguments(args, parser)

  authors = ReadFile(args.affiliations_file, args)
  institutions = {}  # key: position, value: name string
  ProcessAuthors(authors, institutions, args)
  PrintInstitutions(institutions, args)

if __name__ == '__main__':
  main()
