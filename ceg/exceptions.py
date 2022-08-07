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
""" Cegs exceptions """


class CegExceptions:
    """All of Cegs exceptions."""

    class BadCredentials(Exception):
        """raised when a bad response like bad auth is risen."""

        def __init__(self, msg: str = "Bad Credentials!") -> None:
            super().__init__(msg)

    class ResourceNotFound(Exception):
        """raised when inquired resource is not found."""

        def __init__(self, msg: str = "Inquired Resource not found!") -> None:
            super().__init__(msg)

    class ForbiddenResource(Exception):
        """raised when forbidden resource is inquired."""

        def __init__(self, msg: str = "Forbidden Resource!") -> None:
            super().__init__(msg)

    class UnprocessableRequest(Exception):
        """raised when a syntatically correct (tho possibly semantically wrong) request is unprocessable by the server."""

        def __init__(self, msg: str = "Unprocessable Request!") -> None:
            super().__init__(msg)

    class InsufficientSubArguments(Exception):
        """raised when sub-arguments are missing from argument list.

        Due to nature of handling of arguments from cli,missing sub-arguments
        are not catched by argparse.
        """

        def __init__(self, msg: str) -> None:
            super().__init__(msg)

    class InternalException(Exception):
        """raised due to internal errors."""

        def __init__(self, msg: str = "Unprocessable Resource") -> None:
            super().__init__(msg)


class GenericReturnCodes:
    """Generic Return Codes

    Contains the commandline return codes.

    Attributes:
        SUCCESS: return code for successfull operation.
        FAILURE: return code incase an error occurs.
    """

    # TODO: for [v0.2.0]: return different exit codes for better script compatibility
    SUCCESS: int = 0
    FAILURE: int = 1
