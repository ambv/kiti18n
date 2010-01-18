# -*- coding: utf-8 -*-

import sys
import os
import functools
import re

import polib

class POAnalyser(object):

    def __init__(self, config):
        self.recursive = config.recursive
        self.verbose = config.verbose
        self.quiet = config.quiet
        self.ignore_duplicates = config.ignore_duplicates
        self.ignore_occurrences = config.ignore_occurrences
        self.ignore_fuzzy = config.ignore_fuzzy
        self.compare = config.compare

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


    def build_path(self, *args):
        return re.sub(r'/+', '/', os.sep.join(args))


    def count_problems(self, po, log):
        entry_count = 0
        problem_count = 0
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
        return entry_count, problem_count


    def analyse_pofile(self, base_dir, file_path, compare_with):
        path = self.build_path(base_dir, file_path)
        if compare_with:
            if os.path.isdir(compare_with):
                compare_path = self.build_path(compare_with, file_path)
            else:
                compare_path = compare_with

        if not (compare_with and os.path.isfile(compare_path)):
            compare_path = None

        self.logv('Analysing ', path, '... ', newline='')
        try:
            po = polib.pofile(path)
        except IOError, e:
            self.log('In ', path, ': ', e.strerror)
            return 0, 1

        entry_count, problem_count = self.count_problems(po,
                                                         functools.partial(self.logv,
                                                                           'In ',
                                                                           path,
                                                                           ': '))
        po_quality = ((1 - 1.0 * problem_count / entry_count) * 100)

        try:
            compare_po = polib.pofile(compare_path)
            entry_count2, problem_count2 = self.count_problems(compare_po,
                                                               functools.partial(self.logv,
                                                                                 'In ',
                                                                                 compare_path,
                                                                                 ': '))
            po_quality2 = ((1 - 1.0 * problem_count2 / entry_count2) * 100)
        except:
            compare_po = None

        self.logv('done.')

        if problem_count > 0:
            if problem_count == entry_count:
                self.log('EMPTY file; ', newline='')
            else:
                self.log('%.2f%% complete; ' % po_quality, newline='')
            self.log(problem_count, ' problems in ', path, newline='')

        if self.compare and compare_po:
            entry_diff = entry_count2 - entry_count
            problem_diff = problem_count2 - problem_count
            quality_diff = po_quality2 - po_quality
            if entry_diff == 0 and problem_diff == 0:
                self.log(' ; ', compare_path, ' is the same')
            elif quality_diff < 0.01:
                self.log(' ; ', compare_path, ' has the same level of quality')
            else:
                self.log(' ; ', compare_path, ' is ', '%.2f%% better' % quality_diff)
        else:
            self.log()

        return entry_count, problem_count


    def analyse_dir(self, base_dir, file_path, compare_with):
        path = self.build_path(base_dir, file_path)

        entries = 0
        problems = 0
        for entry in os.listdir(path):
            entry_path = self.build_path(file_path, entry)
            complete_path = self.build_path(base_dir, file_path, entry)
            entry_is_dir = os.path.isdir(complete_path)
            if self.recursive and entry_is_dir:
                entry_count, problem_count = self.analyse_dir(base_dir, entry_path, compare_with)
                entries += entry_count
                problems += problem_count
            elif entry.endswith('.po'):
                entry_count, problem_count = self.analyse_pofile(base_dir, entry_path, compare_with)
                entries += entry_count
                problems += problem_count
        return entries, problems


    def analyse(self, sources=[]):
        compare_with = None

        if self.compare:
            if len(sources) < 2:
                print >>sys.stderr, "Wrong number of arguments. Try -h for help."
                sys.exit(-1)
            else:
                compare_with = sources[-1]
                sources = sources[:-1]

        entries = 0
        problems = 0
        for s in sources:
            if os.path.isdir(s):
                entry_count, problem_count = self.analyse_dir(s, '', compare_with)
                entries += entry_count
                problems += problem_count
            else:
                entry_count, problem_count = self.analyse_pofile('', s, compare_with)
                entries += entry_count
                problems += problem_count
        if problems > 0 and entries > 0:
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
    parser.add_argument('-c', '--compare', action='store_true',
                        help='potool will compare the given files or directories. When using -c, there should be '
                        'at least 2 file_or_directory arguments passed. Every entry is compared with the last '
                        'one specified.')
    values = parser.parse_args()

    POAnalyser(config=values).analyse(values.file_or_directory)
