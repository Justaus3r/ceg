===
Ceg
===


Overview
========
-   `Introduction`_
-   `Installation`_
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
-   `License`_

Introduction
------------
A gist **<c**>reate/**<r**>ead/**<u**>pdate/**<d**>elete (crud) utility(pronounced as *Keg*).it can perform all the operations,you would want to perform on a gist.this includes:

1. Creating gist(s).
2. Modifying existing gist(s).
3. Downloading gist(s). [1]_
4. Listing public/secret gists for authenticated users as well as for unauthenticated users(only public).
5. Deleting a gist. [2]_
6. Creating a local backup of all the gists(for authenticated users).

ceg can also be used as a library. check out `Api documentation`_.

.. [1] As of now, only files smaller than 10MB can be downloaded as allowed by GitHub API.this is planned to change once "git clone" has been implemented internally in future releases.
.. [2] Bulk operation for deleting multiple gists for planned for next release.

Installation
------------
There are multiple ways to install ceg, the simplest one being installing from PYPI_:
::

    # py instead of python3 on windows
    python3 -m pip install ceg


You can also install it manually. for that, you need to have poetry_ installed and be on a system with a minimal python version being ``3.7``.after installing poetry, you can just do ``poetry build`` and pip install from ``dist/ceg*.whl`` or whatever you prefer. however please be mindful that installing poetry from pip is `not recommended`_. 
::

    # you can also use install/uninstall scripts after cloning the repo, if on *nix.
    curl -sSL https://install.python-poetry.org | python3 - 
    git clone https://github.com/justaus3r/ceg.git 
    cd ceg
    poetry install
    poetry build

After installation, you can optionally set an environment variable named ``GIHTUB_SECRET_KEY`` and save your GitHub secret there. this helps to preclude you from passing your key explicitly every time you use the utility. however, if you don't feel comfortable storing it in an environment variable, you can use ``-sk/--secret-key`` and pass it to the utility.


Usage
-----
::

    usage: ceg [options] [sub-arguments]

    A simple gist crud utility.

    options:
      -h, --help            show this help message and exit
      -po GISTNAME [GISTNAME ...], --post GISTNAME [GISTNAME ...]
                            create a gist
      -pa GISTNAME [GISTNAME ...], --patch GISTNAME [GISTNAME ...]
                            modify an existing gist
      -g GISTID [GISTID ...], --get GISTID [GISTID ...]
                            Download gist(s)
      -d GISTID, --delete GISTID
                            remove a gist
      -l, --list            list public/private gists for authenticated user
      -lo USERNAME, --list-other USERNAME
                            list public gists for unauthenticated users
      -bk, --backup         create a backup of all gists
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
    
    $ ceg --patch "file4" "file4" -desc "My dirty secrets." -gi abcdef

Listing public/secret(private) gists
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
You can list all of your gists, which will be beautified before printing to stdout. please note that if you are not authenticated(not giving GitHub secret key) then you can use ``--list-other/-lo`` but you will only be shown public gists.
::

    $ ceg -l
      # or
    $ ceg -lo Justaus3r

Downloading a gist
~~~~~~~~~~~~~~~~~~
You can download an arbitrary amount of gists in one go! just pass their ``gist-id``, sit back and let the magic happen! all of the gists will be downloaded in directories named with their respective gist-ids.
::
    
    $ ceg -g gistid1 gistid2 gistid3

Deleting a gist
~~~~~~~~~~~~~~~
You can delete a gist by simpling passing its ``gist-id``.note that bulk operation is not supported for now.
::

    $ ceg -d gistid

Backing up all gists
~~~~~~~~~~~~~~~~~~~~
All user gists can be backed up, only by using a single command. only authenticated users can use this feature for now but that might change in future releases.
::

    $ ceg -bk

Silent mode
~~~~~~~~~~~
All operations can be performed under the silent mode, under which the logger is turned off and nothing is printed to stdout.
::
    
    $ ceg -l -nl

Similar Projects
~~~~~~~~~~~~~~~~
Is ceg not your taste? well then you can try following similar projects:

1. `defunkt/gist`_
2. `ropensci/gistr`_ 
3. `jswank/gister`_

Issues
------
You can report all issues/feature requests at `GitHub bug tracker`_.

Contribution
------------
All kinds of contributions are welcomed. though please be mindful that this project is statically typed and uses black formatting so please type-check(using ``mypy``) before a PR. I haven't yet added ``py.typed``, nor is the project type-checked at installation or any workflows setup to do so because I am too lazy. tho I plan to do that. also, note that
`conventional commits`_ and `semantic versioning`_ are used for git commits/versioning.

License
-------
This project is distributed under "GNU General Public License v3.0",and can be distributed with its later versions.

.. _`Api documentation`: https://github.com
.. _PYPI: https://pypi.org
.. _poetry: https://python-poetry.org/docs/master/#installing-with-the-official-installer
.. _`not recommended`: https://python-poetry.org/docs/#alternative-installation-methods-not-recommended
.. _`GitHub bug tracker`: https://github.com/justas3r/ceg/issues/
.. _`conventional commits`: https://www.conventionalcommits.org/en/v1.0.0/
.. _`semantic versioning`: https://semver.org/
.. _`defunkt/gist`: https://github.com/defunkt/gist
.. _`ropensci/gistr`: https://github.com/ropensci/gistr
.. _`jswank/gister`: https://github.com/jswank/gister
