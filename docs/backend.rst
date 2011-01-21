=================
API documentation
=================

Fetching an object
==================

``/1/content/<id>``

Fetching a representation of an object
======================================

``/1/content/<id>/<represenation>``

Doing a query on a folderish object
===================================

``/1/content/<id>/query``

with the following parameters:

 * ``limit`` limits the amount of data
 * ``offset`` starts on specific index 
 * ``until`` with a string returns all objects until this date (TODO)
 * ``since`` with a string returns all objects since this date (TODO)
 * ``type`` to get objects with a specific type only
 * ``recursive`` 1 or 0 will go through all sub folders
 * ``fields`` with a list of fields to return 
 * ``view`` will use a view each of the object which needs to be registered
   previously. The default view will just put all fields into a JSON object

