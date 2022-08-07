# ╔═══╗
# ║╔═╗║
# ║║ ╚╝╔══╗╔══╗
# ║║ ╔╗║╔╗║║╔╗║
# ║╚═╝║║║═╣║╚╝║
# ╚═══╝╚══╝╚═╗║
#          ╔═╝║
#          ╚══╝
# ©Justaus3r 2022
# This file is part of "Ceg",a gist crud utility.
# Distributed under GPLV3
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
Introduction
========
Ceg (as in **c**r**e**ate **g**ist and pronounced *Keg*) is a command-line utility as well as a library for 
interacting with github gists.it uses github's official api for performing all operations.it can:
- Create gists.
- Modify existing gists.
- Download gists.
- List public/private(secret) gists for authenticated users as well as list public gists for unauthenticated users.
- Delete a gist.
- Create local backup of all the gists.

Installation
============
There are multiple ways to install ceg,the simplest one being installing from PYPI:
```
# py instead of python3 on windows
python3 -m pip install ceg
```
You can also install it manually.for that you need to have [``poetry``](https://python-poetry.org/docs/master/#installing-with-the-official-installer) installed and be on a system with minimal python version being 3.7.after installing poetry,you can just 
do `poetry build` and pip install from `dist/ceg*.whl` or whatever you prefer.please be mindful that installing poetry
from pip is [not recommended](https://python-poetry.org/docs/#alternative-installation-methods-not-recommended).
```
# you can also use install/uninstall scripts after cloning the repo, if on *nix.
curl -sSL https://install.python-poetry.org | python3 - 
git clone https://github.com/justaus3r/ceg.git 
cd ceg 
poetry build
```

Now wat?
=======
After installing ceg you can either do ``ceg --help`` in your terminal, check out projects README or refer to api documentation.

**Note:**
Please only refer to submodule named `api` as other files contain reference to main implementation of ceg and such
may contain ambiguous documentation which may or maynot be clear unless codebase is understood.

"""
