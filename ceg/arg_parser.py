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
""" Argument parser for ceg """

import sys
import argparse
from .misc import UtilInfo


class ArgumentParser(argparse.ArgumentParser):
    """Reccord arguments from cli.

    Argument parser that inherits from argparse.ArgumentParser
    class and is used for reccording all the arguments from cli.
    """

    def __init__(self) -> None:
        """Inits (Parent) ArgumentParser with program name and description"""
        super().__init__(
            prog=UtilInfo.UTIL_NAME,
            formatter_class=argparse.RawDescriptionHelpFormatter,
            usage=UtilInfo.UTIL_USAGE,
            description=UtilInfo.DESCRIPTION,
            epilog=UtilInfo.EPILOG,
        )

    def reccord_arguments(self) -> argparse.Namespace:
        """Record (possibly) conflicting arguments from commandline.

        arguments that conflict with each other,i.e: not meant to be used
        simultaneously will be reccorded with add_mutually_exclusive_group()
        method while normal arguments will be reccorded with add_argument()
        method.

        Returns:
            Returns the argparse.Namespace object containing all the arguments.

        """
        # TODO: for [v0.2.0 - v1.0.0]: switch for returning enhanced return codes for better script compatibility.
        # TODO: for [v0.2.0 - v1.0.0]: Use pickle to use serialized cache from local storage(Security implications?).
        # TODO: for [v0.2.0 - v1.0.0]: Change arg parser to flask/click or python-poetry/cleo
        group = self.add_mutually_exclusive_group()
        group.add_argument(
            "-po",
            "--post",
            help="create a gist",
            metavar="GISTNAME",
            type=str,
            nargs="+",
        )
        # anonymous auxiliary arguments for --post(some also maybe used for --patch).
        self.add_argument(
            "-np", "--no-public", action="store_true", help=argparse.SUPPRESS
        )
        self.add_argument("-desc", "--description", type=str, help=argparse.SUPPRESS)

        group.add_argument(
            "-pa",
            "--patch",
            help="modify an existing gist",
            metavar="GISTNAME",
            type=str,
            nargs="+",
        )
        # anonymous auxiliary arguments for --patch
        self.add_argument("-gi", "--gist-id", type=str, help=argparse.SUPPRESS)

        group.add_argument(
            "-g",
            "--get",
            help="Download gist(s)",
            metavar="GISTID",
            type=str,
            nargs="+",
        )
        group.add_argument(
            "-d",
            "--delete",
            help="remove gist(s)",
            metavar="GISTID",
            type=str,
            nargs="+",
        )
        group.add_argument(
            "-l",
            "--list",
            help="list public/private gists for authenticated user",
            action="store_true",
        )
        group.add_argument(
            "-lo",
            "--list-other",
            help="list public gists for unauthenticated users",
            metavar="USERNAME",
            type=str,
        )
        group.add_argument(
            "-bk", "--backup", help="create a backup of all gists", action="store_true"
        )
        self.add_argument(
            "-sk",
            "--secret-key",
            help="user's github secret key",
            metavar="SECRETKEY",
            type=str,
        )
        self.add_argument(
            "-nl",
            "--no-logging",
            help="don't log anything to stdout",
            action="store_true",
        )

        self.add_argument(
            "-v",
            "--version",
            help="show utility's semantic version",
            action="version",
            version=f"{UtilInfo.UTIL_NAME} version: {UtilInfo.VERSION}",
        )

        if len(sys.argv) < 2:
            self.print_help()
            sys.exit(1)
        return self.parse_args()
