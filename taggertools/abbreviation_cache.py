#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import shutil

class Cache:
    gene = []
    abbreviations = []
    gene_file = None
    abbreviations_file = None

    def __init__(self, name):
        self.name = name

    def setup(self, dir):
        if not os.path.exists(dir):
            os.makedirs(dir)
        self._load(dir)
        self._open(dir, 'a')

    def teardown(self):
        self._close()

    def load(self, dir):
        self._load(dir)

    def _load(self, dir):
        path = Cache.get_gene_filename(dir, self.name)
        if os.path.exists(path):
            with open(path, 'r') as f:
                for w in f:
                    self.gene.append(w.rstrip())
        path = Cache.get_abbreviation_filename(dir, self.name)
        if os.path.exists(path):
            with open(path, 'r') as f:
                for w in f:
                    self.abbreviations.append(w.rstrip())

    def _open(self, dir, mode):
        self.gene_file = open(Cache.get_gene_filename(dir, self.name), mode)
        self.abbreviations_file = open(Cache.get_abbreviation_filename(dir, self.name), mode)

    def _close(self):
        if self.gene_file:
            self.gene_file.close()
        if self.abbreviations_file:
            self.abbreviations_file.close()

    @staticmethod
    def get_gene_filename(dir, name):
        return dir + '/' + name + '.txt'

    @staticmethod
    def get_abbreviation_filename(dir, name):
        return dir + '/' + name + '_abbreviations.txt'

    def add(self, word):
        if len(word) <= 2:
            return
        word = word.lower()
        if word in self.gene:
            return
        self.gene.append(word)
        if self.gene_file:
            self.gene_file.write(word + '\n')
            self.gene_file.flush()

    def add_abbreviation(self, word):
        if len(word) <= 2:
            return
        word = word.lower()
        if word in self.abbreviations:
            return
        self.abbreviations.append(word)
        if self.abbreviations_file:
            self.abbreviations_file.write(word + '\n')
            self.abbreviations_file.flush()

class CacheManager:

    def __init__(self):
        self.service_cache = {}
        self.cache_dir = None

    def set_cache_dir(self, cache_dir):
        self.cache_dir = cache_dir

    def add_abbreviation(self, name, word):
        if name in self.service_cache:
            self.service_cache[name].add_abbreviation(word)

    def add_cache(self, name, word):
        if name in self.service_cache:
            self.service_cache[name].add(word)

    def is_cached(self, word):
        for cache in self.service_cache.values():
            if word in cache.gene:
                return True
        return False

    def is_abbreviation(self, word):
        for cache in self.service_cache.values():
            if word in cache.abbreviations:
                return True
        return False

    def setup(self, name):
        cache = Cache(name)
        cache.setup(self.cache_dir)
        self.service_cache[name] = cache

    def teardown(self):
        for cache in self.service_cache.values():
            cache.teardown()

    def get_files(self, name):
        return [ 
            Cache.get_gene_filename(self.cache_dir, name),
            Cache.get_abbreviation_filename(self.cache_dir, name),
           ]

    def islock(self, name):
        for f in self.get_files(name):
            if os.path.exists(f + '.lock'):
                return True
        return False

    def lock(self, name):
        if not self.islock(name):
            for f in self.get_files(name):
                shutil.copy(f, f + '.lock')

    def unlock(self, name):
        for f in self.get_files(name):
            lockfile = f + '.lock'
            if os.path.exists(lockfile):
                os.remove(lockfile)

    def sort(self, name):
        for f in self.get_files(name):
            if os.path.exists(f):
                words = []
                with open(path, 'r') as f:
                    for w in f:
                        words.append(w.rstrip())
                with open(path, 'w') as f:
                    for w in sorted(set(words)):
                        f.write(w + '\n')

    def load_whitelist(self, name):
        return CacheManager._file_to_list(Cache.get_gene_filename(self.cache_dir, name))

    def load_abbreviationlist(self, name):
        return CacheManager._file_to_list(Cache.get_abbreviation_filename(self.cache_dir, name))

    @staticmethod
    def _file_to_list(path):
        wordlist = []
        with open(path, 'r') as f:
            for line in f:
                word = line.strip()
                wordlist.append(word.lower())
        return wordlist

cache = CacheManager()
