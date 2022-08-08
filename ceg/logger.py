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
""" Enhanced Logger for Ceg """

import logging
from rich.logging import RichHandler
from typing import Union, Any, no_type_check


class Logger(logging.Logger):
    """Logger object responsible for logging all the events.

    Inherits from Logger class of stdlib logging library
    and implements the log propagation validation,i.e whether
    logs should be logged to the stdout/stderr.

    Attributes:
    send_log = boolean indicating whether to log or not
    loglevel = indicates the effective log level.
    dateformat = string represrnting datetime format.
    handler = Handler used by the logger.
    """

    def __init__(
        self,
        send_log: bool = True,
        loglevel: Union[int, str] = logging.INFO,
        dateformat: str = "[%X]",
    ) -> None:
        """Inits the Logger"""
        self.formatter: logging.Formatter = logging.Formatter(datefmt=dateformat)
        self.handler: RichHandler = RichHandler()

        self.handler.setFormatter(self.formatter)
        super().__init__(name=__name__, level=logging.INFO)
        super().addHandler(self.handler)
        self.setLevel(logging._checkLevel(loglevel))  # type: ignore
        if not send_log:
            logging.disable(logging.CRITICAL)

    @no_type_check
    def info(self, msg: str, send_log: bool = True, *args: Any, **kwargs: Any) -> None:
        if send_log:
            super().info(msg, *args, **kwargs)

    @no_type_check
    def warning(
        self, msg: str, send_log: bool = True, *args: Any, **kwargs: Any
    ) -> None:
        if send_log:
            super().warning(msg, *args, **kwargs)

    @no_type_check
    def error(self, msg: str, send_log: bool = True, *args: Any, **kwargs: Any) -> None:
        if send_log:
            super().error(msg, *args, **kwargs)
