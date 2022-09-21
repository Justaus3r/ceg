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
""" Main implementation of ceg """

import os
import json
import requests
from .logger import Logger
from rich.tree import Tree
from rich.console import Console
from .exceptions import GenericReturnCodes, CegExceptions
from .misc import Misc, FileHandler, open_file, gist_filename_validated
from typing import List, Tuple, Dict, Optional, Union, Callable

console: Console = Console()

__all__ = ("Ceg",)


class AuxSequence(List):
    """An Auxiliary sequence.

    An Auxiliary Sequence that structurally saves stdout for
    delivering api.

    Attributes:
    single_item_dict: A dictionary containing elements of single gist.
    """

    def __init__(self) -> None:
        self.single_item_dict: Dict[str, Union[str, List[str]]] = {}

    def append(
        self,
        writable: Optional[Union[str, Tree, Dict[str, List[str]]]],
        iteration_complete: bool = False,
    ) -> None:
        """Overloads the append method of List

        Receives (unsanitized) data which is added to
        a mapping,which is then appended to the
        sequence itself.

        Args:
        writable: Actual stream which is to be stored.
        iteration_complete: A boolean acting as a delimiter for gists.
        """
        if isinstance(writable, Dict):
            self.single_item_dict.update(writable)
        else:
            key, val = writable.split(":")  # type: ignore
            self.single_item_dict.update({key: val})
        if iteration_complete:
            single_item_dict_copy = self.single_item_dict.copy()
            super().append(single_item_dict_copy)
            self.single_item_dict.clear()


class WriteStdout:
    """Write stdout to an initialized resource.

    Implements the "write stdout" functionality.It writes the stdout to an initialized resource.

    Attributes:
        to_stdout: A bool indicating whether to write to stdout or not.
        stream_cache: A list containing all gists info.
        write_stdout: A Callable which either writes to stdout or stream_cache.
    """

    def __init__(self, to_stdout: bool) -> None:
        """Inits WriteStdout with appropriate attributes"""
        self.to_stdout: bool = to_stdout
        self.stream_cache: AuxSequence = AuxSequence()
        self.write_stdout: Callable[
            [Optional[Union[str, Tree, Dict[str, List[str]]]], bool], None
        ]
        # mypy was being bitchy when using ternary operator so ...
        # related issue: https://github.com/python/mypy/issues/10740
        if self.to_stdout:
            self.write_stdout = lambda writable, _: console.print(writable)
        else:
            self.write_stdout = self.stream_cache.append

    def __call__(
        self,
        writable: Optional[Union[str, Tree, Dict[str, List[str]]]] = None,
        is_rule: bool = False,
        silent: bool = False,
        text_style: Optional[str] = None,
        iteration_complete: bool = False,
    ) -> None:
        """Implements dunder call

        Calls the actual write_stdout method after evaluation.

        Args:
            writable: A string or Tree object.
            is_rule: A boolean indicating if the writable is a rule object.
            is_tree: A boolean indicating if the writable is a Tree object.
            silent: A boolean indicating whether to waste the write_stdout
                    call(mostly while self.to_stdout is False and we don't
                    want to print the rule).
            text_style: Contains the styling string.

        """
        if isinstance(writable, Tree) and not self.to_stdout:
            tree_dict: Dict[str, List[str]] = {"Files": []}
            retreive_file: Callable[
                [Tree], str
            ] = lambda tree_obj: tree_obj.label  # type: ignore
            tree_files: List[str] = list(map(retreive_file, writable.children))
            tree_dict["Files"] = tree_files
            writable = tree_dict
        if not silent:
            writable = text_style + writable if text_style and self.to_stdout else writable  # type: ignore
            self.write_stdout(
                writable, iteration_complete
            ) if not is_rule else console.rule(
                writable  # type: ignore
            )


class Ceg:
    """Main implementation of ceg.

    The Ceg class actually contains the main implementation
    of the utility.

    Attributes:
        http_operation: A Callable that actually performs the http calls.
        arg_val: A string that is used as argument value as well as a switch for operation resolution.
        is_recursive_op: A boolean indicating if the operation is recursive.
        header: A Dict containing the HTTP header.
        end_point: Endpoint for api calls.
        payload: payload containing data for post requests.
        to_stdout: boolean indicating whether to send data to stdout.
        gist_no_public: boolean indicating if a gist is private.
        is_other: boolean indicating if to list gists for unauth user.
        gist_description: String containing gist description which can be used in patch(),post().
        gist_id: String containing gist-id.
        response_status_str: Contains HTTP call response status in string format.
        logger: Logger object.
    """

    def __init__(
        self,
        operation: str,
        arg_value: Optional[Union[str, Tuple[str, ...]]],
        is_recursive_operation: bool,
        is_other_user: bool,
        secret_key: Optional[str],
        do_logging: bool,
        gist_no_public: bool,
        gist_desc: Optional[str],
        gist_id: Optional[str],
    ) -> None:
        """Inits Ceg with appropriate attributes"""
        self.http_operation: str = operation
        self.arg_val: Optional[Union[str, Tuple[str, ...]]] = arg_value
        self.to_stdout: bool = do_logging
        self.is_recursive_op: bool = is_recursive_operation
        self.is_other: bool = is_other_user
        self.gist_no_public: bool = gist_no_public
        self.gist_description: Optional[str] = gist_desc
        self.gist_id: Optional[str] = gist_id
        self.response_status_str: str = ""
        self.header: Dict[str, str] = {
            "Authorization": f"token {secret_key}",
            "Accept": "application/vnd.github+json",
        }
        self.end_point: str = "https://api.github.com/gists"
        self.payload: Dict[str, Union[Dict[str, Dict[str, str]], bool, str]] = {}
        self.logger: Logger = Logger(send_log=do_logging)

    def __send_http_request(
        self,
        end_point: Optional[str] = None,
        header: Optional[Dict[str, str]] = None,
        params: Optional[str] = None,
        no_header: bool = False,
    ) -> Union[int, List[Dict[str, Union[str, Dict[str, str], None, bool, int]]]]:
        """sends the actual http request with params

        Sends the actual http request with metadata and returns the response.

        Args:
            end_point: optional endpoint string.
            header: optional header for the request.
            params: Optional paramters for the request.

        Returns:
            Returns http call return-code or json formatted response.
        """
        if end_point is None:
            end_point = self.end_point
        if header is None:
            header = self.header
        http_operation = getattr(requests, self.http_operation)
        response: requests.models.Response = (
            http_operation(url=end_point, data=params, headers=header)
            if not no_header
            else http_operation(url=end_point, data=params)
        )
        self.response_status_str = self.__response_validator(response)
        return_var: Union[
            int, List[Dict[str, Union[str, Dict[str, str], bool, int, None]]]
        ]
        if self.http_operation in ["get", "post"]:
            response_hashtable = json.loads(response.content.decode("utf-8"))
            if self.http_operation == "get":
                return_var = response_hashtable
            else:
                return_var = response_hashtable.get("html_url")
        elif self.http_operation in ["patch", "delete"]:
            return_var = response.status_code

        return return_var

    def __response_validator(self, response: requests.models.Response) -> str:
        """Validates the response

        Takes http response as argument and checks to see if its valid,returns the response string,otherwise raises
        respective exception.

        Args:
            response: Http response
        Returns:
            Response status string.

        """
        try:
            http_response_codes: Misc.HttpResponseCodes = Misc.http_response_codes
            response_str: str
            exception_obj_dict: Dict[str, Misc.OptionalException]
            response_str, exception_obj_dict = tuple(
                http_response_codes[response.status_code].items()  # type: ignore
            )[0]
            exception_obj = exception_obj_dict.get("exception_obj")
            response_action: Callable[
                [Misc.OptionalException], None
            ] = http_response_codes.get(  # type: ignore
                "exception_action"
            )
            response_action(exception_obj)
        except KeyError:
            raise CegExceptions.InternalException(
                "Undefined Response!.please open an issue on github."
            )

        return response_str

    def list(
        self,
        end_point: Optional[str] = None,
        header: Optional[Dict[str, str]] = None,
        no_header: bool = False,
    ) -> Optional[List[Dict[str, str]]]:
        """lists public/private gists for authenticated user.

        Performs GET operation on endpoint and retrieves all the public/private gists and propagates the formatted
        response to standard stream.

        Args:
            end_point: optional endpoint string.
            header:    optional header for the request.

        Returns:
            (Optionally) returns a list containing all gists.
        """
        if end_point is None:
            end_point = self.end_point
        if header is None:
            header = self.header

        hashtable_response: Union[
            int, List[Dict[str, Union[str, Dict[str, str], None, bool, int]]]
        ] = (
            self.__send_http_request(end_point, header)
            if not no_header
            else self.__send_http_request(end_point, no_header=True)
        )

        write_stdout: WriteStdout = WriteStdout(self.to_stdout)
        for gist_no, gist_hashtable in enumerate(hashtable_response):  # type: ignore
            write_stdout(
                f"Gist#{gist_no}",
                is_rule=True,
                silent=not self.to_stdout,
                text_style="[cyan bold]",
            )
            write_stdout(f"GistId: {gist_hashtable.get('id')}", text_style="[yellow]")
            write_stdout(
                f"Publicity: {'Public' if gist_hashtable.get('public') else 'Private'}",
                text_style="[blue]",
            )
            write_stdout(
                f"Description: {gist_hashtable.get('description')}",
                text_style="[grey58]",
            )
            file_tree: Tree = Tree(
                "[bold magenta]Files", guide_style="green underline2"
            )
            for file_name, file_hashtable in gist_hashtable.get(
                "files"
            ).items():  # type: ignore
                file_tree_branch: Tree = file_tree.add(file_name)
                file_tree_branch.add(
                    f"Filesize: {file_hashtable.get('size')} bytes"  # type: ignore
                )
                file_tree_branch.add(
                    f"Language: {file_hashtable.get('language')}"  # type: ignore
                )
                file_tree_branch.add(f"Created at: {gist_hashtable.get('created_at')}")
                file_tree_branch.add(f"Updated at: {gist_hashtable.get('updated_at')}")
            write_stdout(file_tree, iteration_complete=True)
            write_stdout(is_rule=True, silent=not self.to_stdout)
        if not self.to_stdout:
            return write_stdout.stream_cache
        # welp mypy wants explicit return statement
        else:
            return None

    def get(self, **kwargs) -> None:
        """Download gists using gist-ids as argument.

        This method downloads all the gists given on cli. backup() also uses this method internally.

        Args:
            **kwargs = Auxiliary arbitrary keyword arguments.
        """
        gist_id: Optional[str]
        do_logging: Optional[bool]
        bypass_recursion: Optional[bool]
        gist_id = kwargs.get("gist_id")
        do_logging = kwargs.get("logging_status")
        bypass_recursion = kwargs.get("bypass_recursion")
        hashtable_response: Union[
            int, List[Dict[str, Union[str, Dict[str, str], None, bool, int]]]
        ]
        if gist_id is not None:
            self.logger.info(
                f"Inquiring for gist with id '{gist_id}'", send_log=do_logging
            )
        hashtable_response = self.__send_http_request(self.end_point, self.header)
        gist_ids: List[str] = [
            gist.get("id")  # type: ignore
            for gist in hashtable_response  # type: ignore
        ]

        gist_id_list: List[str] = (
            gist_ids if self.is_recursive_op else self.arg_val  # type: ignore
        )
        if not bypass_recursion:
            do_logging = False if self.is_recursive_op else True
            for gist in gist_id_list:
                self.get(gist_id=gist, bypass_recursion=True, logging_status=do_logging)
            return None
        try:
            gist_id_index: int = gist_ids.index(gist_id)
        except ValueError:
            raise CegExceptions.ResourceNotFound("The Inquired Gist was not found!")
        self.logger.info("Gist Found!", send_log=do_logging)
        gist_files: List[Tuple[str, str]] = [
            (key, value)
            for key, val in hashtable_response[gist_id_index]  # type: ignore
            .get("files")
            .items()
            if (value := val.get("raw_url")) is not None  # type: ignore
        ]
        file_handler: FileHandler = FileHandler(dir_name=gist_id)
        self.logger.info(
            "Downloading and organizing all the files!", send_log=do_logging
        )
        for single_gist in gist_files:
            try:
                file_name: str
                file_url: str
                file_name, file_url = single_gist
                file_content = requests.get(url=file_url).content.decode("utf-8")
                file_handler.write(file_name, file_content)
            except requests.exceptions.ConnectionError:
                file_handler.return_code = 1
                raise requests.exceptions.ConnectionError(
                    "Connection Error!,please check your internet connection."
                )
        self.logger.info("Sucessfully downloaded the gist!", send_log=do_logging)

    def post(self, **kwargs) -> Optional[str]:
        """Create gists.

        Creates arbitrary number of gists depending on files given on cli.

        Args:
            **kwargs: Auxiliary arbitrary keyword arguments.

        Returns:
            (Optionally) return html url of the newly created gist
        """
        is_patch: Optional[bool]
        new_filenames: Optional[Dict[str, str]]

        is_patch = kwargs.get("is_patch")
        new_filenames = kwargs.get("new_filenames")

        op_success_msg: Dict[str, str] = {"post": "published", "patch": "updated"}
        all_files_validate: bool = True
        files_to_ignore: List[str] = []
        file_to_content_map: Dict[str, Dict[str, str]] = {}
        for file in self.arg_val:  # type: ignore
            if not os.path.exists(file):
                self.logger.info(
                    f"{file} not found in given path,opening in default editor.."
                )
                ret_code: int = open_file(file)
                if ret_code != 0:
                    self.logger.warning(
                        f"An Error occured while opening '{file}' in default editor."
                    )
            self.logger.info(f"Validating filename for '{file}'")
            file_basename: str = os.path.basename(file)
            validated: bool = gist_filename_validated(file_basename)
            if not validated:
                all_files_validate = False
                self.logger.warning(f"{file} will be ignored!")
                files_to_ignore.append(file)
                continue
            with open(file, "r") as r_obj:
                file_content: str = r_obj.read()
            file_to_content_map.update({file_basename: {"content": file_content}})
            if is_patch and new_filenames.get(file_basename):  # type: ignore
                file_to_content_map[file_basename].update(
                    {"filename": new_filenames.get(file_basename)}  # type: ignore
                )

        if not all_files_validate:
            self.logger.warning(
                "One or more files were found to have filenames that are prohibited by github and hence will be ignored."
            )
        self.payload.update({"files": file_to_content_map})
        if is_patch is None:
            self.payload.update({"public": not self.gist_no_public})
        if self.gist_description:
            self.payload.update({"description": self.gist_description})
        gist_html_url = self.__send_http_request(params=json.dumps(self.payload))
        self.logger.info(f"Sucessfully {op_success_msg[self.http_operation]} the gist!")
        if self.http_operation == "post":
            if self.to_stdout:
                self.logger.info(f"Gist Url: {gist_html_url}")
            else:
                return gist_html_url  # type: ignore
        return None

    def patch(self) -> None:
        """Modify an existing gist."""
        if self.gist_id is None:
            raise CegExceptions.InsufficientSubArguments("--gist-id missing!")
        new_filename_map: Dict[str, str] = {}
        self.end_point += "/" + self.gist_id

        for file_index, file in enumerate(self.arg_val):  # type: ignore
            try:
                oldname, newname = file.split("->")
                oldname_base: str = os.path.basename(oldname)
                new_filename_map.update({oldname_base: newname})
                self.arg_val[file_index] = oldname  # type: ignore
            except ValueError:
                pass
        self.post(is_patch=True, new_filenames=new_filename_map)

    def delete(self) -> None:
        """Delete an existing gist."""
        endpoint_copy: str = self.end_point
        for gist in self.arg_val:  # type: ignore
            self.logger.info(f"Searching and deleting gist with id '{gist[:4]}...'")
            self.end_point = "{}/{}".format(endpoint_copy, gist)  # type: ignore
            self.__send_http_request()
            self.logger.info("Gist deleted sucessfully!.")

    def backup(self) -> None:
        """Create a local backup of all the gists."""
        self.logger.info("Backing up all gists to local media...")
        dir_handler: FileHandler = FileHandler("GIST-BACKUP")
        os.chdir("GIST-BACKUP")
        try:
            self.get()
        except requests.exceptions.ConnectionError:
            dir_handler.return_code = 1
            raise requests.exceptions.ConnectionError(
                "Connection Error!,please check your internet connection."
            )
        else:
            self.logger.info("Backup successfull!")

    def list_other(self) -> Optional[List[Dict[str, str]]]:
        """Get gists for other users

        This method simply mutates the endpoint and nulls the auth headers and simply calls the list() method.
        Args:
            user_name: github username for the other user.
        Returns:
            (Optionally) returns a list containing all gists.
        """
        user_gist_info: Optional[List[Dict[str, str]]] = self.list(
            end_point=f"https://api.github.com/users/{self.arg_val}/gists",
            no_header=True,
        )
        if not self.to_stdout:
            return user_gist_info
        else:
            return None

    def perform_operation(self) -> int:
        """Wrapper for all the methods

        Performs all the http requests,sorts out data and
        does all the pretty printing using rich.

        Returns:
            Return code used on exit,indicating success or failure.

        Raises:
            ConnectionError: raised due to connection error while sending the http request.
            BadCredentials:  raised due to bad github secret key.
            ResourceNotFound: raised due to inavailability of inquired resource.
        """
        try:
            if self.arg_val is None and not self.is_recursive_op:
                self.list()
            elif self.is_other:
                self.list_other()
            elif self.is_recursive_op:
                self.backup()
            else:
                http_intrinsics = getattr(self, self.http_operation)
                http_intrinsics()
        except (
            CegExceptions.BadCredentials,
            CegExceptions.ResourceNotFound,
            CegExceptions.UnprocessableRequest,
            CegExceptions.InsufficientSubArguments,
            requests.exceptions.ConnectionError,
        ):
            self.logger.exception("An Error has occured!")
            return GenericReturnCodes.FAILURE
        except Exception:
            self.logger.exception(
                "An internal exception has risen!.please open an issue if you think this is a bug"
            )
            return GenericReturnCodes.FAILURE
        else:
            return GenericReturnCodes.SUCCESS
