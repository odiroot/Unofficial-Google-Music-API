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


Python 3 features
-----------------

Print as a function::

    from __future__ import print_function
    print(foo)

Proposed solution: replace with old, expression style::

    print foo

