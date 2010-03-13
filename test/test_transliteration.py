# -*- coding: utf-8 -*-
"""
Transliteration tests, using py.test. Run as:

$ easy_install -U py
$ py.test
"""
import codecs

from langacore.kit.i18n import translit


def test_transliteration_from_file():
    with codecs.open('./test_transliteration.in', encoding='utf-8') as fin:
        with codecs.open('./test_transliteration.out', encoding='utf-8') as fout:
            line_in = fin.readline()
            line_out = fout.readline()
            line_no = 1
            while line_in and line_out:
                assert translit.any('ru', line_in, input_lang=line_in.split(' -- ')[0]) == line_out, 'Files differ on line %d' % line_no 
                line_in = fin.readline()
                line_out = fout.readline()
                line_no += 1

def _make_transliterations_to_file():
    with codecs.open('./test_transliteration.in', encoding='utf-8') as fin:
        with codecs.open('./test_transliteration.out', 'w', encoding='utf-8') as fout:
            line_in = fin.readline()
            while line_in:
                fout.write(translit.any('ru', line_in, input_lang=line_in.split(' -- ')[0]))
                line_in = fin.readline()
