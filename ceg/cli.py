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
""" Main cli """

import sys
from .ceg import Ceg
from .misc import Misc
from .arg_parser import ArgumentParser
from typing import Optional, Any


def ceg_cli() -> None:
    """First subroutine to run on execution of utility.

    The main function which reccords the arguments
    and also partially handles them.
    """
    arg_parse_obj: ArgumentParser = ArgumentParser()
    parsed_args = arg_parse_obj.reccord_arguments()
    http_operation: str
    gist_description: Optional[str] = None
    gist_id: Optional[str] = None
    is_recursive: bool = False
    is_other: bool = False
    logging_status: bool = True
    gist_no_public: bool = False
    argument_value: Optional[Any]

    for arg, arg_val in vars(parsed_args).items():
        if arg == "secret_key" and arg_val:
            Misc.secret_key = arg_val
        elif arg == "no_logging" and arg_val:
            logging_status = False
        elif arg == "no_public" and arg_val:
            gist_no_public = True
        elif arg == "description" and arg_val:
            gist_description = arg_val
        elif arg == "gist_id" and arg_val:
            gist_id = arg_val
        elif arg in Misc.http_intrinsics and arg_val:
            http_operation = arg
            argument_value = arg_val
        elif arg in ["list", "backup", "list_other"] and arg_val:
            http_operation = "get"
            is_recursive = True if arg == "backup" else False
            is_other = True if arg == "list_other" else False
            argument_value = None if arg in ["list", "backup"] else arg_val

    ceg_obj = Ceg(
        operation=http_operation,
        arg_value=argument_value,
        is_recursive_operation=is_recursive,
        is_other_user=is_other,
        secret_key=Misc.secret_key,
        do_logging=logging_status,
        gist_no_public=gist_no_public,
        gist_desc=gist_description,
        gist_id=gist_id,
    )
    return_code: int = ceg_obj.perform_operation()
    sys.exit(return_code)
