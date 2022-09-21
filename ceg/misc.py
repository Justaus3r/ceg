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
""" Misc stuff dat i couldn't figure out where to put """

import os
import platform
import subprocess
from .exceptions import CegExceptions
from typing import List, Dict, Callable, Union, Optional, Type, TypeAlias

__all__ = ("UtilInfo", "Misc")


class UtilInfo:
    """Metainfo about utility.

    Class containing all the meta info about
    the utility.

    Attributes:
        UTIL_NAME: The utility name.
        DESCRIPTION: Short description of the utility.
        VERSION: Semantic verson of the utility.
    """

    UTIL_NAME: str = "ceg"
    UTIL_USAGE: str = f"{UTIL_NAME} [options] [sub-arguments]"
    EPILOG: str = """
sub-arguments:
  --post/-po
      --no-public/-np        switch gist visibility to private

      --description/-desc    description for the gist
    
  --patch/-pa
      --gist-id/-gi          gist-id for the gist

For more usage help, check out https://www.github.com/justaus3r/ceg/#examples"""
    DESCRIPTION: str = "A simple gist crud utility."
    # Caution(message to myself): Be careful when updating the version because
    # wrong updates can be a mess.
    VERSION: str = "0.4.1"


def exception_executioner(exception_obj) -> None:
    """Raises exception taken as am argument.

    Args:
        exception_obj: THe Exception object.

    """
    if exception_obj:
        raise exception_obj


class Misc:
    """Misc stuff.

    Contains all the miscellaneous vars.

    Attributes:
    http_intrinsics: List containing names of all http methods.
    secret_key: Gitub Secret key extracted from env variable.
    """

    http_intrinsics: List[str] = ["get", "post", "patch", "delete"]
    OptionalException: TypeAlias = Optional[
        Union[
            Type[CegExceptions.BadCredentials],
            Type[CegExceptions.ForbiddenResource],
            Type[CegExceptions.ResourceNotFound],
            Type[CegExceptions.UnprocessableRequest],
        ]
    ]
    HttpResponseCodes: TypeAlias = Dict[
        Union[int, str],
        Union[
            Dict[str, Dict[str, OptionalException]], Callable[[OptionalException], None]
        ],
    ]
    http_response_codes: HttpResponseCodes = {
        200: {"OK!": {"exception_obj": None}},
        201: {"Gist Created Sucessfully!": {"exception_obj": None}},
        204: {"OK!.No Response Recieved.": {"exception_obj": None}},
        401: {"Bad Credentials!": {"exception_obj": CegExceptions.BadCredentials}},
        403: {
            "Forbidden Resource!": {"exception_obj": CegExceptions.ForbiddenResource}
        },
        404: {"Resource not found!": {"exception_obj": CegExceptions.ResourceNotFound}},
        422: {
            "Request Unprocessable!": {
                "exception_obj": CegExceptions.UnprocessableRequest
            }
        },
        "exception_action": exception_executioner,
    }
    secret_key: Optional[str] = os.getenv("GITHUB_SECRET_KEY")


class FileHandler:
    """File & Directory Handler.

    Responsible for creating gist directories,
    files,writing content to them and removing
    gist directories if found empty due to some
    error.

    Attributes:
        return_code: return code which determines whether to keep a directory or not.
    """

    def __init__(self, dir_name: str) -> None:
        "Inits FileHandler with some directory name"
        self.__dir_name: str = dir_name
        self.__return_code: int = 0
        os.mkdir(self.__dir_name)

    @property
    def return_code(self) -> int:
        return self.__return_code

    @return_code.setter
    def return_code(self, return_code) -> None:
        self.__return_code = return_code
        if self.__return_code == 1:
            if len(os.listdir(self.__dir_name)) == 0:
                os.rmdir(self.__dir_name)

    def write(self, file_name: str, content: str) -> None:
        with open(os.path.join(self.__dir_name, file_name), "w") as wr:
            wr.write(content)


def open_file(file_name: str) -> int:
    """Opens an already existing or
    a new file in default text editor for
    one of the three major os's.

    Args:
        file_name: file to open.

    Returns:
        Returns an integer return code indicating
        if the operation was successfull or not
    """
    try:
        file_obj = open(file_name, "w")
    except PermissionError:
        return 1
    util: str = ""
    cmd: List[str] = [""]
    if platform.system() == "Windows":
        util = "start"
    elif platform.system() == "Linux":
        util = "xdg-open"
        file_obj.write("# Placeholder text.")
    elif platform.system() == "Darwin":
        util = "open"
        cmd.append("-t")
    file_obj.close()
    cmd[0] = util
    cmd.append(file_name)
    ret_code: int = subprocess.run(cmd, stdout=subprocess.DEVNULL).returncode

    return ret_code


def gist_filename_validated(file_name: str) -> bool:
    """Validates the filename.

    Validates and checks if the filename has filename
    pattern prohibited by github and depending so,returns
    a boolean to represent the respective state.

    Args:
        file_name: filename to validate.
    Returns:
        boolean representing the validated state of filename.

    """
    striped_filename: str = file_name.replace("gistfile", "")
    # so the logic here is that if the filename contains 'gistfile'
    # in it then that will be replaced with emtpy string and the filename
    # will change,otherwise it won't change which will help us decide
    # if it does contain that string and if it does then the remaining
    # string will be validated for numerical digits
    if striped_filename != file_name and striped_filename.isdigit():
        return False
    return True
