#!/usr/bin/env python3

import os, pypandoc

# Build our reStructuredText version of the readme
output = pypandoc.convert('readme.md', 'rst')
f = open('readme.txt','w+')
f.write(output)
f.close()

os.system('./setup.py register')

