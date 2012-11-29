#!/usr/bin/env python
# -*- coding: utf-8 -*-
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
# - argparse (part of the standard library in 2.7)
# - beautifulsoup4
# - lxml (Hint for windows users: easy_install lxml==2.3)
# - django (temporary)
#
# TODO list:
# - DONE: Retrieve a list of sentences for a word
# - DONE: Specify a source language for a word, or leave undefined
# - DONE: Specify a target languages for sentence translations, or leave undefined to include all translations
# - DONE: Accept command line parameters for specifying source and target languages, and words
# - DONE: Accept a text file with a list of words
# - Output CSV to stdout or to a file specified on the command line
# - Find a unicode friendly output method that doesn´t depend on django
#
# Possible Future Features:
# - Allow user to specify whether to include all sentences, only the first, random, or prompt (default all)
# - Allow user to specify how the CSV file is output, with some sensible presets
# - Import from other sources besides tatoeba.org
# - Import dictionary definititions for words.
# - GUI
#
import argparse
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
        src_flag = soup.select("img#flag_" + sid)[0]
        translations = []
        translations_div = soup.select("div#_" + sid + "_translations")[0]
        trans_sentences_divs = translations_div.select("div.sentence")
        for div in trans_sentences_divs:
            translations.append({ 'lang': div.select("img.languageFlag")[0]['alt'], 'translation': div.div.a.string})
        sentence = { 'main': link.string, 'main_lang': src_flag['alt'], 'translations': translations }
        sentences.append(sentence)
    return sentences

def get_command_line_parser():
    parser = argparse.ArgumentParser(description='Sentence Miner grabs sentences from a source (currently tatoeba.org) using a word list and outputs a csv file suitable for import into an SRS system like Anki.')
    parser.add_argument('-w', '--word')
    parser.add_argument('-s', '--src-lang', default='und')
    parser.add_argument('-d', '--dest-lang', default='und')
    parser.add_argument('-i', '--infile')
    return parser
    
def output_sentences(sentences):
    for sentence in sentences:
        #smart_str is used because when you output to a file it will throw an exception when printing directly or even using unicode()
        print smart_str(sentence['main_lang'] + ': ' + sentence['main'])
        for t in sentence['translations']:
            print smart_str('\t' + t['lang'] + ':\t' + t['translation'])
        print '----------'
    
def get_words_from_file(infile):
    words = []
    try:
        f = open(infile, 'r')
        for line in f:
            word = line.strip()
            if word != '':
                words.append(word)
        f.close()
        return words
    except:
        print "Error reading from " + infile

def build_output_rows(sentences):
    langs = []
    for sentence in sentences:
        sentence_dict = { sentence['main_lang']: sentence['main'], }
        if not sentence['main_lang'] in langs:
            langs.append(sentence['main_lang'])
        for t in sentence['translations']:
            if not t['lang'] in langs:
                langs.append(t['lang'])
            if t['lang'] in sentence_dict.keys():
                i = 1
                while t['lang'] + str(i) in sentence_dict.keys():
                    i+=1
                sentence_dict[t['lang'] + str(i)] = t['translation']
                if not t['lang'] + str(i) in langs:
                    langs.append(t['lang'] + str(i))
    #TODO: PJC build rows

def output_csv(sentences, outfile):
    rows = build_output_rows(sentences)
    #TODO: PJC output to file using csv module

#main method starts here
if __name__ == "__main__":
    parser = get_command_line_parser()
    args = vars(parser.parse_args())
    if args['word'] != None:
        sentences = get_sentences_for_word(args['word'], args['src_lang'], args['dest_lang'])
        output_sentences(sentences)
    elif args['infile'] != None:
        words = get_words_from_file(args['infile'])
        for word in words:
            sentences = get_sentences_for_word(word, args['src_lang'], args['dest_lang'])
            output_sentences(sentences)            
    else:
        parser.print_help()
