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
# Dependencies:
# - beautifulsoup4
# - lxml (Hint for windows users: easy_install lxml==2.3)
# - django (temporary)
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
# - Find a unicode friendly output method that doesn´t depend on django
#
# Possible Future Features:
# - Import from other sources besides tatoeba.org
# - Import dictionary definititions for words.
# - GUI
#
import urllib2
from bs4 import BeautifulSoup
from django.utils.encoding import smart_str 

def get_sentences_for_word(word, src_lang = 'und', dest_lang = 'und'):
    url = 'http://tatoeba.org/eng/sentences/search?query=' + word + '&from=' + src_lang + '&to=' + dest_lang
    page = urllib2.urlopen(url).read()
    soup = BeautifulSoup(page, "lxml")
    sentence_links = soup.select("div.mainSentence div.sentenceContent a")
    sentences = []
    for link in sentence_links:
        sid = link['href'].rpartition('/')[2]
        translations = []
        translations_div = soup.select("div#_" + sid + "_translations")[0]
        trans_sentences_divs = translations_div.select("div.sentence")
        for div in trans_sentences_divs:
            translations.append({ 'lang': div.select("img.languageFlag")[0]['alt'], 'translation': div.div.a.string})
        sentence = { 'main': link.string, 'translations': translations }
        sentences.append(sentence)
    return sentences

sentences = get_sentences_for_word('はい')
for sentence in sentences:
    #smart_str is used because when you output to a file it will throw an exception when printing directly or even using unicode()
    print smart_str(sentence['main'])
    for t in sentence['translations']:
        print smart_str('\t' + t['lang'] + ':\t' + t['translation'])
    print '----------'