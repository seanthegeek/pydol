===========
pydol
===========

pydol provides a pythonic interface to the `U.S. Department of Labor API`_.
It can be used to fetch official unemployment numbers and other interesting 
data.
::

    from pydol import DOLAPI

    # Create an instance of the API
    DOL = DOLAPI("d9c6c290-da4c-424e-a378-fb4bd027b58b",
                 "mysecret11111111111")

    # Get dataset metadata as a dictionary structure
    # Multi-part dataset names are separated by a /
    BLS = DOL.metadata("statistics/BLS_Numbers")

    # Get table data as a list of dictionaries
    UNEMPLOYMENT = DOL.table("statistics/BLS_Numbers", "unemploymentRate")
    
    # Detailed examples at docs/examples.rst

It is well documented, easy-to-use, `PEP 8`_ compliant, and unit tested. 


Dependencies
============

* Python_ >= 2.6 < 3.0 

* requests_

* xmltodict_


Obtaining API credentials
=========================

Valid API credentials are required to request data from tables. To obtain credentials:

1) `Create a DOL developer account`_  and log in
2) `Create a new token/key`_
    You must provide:

    * A shared secret - I suggest using a subset of `"random" alpha-numeric characters`_
    * An application name
    * An application description
    
4) The token/key will be generated after the submission of the form
    
 *Note*: The words token and key are used interchangeably 
    

This project is not affiliated with or endorsed by the `U.S. Department of Labor`_.
 
 
.. _U.S. Department of Labor API: http://developer.dol.gov/
.. _PEP 8: http://www.python.org/dev/peps/pep-0008/
.. _Python: http://www.python.org/download/
.. _requests: http://docs.python-requests.org/en/latest/index.html
.. _xmltodict: https://github.com/martinblech/xmltodict
.. _Create a DOL developer account: https://devtools.dol.gov/developer/Account/Register
.. _Create a new token/key: https://devtools.dol.gov/developer/Tokens/Create
.. _"random" alpha-numeric characters: https://www.grc.com/passwords.htm
.. _U.S. Department of Labor: http://www.dol.gov