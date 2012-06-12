#!/usr/bin/env python
#
# Sentence Miner (sminer)
#
# Sentence Miner grabs sentences from a source (currently tatoeba.org) using a word list
# and outputs a csv file suitable for import into an SRS system like Anki.
#
# Created by Peter Carroll <peter at peterjcarroll dot com> on June 12, 2012
#
# Contributors:
# <insert name here>
#
# TODO list:
# - Retrieve a list of sentences for a word
# - Specify a source language for a word, or leave undefined
# - Specify one or more target languages for sentence translations, or leave undefined to not include translations
# - Accept command line parameters for specifying source and target languages, and words
# - Accept a text file with a list of words
# - Output CSV to stdout or to a file specified on the command line
# - Allow user to specify whether to include all sentences, only the first, random, or prompt (not sure which to default yet)
# - Allow user to specify how the CSV file is output, with some sensible presets
#
# Possible Future Features:
# - Import from other sources besides tatoeba.org
# - Import dictionary definititions for words.
# - GUI
#
import urllib2
from bs4 import BeautifulSoup
from django.utils.encoding import smart_str

page = urllib2.urlopen('http://tatoeba.org/eng/sentences/search?query=plancha&from=spa&to=und').read()
soup = BeautifulSoup(page)
print smart_str(soup.prettify()) #TODO: I dont like depending on django here, find an alternative