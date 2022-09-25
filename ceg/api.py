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
Description
-----------

This is the main api of ceg.it internally uses the main implementation of ceg.interface provided to a developer
is a single class named CegApi, which contains all the functionality of ceg.it can be instantiated by providing
github secret key, which can be obtained from developers **``github``** >> **``Settings``** >> **``Developer settings``** >> **``Personal access tokens``**.

Typical usage example
---------------------
Object instantiation:
```
cgi = CegApi(secret_key="abcd")
```
For creating a gist:
```
gist_url = cgi.post("file1.py", "file2.py", "dirty_secrets.verysecurefile", is_private=False, gist_description="bla")
# note that if a file provided as argument does not exist,ceg will automatically create it and open
# it in your default file editor.
```   

For modifying an existing gist:
```
response_str = cgi.patch("file2.py", gist_id="abc")
# you can optionally also modify the gist description using 'gist_description="whatever"'
```

For listing gists for authenticated user:
```
user_gist_list = cgi.list()
```

For list gist for unauthenticated user:
```
user_gist_list = cgi.list_other("username")
```

For downloading a gist:
```
response_str = cgi.get("gistid1", "gistid2")
# note that gist-ids are typically hashes like 'aa5a315d61ae9438b18d'
```

For creating a backup:
```
response_str = cgi.backup()
```

For deleting a gist:
```
cgi.delete("gistid")
# doesn't support batch operation for now 
```

Api Reference
-------------
"""

from .ceg import Ceg
from typing import List, Dict, Optional


class CegApi:
    """Main interface for api.

    Provides the main interface open for api.contains all
    the methods needed to perform all basic operations on gists.

    Attributes:
        ceg_instance: its an instance of Ceg class.which contains the main
                      implementation of ceg utility.
    """

    def __init__(self, secret_key: str) -> None:
        """Inits CegApi with github secret key"""
        self.ceg_instance: Ceg = Ceg(
            operation="",
            arg_value="",
            is_recursive_operation=False,
            is_other_user=False,
            secret_key=secret_key,
            do_logging=False,
            gist_no_public=False,
            gist_desc="",
            gist_id="",
        )

    def get(self, *args: str) -> str:
        """Downloads a gist.

        Receives arbitrary amount gist-ids and downloads them.

        Args:
            *args: Variable lenght argument list containing gist-ids.


        Returns:
            Returns HTTP call response status in string format.
        """
        self.ceg_instance.http_operation = "get"
        self.ceg_instance.arg_val = args
        self.ceg_instance.get()
        return self.ceg_instance.response_status_str

    def post(
        self,
        *args: str,
        is_private: bool = False,
        gist_description: Optional[str] = None
    ) -> str:
        """Create arbitrary number of gists.

        Args:
            *args: variable lenght arguments list containing gist-ids.
            is_private: indicates whether to make gist private.
            gist_description: Description for the gist.

        Returns:
            Returns HTML url for newly created gist.
        """
        self.ceg_instance.http_operation = "post"
        self.ceg_instance.arg_val = args
        self.ceg_instance.gist_no_public = is_private
        self.ceg_instance.gist_description = gist_description
        # type casting because of distinct variable types(i.e Optional[str] and str)
        # and so so mypy will complain if not type casted
        gist_html_url: str = str(self.ceg_instance.post())
        return gist_html_url

    def patch(
        self, *args: str, gist_id: str, gist_description: Optional[str] = None
    ) -> str:
        """Modify arbitrary number of existing gists.

        Args:
             *args: variable lenght arguments list containing gist-names.
             gist_id: gist-id for the gist,that is to be modified.
             gist_description: (Optional) Description for the gist.

        Returns:
            Returns HTTP call response status in string format.
        """
        self.ceg_instance.http_operation = "patch"
        self.ceg_instance.arg_val = list(args) # type: ignore
        self.ceg_instance.gist_description = gist_description
        self.ceg_instance.gist_id = gist_id
        self.ceg_instance.patch()
        return self.ceg_instance.response_status_str

    def delete(self, *args) -> str:
        """Delete an existing gist.

        Args:
        gist_id = arbitrary amount of gist-ids.

        Returns:
            Returns HTTP call response status in string format.
        """
        self.ceg_instance.http_operation = "delete"
        self.ceg_instance.arg_val = args
        self.ceg_instance.delete()
        return self.ceg_instance.response_status_str

    def list(self) -> Optional[List[Dict[str, str]]]:
        """Return gist data for authenticated user.

        Returns:
            Returns a sequence containing list of all the gists of user with some info.
        """
        self.ceg_instance.http_operation = "get"
        return self.ceg_instance.list()

    def list_other(self, user_name: str) -> Optional[List[Dict[str, str]]]:
        """Return gist data for unauthenticated user.

        Args:
            user_name: username for the user.

        Returns:
            Returns a sequence containing list of all the gists of user with some info.
        """
        self.ceg_instance.http_operation = "get"
        self.ceg_instance.arg_val = user_name
        return self.ceg_instance.list_other()

    def backup(self) -> str:
        """Create backup of all gists on local media.

        Returns:
            Returns HTTP call response status in string format.
        """
        self.ceg_instance.http_operation = "get"
        self.ceg_instance.is_recursive_op = True
        self.ceg_instance.backup()
        return self.ceg_instance.response_status_str
