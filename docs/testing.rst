============
Unit testing
============

In order to facilitate automated testing, pydol's unit tests expect the API 
credentials to be stored in a file named ``keys`` in the current working directory.

The file must contain the API key and secret as a json_ object. For example:

::

    {"key": "3d9c6c290-da4c-424e-a378-fb4bd027b58b", "secret": "mysecret11111111111"}
    
.. _json: http://www.json.org/