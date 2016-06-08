#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""pydol - A pythonic interface to the U.S. Department of Labor API

Copyright 2016 Sean Whalen

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from hashlib import sha1
from hmac import new as sign
from time import strftime, gmtime
from urllib import urlencode

from requests import get
import xmltodict


__author__ = "Sean Whalen"
__copyright__ = "Copyright (C) 2016 %s" % __author__
__license__ = "Apache 2.0"
__version__ = "1.0.3"


class DOLAPI(object):
    """An interface to the US DOL API"""
    class _DOLAPIError(Exception):
        """A simple exception class for identifying DOL API errors"""
        pass

    def __init__(self, api_key=None, shared_secret=None):
        """Creates an instance of the API handler.
        API credentials are needed for most queries.
        Credentials can be obtained at:
        https://devtools.dol.gov/developer

        @param api_key: Your DOL-generated API key/token
        @param shared_secret: The secret string to provided to the DOL
        """
        self._base_url = "http://api.dol.gov"
        self._api_version = "1"
        self._api_key = api_key
        self._shared_secret = shared_secret

    def _create_auth_header(self, path):
        """Generates the authorization header

        @param path: The URL path requested

        An "authorization string" consists of three parts:

        - The requested URL path, beginning after the top level domain,
        including any parameters. Must match the actual request URL.
        - An ISO 8601 compliant timestamp (in GMT)
        - Your API key

        These values are arranged like HTTP GET parameters:

        {0}&Timestamp={1}&ApiKey={1}

        where {0}, {1}, and {2} are the values for path, Timestamp and
        API Key respectively.

        These values should NOT be URL escaped, with the exception of the URL.

        A HMAC-SHA1 signature is generated using the shared secret as the key,
        and the authentication string as the message.

        The authorization header format is:

        Timestamp={0}&ApiKey={1}&Signature={2}

        where {0}, {1}, and {2} are the values for Timestamp, API Key, and
        Signature respectively.

        Note that the authorization string and the authorization header are
        different.
        """

        # Generate an ISO 8601 compliant timestamp (in GMT)
        timestamp = strftime("%Y-%m-%dT%H:%M:%SZ", gmtime())

        # Construct the authentication string
        auth_string = "%s&Timestamp=%s&ApiKey=%s" % (path,
                                                     timestamp,
                                                     self._api_key)

        # Generate the MAC-SHA1 signature
        signature = sign(key=self._shared_secret,
                             msg=auth_string,
                             digestmod=sha1).hexdigest()

        # Construct the authentication header
        auth_header = "Timestamp=%s&ApiKey=%s&Signature=%s" % (timestamp,
                                                               self._api_key,
                                                               signature)

        return auth_header

    def _request(self, path, url_params="", auth=True, accept_format="json"):
        """Provides a consistent method for fetching data from the API

        @param path: The path to request, starting after the API version
        @param url_params: An optional dictionary of parameters
        @param auth: Specifies whether to provide an Authorization Header
        @param accept_format: The format to request: 'json' or 'xml'.

        @return: A dictionary containing the requested data
        """
        # pylint complains when Requests is used
        # pylint: disable=E1103

        # Be professional. Provide a User-Agent header.
        http_headers = {'User-Agent': 'pydol/%s' % __version__}

        # Add the API version to the URL
        path = "/V%s/%s" % (self._api_version, path)

        # Add the HTTP GET parameters to the URL
        path += "?%s" % urlencode(url_params)

        if auth:
            if self._api_key is None or self._shared_secret is None:
                raise ValueError("API credentials are required.")
            # Add the authorization header
            http_headers['Authorization'] = self._create_auth_header(path)

        # The DOL API returns data in XML default; json may be requested.
        if accept_format == "json":
            http_headers['Accept'] = 'application/json'
        elif accept_format != "xml":
            raise ValueError("Acceptable formats are 'json' or 'xml'")

        # Build the full URL to request
        url = "%s%s" % (self._base_url, path)

        # Make the HTTP GET request
        response = get(url, headers=http_headers)

        # Ensure the correct parser is used. Process API errors.
        if  response.headers['Content-Type'].startswith('application/json'):
            data = response.json()
            if "error" in data:
                error = data['error']['message']['value']
                raise self._DOLAPIError(error)
            elif 'd' in data:
                # Remove useless wrapper
                data = data['d']

        elif response.headers['Content-Type'].startswith('application/xml'):
            data = xmltodict.parse(response.content)
            if "error" in data:
                error = data['error']['message']['#text']
                raise self._DOLAPIError(error)

        # Heed generic HTTP errors
        if response.status_code == 400:
            raise self._DOLAPIError("400 - The query contains an error")
        elif response.status_code == 401:
            raise self._DOLAPIError("401 - Credentials are missing or invalid")
        elif response.status_code == 404:
            raise self._DOLAPIError("404 - Dataset name or table name invalid")

        return data

    def metadata(self, dataset):
        """Returns a dictionary containing detailed metadata about a given
        dataset. The dictionary is converted from XML using xmltodict, so the
        keys are a bit strange. The DOL API does not provide this metadata in
        json. API credentials are not required to use this method."""

        return self._request("/%s/$metadata" % dataset,
                             auth=False,
                             accept_format="xml")

    def table(self,
              dataset,
              table,
              top=100,
              skip=0,
              fields="",
              order_by="",
              filters=""):
        """Returns data from the specified table as a list of dictionaries

        @param dataset: The dataset in which the desired table resides
        @param table: The table to query
        @param top: The maximum number of records to return. Optional.
        @param skip: Skip the specified number of records. Optional.
        @param fields: Return only the fields specified in a list. Optional.
        @param order_by: The field to sort the data by. Optional.
        @param filters: A conditional string to sort the data by. Optional.

        @attention: API credentials are required
        @attention: No more than 100 records will ever be returned at once

        @note: If a database has a multipart name, seperate it with a /
        @note: The records can be paginated by using top and skip

        @note: Each dictionary in the list is an entry from the table
        @note: Each dictionary contains a key for __metadata and for each field
        """

        # Tell pylint to ignore the large number of arguments
        # pylint: disable=R0913

        url_params = {
                    '$top': top,
                    '$skip': skip,
                    '$select': ','.join(fields),
                    '$orderby': order_by,
                    "$filter": filters
                    }

        path = "%s/%s" % (dataset, table)

        return self._request(path, url_params=url_params)


if __name__ == '__main__':
    print __doc__
