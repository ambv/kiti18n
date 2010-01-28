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
        self.merge = config.merge
        self.merge_conflict = not config.overwrite_conflicts and not config.skip_conflicts
        self.merge_overwrite = config.overwrite_conflicts
        self.merge_skip = config.skip_conflicts
        self.test_only = config.test_only

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
        if len(args) > 1 and args[0] == '':
            args = list(args)
            args[0] = '/' if args[1][0:1] == '/' else '.'

        return re.sub(r'/+', '/', os.sep.join(args))


    def collect_entries(self, path):
        result = {}

        try:
            po = polib.pofile(path)
        except IOError, e:
            self.log('In ', path, ': ', e.strerror)
            return result, None

        for entry in po:
            result[entry.msgid] = entry

        return result, po


    def merge_dicts(self, source, target):
        """ Returns (target_dict, add_count, change_count, remove_count). """

        source_keys = set(source.keys())
        target_keys = set(target.keys())

        # added
        new = source_keys - target_keys
        for key in new:
            target[key] = source[key]

        # removed
        removed = target_keys - source_keys

        # changed
        common = target_keys.intersection(source_keys)

        diff = set()
        for key in common:
            if target[key].msgstr != source[key].msgstr or target[key].msgstr_plural != source[key].msgstr_plural:
                diff.add(key)

        if len(diff) > 0:
            if self.merge_conflict:
                target = None
            elif self.merge_overwrite:
                for key in diff:
                    te = target[key]
                    se = source[key]
                    te.msgstr = se.msgstr
                    te.msgid_plural = se.msgid_plural
                    te.msgstr_plural = se.msgstr_plural
                    te.flags = se.flags
            elif self.merge_skip:
                pass # nothing has to be done
            else:
                self.log("We have a bug.")

        return (target, len(new), len(diff), len(removed))


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


    def merge_pofile(self, base_dir, file_path, merge_with):
        path = self.build_path(base_dir, file_path)
        if os.path.isdir(merge_with):
            merge_path = self.build_path(merge_with, file_path)
        else:
            merge_path = merge_with

        if not (merge_with and os.path.isfile(merge_path)):
            return (0, 0, 0) # or maybe an error?

        # The Merge
        self.logv('Merging ', path, '... ', newline='')
        source, _ = self.collect_entries(path)
        target, target_po = self.collect_entries(merge_path)
        new_target, add_count, change_count, remove_count = self.merge_dicts(source, target)
        self.logv('done.')

        # The Summary
        if new_target == None:
            self.log('CONFLICT; ', newline='')
        else:
            target = new_target
            while len(target_po) > 0:
                del target_po[0]

            for e in target.itervalues():
                target_po.append(e)

            if not self.test_only:
                target_po.save(merge_path)

        self.log(len(target), ' total items. ', add_count, ' new items, ', change_count, ' changed items, ', remove_count, ' removed items: ', file_path, ' -> ', merge_path)

        return add_count, change_count, remove_count


    def merge_dir(self, base_dir, file_path, merge_with):
        path = self.build_path(base_dir, file_path)

        added = 0
        changed = 0
        removed = 0
        for entry in os.listdir(path):
            entry_path = self.build_path(file_path, entry)
            complete_path = self.build_path(base_dir, file_path, entry)
            entry_is_dir = os.path.isdir(complete_path)
            add_count, change_count, remove_count  = self.merge_dir(base_dir, entry_path, merge_with) \
                                                     if self.recursive and entry_is_dir else \
                                                     self.merge_pofile(base_dir, entry_path, merge_with) \
                                                     if entry.endswith('.po') else \
                                                     (0, 0, 0)
            added += add_count
            changed += change_count
            removed += remove_count
        return added, changed, removed


    def start(self, sources=[]):
        target = None

        if self.merge and self.compare:
            print >>sys.stderr, "Merge and compare cannot be run together. Use either -m or -c."
            sys.exit(-1)
        elif self.merge or self.compare:
            if len(sources) < 2:
                print >>sys.stderr, "Wrong number of arguments. Try -h for help."
                sys.exit(-1)
            else:
                target = sources[-1]
                sources = sources[:-1]

        if self.merge:
            added = 0
            changed = 0
            removed = 0
            for s in sources:
                add_count, change_count, remove_count = self.merge_dir(s, '', merge_with=target) \
                                                        if os.path.isdir(s) else \
                                                        self.merge_pofile('', s, merge_with=target)
                added += add_count
                changed += change_count
                removed += remove_count
            self.log('---')
            #self.log('%.2f%% complete; ' % ((1 - 1.0 * problems / entries) * 100), newline='')
            #self.log(problems, ' problems detected.')
        else:
            entries = 0
            problems = 0
            for s in sources:
                entry_count, problem_count = self.analyse_dir(s, '', compare_with=target) \
                                                if os.path.isdir(s) else \
                                                self.analyse_pofile('', s, compare_with=target)
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
    parser.add_argument('-m', '--merge', action='store_true',
                        help='potool will merge the given files or directories. When using -m, there should be '
                        'at least 2 file_or_directory arguments passed. Every entry is merged with the last '
                        'one specified. Overrides .')
    parser.add_argument('-S', '--skip-conflicts', action='store_true',
                        help='when using --merge, potool will skip the entries that are both in source and target '
                        'but differ in content.')
    parser.add_argument('-X', '--overwrite-conflicts', action='store_true',
                        help='when using --merge, potool will overwrite the entries in target that appear both in '
                        'source and target but differ in content.')
    parser.add_argument('-T', '--test-only', action='store_true',
                        help='when using --merge, potool will not write changes to the target but only print the '
                        'changes it would do.')
    values = parser.parse_args()

    POAnalyser(config=values).start(values.file_or_directory)
