#!/usr/bin/env python
# encoding: utf-8

from subprocess import call

if __name__ == '__main__':
    call(['python', '-m', 'unittest', 'discover', '--pattern=*.py'])
