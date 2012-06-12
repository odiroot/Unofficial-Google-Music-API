Incompatible syntax
===================

Context managers
----------------

Example::

    with open(filename, mode="rb") as f:

Proposed solutions:
#. Plain old file operations with explicit ``close`` call.
#. Use without modifications by importing ``with_statement`` from ``__future__`` module.


New ``except`` syntax
---------------------

Example::

    except HTTPError as e:

Proposed solution: replace with old style syntax::

    except HTTPError, e:


New string interpolation with ``{}``
------------------------------------

Example::

    qstring = '?u=0&xt={0}'.format(query_string['xt'])

Proposed solution: replace with old compatible syntax::

    qstring = '?u=0&xt=%s' % query_string['xt']


Python 3 features
-----------------

Print as a function::

    from __future__ import print_function
    print(foo)

Proposed solution: replace with old, expression style::

    print foo


Missing and icompatible modules
===============================

namedtuple
----------
Proposed alternative: replace with casual tuple, use http://code.activestate.com/recipes/500261/

JSON
----
Proposed alternative: simplejson, replace imports::

    import simplejson as json

Validictory
-----------
Uses incompatible syntax.
Proposed solution: remove dependency, custom schema validation or none at all.
Another viable solution: use older version (<0.8)




