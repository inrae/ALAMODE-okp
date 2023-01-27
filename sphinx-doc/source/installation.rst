Installation
============

Requirements and dependencies
-----------------------------
You need Python 3.5 or later to run the ``okplm`` package. You can have
multiple Python versions (2.x and 3.x) installed on the same system
without problems using, for example, virtual environments.

You may use ``pip`` to install the required packages.

.. note:: In Windows, to use ``pip`` to install the required packages, please verify
   that the path to ``pip``'s executable file has been added correctly to your
   environment variable ``PATH``. The address may vary depending on whether you install
   it for one or all users (e.g., ``%USERPROFILE%\AppData\roaming\Python\Python37\scripts``
   or ``C:\Users\MyUserName\AppData\Local\Programs\Python\Python37\Scripts``).

The application ``okplm`` depends on the Python package ``numpy``. Make sure
it is installed before using ``okplm``.

If you do not have to compile the documentation, ``sphinx`` is not
necessary to use ``okplm``, since a precompiled pdf copy of the documentation is
included in the folder ``docs``.

If you need to compile the documentation from source (e.g., to modify it),
you will need the package ``sphinx``. To install ``sphinx`` just make:

.. code:: shell

    pip install sphinx

The package ``sphinx`` works by default with reStructuredText documents. However,
it can also recognise Markdown by installing the Markdown parser ``recommonmark``.

.. code:: shell

    pip install --upgrade recommonmark

To create multilingual documentation, you will need the package ``sphinx-intl``.
The installation process is as above:

.. code:: shell

    pip install sphinx-intl

To compile pdf documents (only in Linux), you will also need to have installed
latex and the Python package ``latexmk``. To install latex, type:

.. code:: shell

    sudo apt-get install texlive-full

And to install ``latexmk``, type:

.. code:: shell

    pip install latexmk.py


Cloning the repository
----------------------
You need to clone the ``okplm`` package with git. For this go to an
appropriate directory (e.g., ``pathtoprojectsfolder``) where to copy the
project's code in a subfolder and clone the ``okplm`` project:

.. code:: shell

    cd pathtoprojectsfolder
    git clone https://github.com/inrae/ALAMODE-okp.git

This command creates the ``okplm`` repertory in the folder ``pathtoprojectsfolder``.

To install the development branch of the project,
after cloning the ``okplm`` package, change to the ``dev`` branch:

.. code:: shell

    cd okplm
    git checkout dev


Installing ``okplm``
---------------------
To install ``okplm``, go to the repertory created during the cloning of the
package ``okplm`` (e.g., ``pathtorepertoryokplm``) and install
it using ``pip``:

.. code:: shell

    cd pathtorepertoryokplm
    pip install -U .

Compilation of the project documentation
----------------------------------------
The source files for the project user manual are stored in the folder
``pathtorepertoryokplm/sphinx-doc/source``. Sphinx also extracts data from the
project modules docstrings.

Documentation in English
^^^^^^^^^^^^^^^^^^^^^^^^
To compile the user manual in English as html files
go to the folder ``pathtorepertoryokplm/sphinx-doc`` and type:

.. code:: shell

    make html

The output html files are saved in the folder
``pathtorepertoryokplm/sphinx-doc/build/html``

You can also compile the user manual as a pdf file making:

.. code:: shell

    make latexpdf

The source documentation files are converted to latex and then to pdf. The
output latex and pdf files are saved in the folder
``pathtorepertoryokplm/sphinx-doc/build/latex``.

Documentation in French
^^^^^^^^^^^^^^^^^^^^^^^
To compile the user manual in French as html files
go to the folder ``pathtorepertoryokplm/sphinx-doc`` and type:

.. code:: shell

    sphinx-build -b html -aE -D language='fr' -c source/locale/fr source build_fr/html

The output html files are saved in the folder
``pathtorepertoryokplm/sphinx-doc/build_fr/html``.

To compile the pdf documentation, type the following commands:

.. code:: shell

    sphinx-build -b latex -aE -D language='fr' -c source/locale/fr source build_fr/latex
    cd build_fr/latex
    make

The source documentation files are converted to latex and then to pdf. The
output latex and pdf files are saved in the folder
``pathtorepertoryokplm/sphinx-doc/build_fr/latex``.
