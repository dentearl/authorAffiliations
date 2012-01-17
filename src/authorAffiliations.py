#!/usr/bin/env python2.6
""" 
authorAffiliations.py
17 Jan 2012
dent earl

Script to help create a superscripted author list
from an affiliation file that contains small groups 
of authors and affiliations. See example/ for an
example input. See README.md for a short explanation.

"""
##############################
# Copyright (C) 2011-2012 by 
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
from optparse import OptionParser
import os
import re
import sys

class Author():
   def __init__(self):
      self.name = ''
      self.affiliationsList = [] # assumed to be in correct order
      self.affiliationsSet = set()
      self.isPI = False # is the author the PI of a lab? PI's are placed at the end of the author list

def initOptions(parser):
   parser.add_option('--format', dest = 'format', default = 'paper',
                     help = ('Controls output format. Options are raw or paper. default=%default'))

def checkOptions(options, args, parser):
   if len(args) != 1:
      parser.error('The first argument needs to be the affiliations file!')
   if not os.path.exists(args[0]):
      parser.error('The first argument needs to be the affiliations file, %s does not exist!' % args[0])
   if options.format not in ('paper', 'raw'):
      parser.error('Unrecognized value for --format %s. Must be `raw\' or `paper\'' % options.format)

def readFile(filename, options):
   authors = []
   theseAuthors = []
   theseInstitutions = {} # key: number, value: string
   f = open(filename, 'r')
   for line in f:
      if line.startswith('#'):
         continue
      line = line.strip()
      if line == '':
         theseAuthors = mergeLocalAuthorsInstitutions(theseAuthors, theseInstitutions)
         authors += theseAuthors
         continue
      if line.startswith('('):
         parseInstitutionLine(line, theseInstitutions, options)
      elif line.startswith('Grants'):
         pass
      else:
         theseInstitutions = {}
         theseAuthors = parseAuthorLine(line, options)
   theseAuthors = mergeLocalAuthorsInstitutions(theseAuthors, theseInstitutions)
   if theseAuthors != []:
      authors += theseAuthors
   return authors

def mergeLocalAuthorsInstitutions(auths, insts):
   for a in auths:
      newList = []
      for l in a.affiliationsList:
         newList.append(insts[l])
      a.affiliationsList = newList
   return auths

def parseInstitutionLine(line, iDict, options):
   regex = '^\((\d+)\)\s+(.*)'
   pat = re.compile(regex)
   m = re.match(pat, line)
   if not m:
      sys.stderr.write('Error, unable to parse institution line, regex:%s line:%s\n' %(regex, line))
      sys.exit(1)
   key = m.group(1)
   institution = m.group(2)
   if key in iDict:
      sys.stderr.write('Error, key %s already in institution dictionary\n' % key)
      sys.exit(1)
   iDict[key] = institution

def parseAuthorLine(line, options):
   authorsList = []
   auths = line.split(', ')
   regex = '^(\D+)([0-9,]+)'
   pat = re.compile(regex)
   isPI = False
   for auth in auths:
      a = Author()
      if auth.startswith('PI: '):
         auth = auth[4:]
         isPI = True
      if isPI:
         a.isPI = True
      m = re.match(pat, auth)
      if m == None:
         sys.stderr.write('Error, unable to match author with regex:%s author:%s\n' % (regex, auth))
         sys.exit(1)
      a.name = m.group(1)
      affs = m.group(2)
      affs = affs.split(',')
      affs = sorted(affs, key=lambda x: int(x))
      a.affiliationsList = affs
      for aff in affs:
         a.affiliationsSet.add(aff)
      authorsList.append(a)
   return authorsList

def printAuthors(authors, options):
   institutions = {} # key name, value order
   i = -1
   piList = []
   for a in authors:
      if a.isPI:
         piList.append(a)
         continue
      i = reportAuthor(a, i, institutions, options)
   for p in piList:
      i = reportAuthor(p, i, institutions, options)
   if options.format == 'paper':
      sys.stdout.write('\n')
   reverseInstitutions = dict((v,k) for k, v in institutions.iteritems())
   for i in xrange(0, len(reverseInstitutions)):
      print '(%d) %s' % (i+1, reverseInstitutions[i])

def reportAuthor(a, i, institutions, options):
   """ a is an author object, i is the index of the current institution
   """
   sys.stdout.write('%s' % a.name)
   instList = []
   for inst in a.affiliationsList:
      if inst not in institutions:
         i += 1
         institutions[inst] = i
      instList.append(institutions[inst])
   # print out the affiliations in sorted order
   instList = sorted(instList, key =lambda x: int(x))
   num = - 1
   for inst in instList:
      num += 1
      if num > 0:
         sys.stdout.write(',%d' % (inst + 1))
      else:
         sys.stdout.write('%d' % (inst + 1))
   if options.format == 'raw':
      sys.stdout.write(' PI:%s\n' % a.isPI)
   elif options.format == 'paper':
      sys.stdout.write(', ')
   return i

def main():
   usage=('usage: %prog affiliations.txt [options]\n\n'
          '%prog takes an affiliations file and parses it into different output formats')
   parser = OptionParser(usage=usage)
   initOptions(parser)
   options, args = parser.parse_args()
   checkOptions(options, args, parser)

   authors = readFile(args[0], options)
   printAuthors(authors, options)

if __name__ == '__main__':
   main()
