===
Ceg
===

|made-with-python-badge|  |github-license-badge|  |github-release-badge|  |pr-welcomed-badge|  |codacy-grade-badge|


.. |made-with-python-badge| image:: https://img.shields.io/badge/Made%20with-Python-1f425f.svg
   :target: https://www.python.org/
   
.. |github-license-badge| image:: https://img.shields.io/github/license/justaus3r/ceg.svg
   :target: https://github.com/justaus3r/ceg/blob/master/LICENSE 

.. |github-release-badge| image:: https://img.shields.io/github/release/justaus3r/ceg.svg
   :target: https://github.com/justaus3r/ceg/releases

.. |pr-welcomed-badge| image:: https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square
   :target: https://makeapullrequest.com


.. |codacy-grade-badge| image:: https://app.codacy.com/project/badge/Grade/25f4e16fd7b74d9ca6309d6b2d31362c
   :target: https://www.codacy.com/gh/Justaus3r/ceg/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=Justaus3r/ceg&amp;utm_campaign=Badge_Grade


Overview
========
-   `Introduction`_
-   `Installation`_
        - `From PYPI using pip`_
        - `From PYPI using pipx`_
        - `Manually`_
-   `Usage`_
-   `Examples`_
        - `Creating a gist`_
        - `Modifying an existing gist`_
        - `Listing public/secret(private) gists`_
        - `Downloading a gist`_
        - `Deleting a gist`_
        - `Backing up all gists`_
        - `Silent mode`_
-   `Similar Projects`_
-   `Issues`_
-   `Contribution`_
-   `Support`_
-   `License`_

Introduction
------------
A gist **<c**>reate/**<r**>ead/**<u**>pdate/**<d**>elete (crud) utility(pronounced as *Keg*). *sounds boring?*  let me try again: it's a command-line `snippet`_ (being called a gist in github's terminology) manager .it can perform all the operations,you would want to perform on a gist.this includes:

1. Creating gist(s).
2. Modifying existing gist(s).
3. Downloading gist(s). [1]_
4. Listing public/secret gists for authenticated users as well as for unauthenticated users(only public).
5. Deleting gist(s).
6. Creating a local backup of all the gists(for authenticated users).

ceg can also be used as a library. check out `Api documentation`_.

.. [1] As of now, only files smaller than 10MB can be downloaded as allowed by GitHub API.this is planned to change once "git clone" has been implemented internally in future releases.


Installation
------------
From PYPI using pip
~~~~~~~~~~~~~~~~~~~
The simplest way to install ceg with battery included is by using pip:
::

    # py instead of python3 on windows
    # Please be sure to use the -U tag to install
    # the latest version as builds are automatically done at github
    # and all patches are pushed to new releases.
    python3 -m pip install -U ceg

From PYPI using pipx
~~~~~~~~~~~~~~~~~~~~
You can also use `pipx`_ if you plan to only use ceg as a command line tool.pipx ensures dependency isolation and is made specifically for cli tools. but please be aware that you will not be able to use ceg as a library if installed from pipx since its installed in a virtenv.
::

    python3 -m pipx install --system-site-packages ceg


Manually
~~~~~~~~
You can also install ceg manually. for that, you need to have poetry_ installed and be on a system with a minimal python version being ``3.7`` (one thing to keep in mind is that i am using python 3.10 so you will need to change python version in pyproject.yaml to your version and build it with that).after installing poetry, you can just do ``poetry build`` and pip install from ``dist/ceg*.whl`` or whatever you prefer. however please be mindful that installing poetry from pip is `not recommended`_. 
::

    # you can also use install/uninstall scripts after cloning the repo, if on *nix.
    curl -sSL https://install.python-poetry.org | python3 - 
    git clone https://github.com/justaus3r/ceg.git 
    cd ceg
    poetry install
    poetry build

After installation, you can optionally set an environment variable named ``GITHUB_SECRET_KEY`` and save your GitHub secret there. this helps to preclude you from passing your key explicitly every time you use the utility. however, if you don't feel comfortable storing it in an environment variable, you can use ``-sk/--secret-key`` and pass it to the utility.


Usage
-----
::

   usage: ceg [options] [sub-arguments]

   An all in one github's gist manager.

   options:
     -h, --help            show this help message and exit
     -po GISTNAME [GISTNAME ...], --post GISTNAME [GISTNAME ...]
                           create a gist
     -pa GISTNAME [GISTNAME ...], --patch GISTNAME [GISTNAME ...]
                           modify an existing gist
     -g GISTID [GISTID ...], --get GISTID [GISTID ...]
                           download gist(s)
     -d GISTID [GISTID ...], --delete GISTID [GISTID ...]
                           remove gist(s)
     -l [OPT-USERNAME], --list [OPT-USERNAME]
                           list public/private gists for a user
     -bk [OPT-USERNAME], --backup [OPT-USERNAME]
                           create a backup of all gists
     -sk SECRETKEY, --secret-key SECRETKEY
                           user's github secret key
     -nl, --no-logging     don't log anything to stdout
     -v, --version         show utility's semantic version

   sub-arguments:
     --post/-po
         --no-public/-np        switch gist visibility to private

         --description/-desc    description for the gist

     --patch/-pa
         --gist-id/-gi          gist-id for the gist

   For more usage help, check out https://www.github.com/justaus3r/ceg/#examples

Examples
--------
Creating a gist
~~~~~~~~~~~~~~~
You can create a gist with multiple files added at the same time. but please know that if your files have a naming scheme like ``gistfile{number}``, it will be
ignored by ceg as GitHub uses this naming scheme internally. for creating a secret gist, you can just append ``--no-public/-np`` in the argument list.
::
    
    $ ceg --post "file1" "file2" -desc "This is description of the gist"

Modifying an existing gist
~~~~~~~~~~~~~~~~~~~~~~~~~~
Modifying a gist is just as easier as creating a gist. just pass all the modified files to ceg and the ``gist-id`` of gist you are modifying(use ``--gist-id/gi``).
you can also update the gist description by passing ``--description/-desc NEWDESCRIPTION``.
::
    # use '->' for renaming files
    $ ceg --patch "file1->file1_renamed" "file2" -desc "My dirty secrets." -gi abcdef

*From v0.4.0 ownwards your files doesn't have to be in running directory of ceg, i.e: you can use files from other directories by giving their path.*

Listing public/secret(private) gists
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
You can list all of your gists, which will be beautified before printing to stdout. please note that if you are not authenticated(not giving GitHub secret key) then you can use ``--list-other/-lo`` but you will only be shown public gists. [1]_
::

    $ ceg -l
      # or
      ceg -lo "Justaus3r"
      # 0.5.0 ownwards
    $ ceg -l "user:Justaus3r"

.. [1] This syntax has been changed ownwards 0.5.0.

Downloading a gist
~~~~~~~~~~~~~~~~~~
You can download an arbitrary amount of gists in one go! just pass their ``gist-id``, sit back and let the magic happen! all of the gists will be downloaded in directories named with their respective gist-ids.
::
    
    $ ceg -g gistid1 gistid2 gistid3
      # or(0.5.0 ownwards)
      ceg -g "user:Justaus3r" gistid1 gistid2
      
**Note**: changed in 0.5.0. now unauthenticated users can also download gists(public only).

Deleting a gist
~~~~~~~~~~~~~~~
You can delete multiple gists by simpling passing their ``gist-id``.
::

    $ ceg -d gistid1 gistid2

Backing up all gists
~~~~~~~~~~~~~~~~~~~~
All user gists can be backed up, only by using a single command.
::

    $ ceg -bk
      # or (0.5.0 ownwards)
      ceg -bk "user:Justaus3r"

Silent mode
~~~~~~~~~~~
All operations can be performed under the silent mode, under which the logger is turned off and nothing(including errors) is printed to stdout.
::
    
    $ ceg -l -nl

Similar Projects
~~~~~~~~~~~~~~~~
Is ceg not your taste? well then you can try following similar projects:

1. `defunkt/gist`_
2. `ropensci/gistr`_ 
3. `jswank/gister`_
4. `hackjutsu/Lepton`_

Issues
------
You can report all issues/feature requests at `GitHub bug tracker`_.

Contribution
------------
.. |strikestart| raw:: html

    <strike>

.. |strikeexit| raw:: html

    </strike>
    
All kinds of contributions are welcomed. though please be mindful that this project is statically typed and uses black formatting so please type-check(using ``mypy``) before a PR. I haven't yet added ``py.typed``, nor is the project type-checked at installation |strikestart| or any workflows setup to do so |strikeexit| (now we actually do type checking using workflow) because I am too lazy. tho I plan to do that. also, note that
`conventional commits`_ and `semantic versioning`_ are used for git commits/versioning.


Support
-------
if you like the project, you can show appreciation by giving it a star.

License
-------
This project is distributed under "GNU General Public License v3.0",and can be distributed with its later versions.

.. _`Api documentation`: https://justaus3r.github.io/ceg/ceg.html
.. _PYPI: https://pypi.org/project/ceg/
.. _poetry: https://python-poetry.org/docs/master/#installing-with-the-official-installer
.. _`not recommended`: https://python-poetry.org/docs/#alternative-installation-methods-not-recommended
.. _`GitHub bug tracker`: https://github.com/justaus3r/ceg/issues/
.. _`conventional commits`: https://www.conventionalcommits.org/en/v1.0.0/
.. _`semantic versioning`: https://semver.org/
.. _`defunkt/gist`: https://github.com/defunkt/gist
.. _`ropensci/gistr`: https://github.com/ropensci/gistr
.. _`jswank/gister`: https://github.com/jswank/gister
.. _`hackjutsu/Lepton`: https://github.com/hackjutsu/Lepton
.. _`pipx`: https://github.com/pypa/pipx/
.. _`snippet`: https://en.wikipedia.org/wiki/Snippet_(programming)
