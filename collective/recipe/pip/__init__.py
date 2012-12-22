# -*- coding: utf-8 -*-
"""Recipe pip."""
import os
import itertools

class Recipe(object):
    """zc.buildout recipe"""

    def __init__(self, buildout, name, options):
        self.options = options
        self.process()

    def install(self):
        """Installer"""
        return tuple()

    def process(self):
        """Process everything"""
        self.options['eggs'] = "\n".join(self.parse_files(self.options.get('configs').split()))

    def parse_files(self, files):
        """Parse files."""
        return itertools.chain.from_iterable(itertools.imap(self.parse_file, files))

    def parse_file(self, file):
        """Parse single file."""
        return itertools.chain.from_iterable(itertools.imap(self.parse_line, open(file).xreadlines()))

    def parse_line(self, line):
        """Parse single line."""
        if any(map(line.startswith, ('#', '-f'))):
            raise StopIteration()

        for token in line.split():
            yield self.parse_token(token)

    def parse_token(self, token):
        """Parse single token"""
        if token and not token[0] in ('-', '#'):
            if '#egg=' in token:
                return token.split('#egg=')[1]
            if '#' in token:
                raise StopIteration()
            return token
        raise StopIteration()

    update = install

