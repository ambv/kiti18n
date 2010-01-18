# -*- coding: utf-8 -*-

import sys
import os
import functools

import polib

class POAnalyser(object):

    def __init__(self, config):
        self.recursive = config.recursive
        self.verbose = config.verbose
        self.quiet = config.quiet
        self.ignore_duplicates = config.ignore_duplicates
        self.ignore_occurrences = config.ignore_occurrences
        self.ignore_fuzzy = config.ignore_fuzzy


    def log(self, *args, **kwargs):
        newline = '\n'
        if 'newline' in kwargs:
            newline = kwargs['newline']

        if not self.quiet:
            for arg in args:
                sys.stdout.write(unicode(arg).encode('utf-8'))
            sys.stdout.write(newline)


    def logv(self, *args, **kwargs):
        if self.verbose:
            self.log(*args, **kwargs)


    def analyse_pofile(self, path):
        self.logv('Analysing ', path, '... ', newline='')
        log = functools.partial(self.logv, 'In ', path, ': ')
        entry_count = 0
        problem_count = 0
        po = polib.pofile(path)

        for entry in po:
            entry_count += 1
            if not entry.msgstr:
                problem_count += 1
                log('empty msgstr for ', entry.msgid)
            elif entry.msgid == entry.msgstr:
                if not self.ignore_duplicates:
                    problem_count += 1
                    log('msgstr == msgid for ', entry.msgid)

            if entry.msgid_plural:
                if not entry.msgstr_plural:
                    problem_count += 1
                    log('empty msgstr_plural for ', entry.msgid, '(plural: ', entry.msgid_plural, ')')
                elif entry.msgid_plural == entry.msgstr_plural:
                    if not self.ignore_duplicates:
                        problem_count += 1
                        log('msgstr_plural == msgid_plural for ', entry.msgid, '(plural: ', entry.msgid_plural, ')')
                elif entry.msgid == entry.msgstr_plural:
                    problem_count += 1
                    log('msgstr_plural == msgid for ', entry.msgid, '(plural: ', entry.msgid_plural, ')')
                elif entry.msgstr == entry.msgstr_plural:
                    if not self.ignore_duplicates:
                        problem_count += 1
                        log('msgstr_plural == msgstr for ', entry.msgid, '(plural: ', entry.msgid_plural, ')')

            if 'fuzzy' in entry.flags and not self.ignore_fuzzy:
                    problem_count += 1
                    log('fuzzy translation for ', entry.msgid)

            if entry.obsolete:
                if not self.ignore_fuzzy:
                    problem_count += 1
                    log('obsolete translation for ', entry.msgid)
            elif not entry.occurrences and not self.ignore_occurrences:
                problem_count += 1
                log('no occurences marked for ', entry.msgid)

        self.logv('done.')

        if problem_count > 0:
            if problem_count == entry_count:
                self.log('EMPTY file; ', newline='')
            else:
                self.log('%.2f%% complete; ' % ((1 - 1.0 * problem_count / entry_count) * 100), newline='')
            self.log(problem_count, ' problems in ', path)

        return entry_count, problem_count

    def analyse_dir(self, path):
        entries = 0
        problems = 0
        for entry in os.listdir(path):
            entry_path = path + os.sep + entry
            entry_is_dir = os.path.isdir(entry_path)
            if self.recursive and entry_is_dir:
                entry_count, problem_count = self.analyse_dir(entry_path)
                entries += entry_count
                problems += problem_count
            elif entry.endswith('.po'):
                entry_count, problem_count = self.analyse_pofile(entry_path)
                entries += entry_count
                problems += problem_count
        return entries, problems


    def analyse(self, sources=[]):
        entries = 0
        problems = 0
        for s in sources:
            if os.path.isdir(s):
                entry_count, problem_count = self.analyse_dir(s)
                entries += entry_count
                problems += problem_count
            else:
                entry_count, problem_count = self.analyse_pofile(s)
                entries += entry_count
                problems += problem_count
        if problems > 0:
            self.log('---')
            self.log('%.2f%% complete; ' % ((1 - 1.0 * problems / entries) * 100), newline='')
            self.log(problems, ' problems detected.')

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(prog='potool')
    parser.add_argument('file_or_directory', nargs='+', help='path to a .po file or a directory with .po files')
    parser.add_argument('-r', '--recursive', action='store_true',
                        help='if file_or_directory is a directory, potool will recurse to find .po '
                        'files also in subdirectories')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='potool will spit more useful information on standard output')
    parser.add_argument('-q', '--quiet', action='store_true',
                        help='potool will not write anything to standard output (useful for batching)')
    parser.add_argument('-d', '--ignore-duplicates', action='store_true',
                        help='potool will not count strings where msgid{_plural} equals msgstr{_plural} as problems')
    parser.add_argument('-o', '--ignore-occurrences', action='store_true',
                        help='potool will not count strings with no marked occurrences as problems')
    parser.add_argument('-f', '--ignore-fuzzy', action='store_true',
                        help='potool will not count fuzzy and obsolete translations as problems')
    values = parser.parse_args()

    POAnalyser(config=values).analyse(values.file_or_directory)
