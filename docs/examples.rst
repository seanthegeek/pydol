==============
pydol examples
==============

pydol provides a single class_, ``DOLAPI`` that can be used to interact with the DOL API.


Creating an instance
--------------------

To create an instance of ``DOLAPI``, import it from pydol and assign it to a variable.

::

    from pydol import DOLAPI

 	DOL = DOLAPI("d9c6c290-da4c-424e-a378-fb4bd027b58b",
	             "mysecret11111111111")

While you are not required to provide API credentials, they are required for most API requests.


Dataset metadata
----------------

DOL data is grouped into datasets_. Each dataset is given a shortened name.
This shortened name can be found by looking at the location URL listed on the
dataset's page. The shorted name is placed after V1/. For example, the BLS
Numbers dataset has a location of 
``http://api.dol.gov/V1/statistics/BLS_Numbers``, so it's shortened name is
``statistics/BLS_Numbers``.  Use the shortened name when making API calls.

Metadata regarding a dataset and the tables can be obtained by calling the
``metadata`` method. This method takes the shortened dataset name as it's
only argument. For example:

::

    BLS = DOL.metadata("statistics/BLS_Numbers")

The metadata is returned as a dictionary_.

*Note*: The metadata is converted from XML to a dictionary by xmltodict_

*Note*: API credentials are not required


Table data
----------

Data within each dataset in separated into tables. The ``table`` method is
used to retrieve table data. The dataset short name and table name are
required arguments.

::

   UNEMPLOYED = DOL.table("statistics/BLS_Numbers", "unemploymentRate")
   
*Note*:  This method requires valid API credentials
   
The table is returned as a list_ of dictionaries, where each dictionary
represents a table record, and each dictionary key represents a field. 

*Note*: Each dictionary has an additional  entry called ``__metadatadata``
that contains metadata about the respective table record.
 
By default, the ``table`` method will return all fields for the first 100
records in the table. This behaver can be modified by specifying optional
`keyword arguments`_:

``top``
    The maximum number of records to return.

    *Note*: The DOL API will never return more than 100 records at once

``skip``
    Skip the specified number of records. It can be used with ``top`` to
    paginate records.

``fields``
    A list_ of fields to return

``order_by``
    Sorts the data by the specified field
    
    *Note*: Sorts by ascending order by default. To sort by descending order,
    add " desc" after the field name.
    
``filters``
    Filter the data using a specially formatted conditional string
    
    A single filter contains three parts, separated by spaces:
    
    1) A field name
    2) A comparison keyword:

        * eq – Equal to
        * ne – Not Equal to
        * gt – Greater than
        * lt – Less than
        * ge – Greater than or equal to
        
    3) A value surrounded by ``'``
 
    For example:

    ::
    
        type eq 'F'
        
    Two or more filters may be combined by surrounding each filter with a set
    of (), and chaining them together with either and or or.
    For example:

    ::

        (year eq '2012') and (type eq 'F')

.. _class: http://docs.python.org/tutorial/classes.html
.. _datasets: http://developer.dol.gov/
.. _dictionary: http://docs.python.org/tutorial/datastructures.html#dictionaries
.. _xmltodict: https://github.com/martinblech/xmltodict
.. _list: http://www.diveintopython.net/native_data_types/lists.html
.. _keyword arguments: http://docs.python.org/tutorial/controlflow.html#keyword-arguments