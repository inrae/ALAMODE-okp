Translation of the project's documentation
==========================================
The ``okplm`` package is originally written in English and
translated into French. This section describes the process to
translate the `User and Developer Guide` by using pot and po files
and the package ``sphinx-intl``. Using this method
only the modified sections of text need to be translated again when
modifications are made to the original documentation. It also facilitates
the translation of docstrings and module documentation. The
translation instructions are based on https://sphinx-doc.org/en/1.8/intl.html.

Preliminary steps
^^^^^^^^^^^^^^^^^
Before starting the translation it is advisable to check the source files
thoroughly to eliminate any language or format issues.

A glossary of technical terms has been created to improve the consistency
of the translation. It is located in the folder ``sphinx-doc/glossaries``.


Creation of POT and PO files
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
The translation of the documentation files is based on the extraction of the
translatable text into pot (portable object template) files and the creation
of translated text in po (portable object) files. For this, the package
``sphinx-intl`` is used.

To extract the document's translatable messages into pot files, change to the
``sphinx-doc`` directory in the terminal and do:

.. code:: shell

    make gettext

The resulting pot files are saved in the folder ``build/gettext``. They
contain the translatable text broken down into segments.

Then you need to generate the po files for each
target language. For example, for French you need to do

.. code:: shell

    sphinx-intl update -p build/gettetxt/ -l fr

The resulting po files are stored in the folder
``source/locale/fr/LC_MESSAGES``.

The po files contain pairs of segments of text in the source (msgid) and target
language (msgstr).

Before starting the translation, the value of msgstr is empty:

::

    #: ../../source/style.rst:24
    msgid "The user manual has been generated using ``sphinx`` from files using `reStructuredText <http://www.sphinx-doc.org/en/master/usage/restructuredtext/index.html>`_ markup language."
    msgstr ""

Translation
^^^^^^^^^^^
Thus to translate the text you need to edit the po files
and type de translated text beside msgstr:

::

    #: ../../source/style.rst:24
    msgid "The user manual has been generated using ``sphinx`` from files using `reStructuredText <http://www.sphinx-doc.org/en/master/usage/restructuredtext/index.html>`_ markup language."
    msgstr "Le guide utilisateur a été créé avec ``sphinx`` depuis fichiers utilisant le language markup `reStructuredText <http://www.sphinx-doc.org/en/master/usage/restructuredtext/index.html>`_."

.. Attention:: Be careful to maintain the reST formatting in the
   translated version.

You can do the translation by hand by modifying the po files. However, it is more
efficient to use a PO editor (e.g., GNOME Translation Editor or PO edit) or
computer assisted translation (CAT) software such as OmegaT.

Compilation of the translated documentation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
The documentation in French is saved in the folder ``build_fr``.
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

Update of the translated documentation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
If the project's documentation is updated, it is necessary to create new pot
files following the procedure described above. To apply the changes to the
po files, do

.. code:: shell

    sphinx-intl update -p build/gettext -l fr

Then, you only need to translate the modified segments.
