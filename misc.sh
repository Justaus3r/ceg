#! /usr/bin/env bash

updated_ver=`cat ceg/misc.py | grep "VERSION: str" |  python3 -c "import re; inp = input(); print(re.search('\d+\.\d+\.\d+', inp).group())"`

echo "v$updated_ver"
