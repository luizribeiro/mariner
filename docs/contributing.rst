Contributing
============

.. highlight:: bash

Development Environment
-----------------------

If you're interested to help with development, these are rough
instructions on how to build and run everything locally.

The Pi Zero is a bit too slow for development, so I generally build things
on my desktop computer and ``git push`` them to a git repo the Pi to test.

.. code-block:: bash

   $ poetry install --no-dev
   $ cd frontend
   $ yarn install
   $ yarn build
   $ cd ..
   $ poetry run mariner

Running backend tests::

   $ poetry green

Running frontend tests::

   $ yarn --cwd frontend test

Documentation
-------------

The documentation is hosted on the mariner repository itself. Pull
requests for documentation are welcome too! You can build and preview the
documentation with the following commands::

   $ cd docs
   $ make html

Then just open `docs/_build/html/index.html` on your browser.
