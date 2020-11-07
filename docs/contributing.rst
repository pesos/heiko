Contributing
============

Development Dependencies
------------------------

#. Python 3 (versions 3.7 to 3.8 are currently supported)
#. To test out heiko you need a system with SSH set up on it. You can do it locally (on localhost) but it is preferred to have a different
   device (such as mobile phone or Raspberry Pi) to test it on. You can use any non-terminating program such as ``cat`` or ``tail -f`` to
   test out heiko.
#. If you're making changes to the documentation, install the documentation dependencies: ``pip install -r docs/requirements.txt``.

    * Refer `this <https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html>`_ for a brief introduction to ReST.

Development Process - Short Version
-----------------------------------

#. Select an issue to work on, and inform the maintainers.
#. Fork the repository.
#. ``git clone`` the forked version of the project.
#. Work on the master branch for smaller patches and a separate branch for new features.
#. Make changes, ``git add`` and then commit. Make sure to link the issue number in the commit message.
#. (Optional) Run the following: ``cd docs``, ``make html`` and then open ``_build/html/index.html`` in a browser to confirm
   that the documentation rendered correctly.
#. If all tests are passing, pull changes from the original remote with a rebase, and push the changes to your remote repository.
#. Use the GitHub website to create a Pull Request and wait for the maintainers to review it.

Development Process - Long Version
----------------------------------

#. Select an issue to work on, and inform the maintainers.

   * Look for issues, find something that you want to work on.
   * Leave a comment on the issue saying that you want to work on it. The maintainers will give you the go-ahead.

#. Fork the repository.

   * The fork button will be available on the top right in the GitHub website.

#. ``git clone`` the forked version of the project.

   * ``git clone https://github.com/<your-github-username>/heiko.git``
   * Add a remote to the original repository and name it ``upstream``.
   * ``git remote add upstream https://github.com/psiayn/heiko.git``

#. Work on the master branch for smaller patches and a separate branch for new features.

   * To create a new feature branch and use it, run: ``git checkout -b feature-<feature-name>``.
   * If a feature branch already exists, switch to it before committing: ``git checkout feature-<feature-name>``

#. Make changes, ``git add`` and then commit. Make sure to link the issue number in the commit message.

   .. caution:: When testing changes, create and activate a virtual environment and install
      the package in editable mode using ``pip install -e .`` to ensure that the pip version is not used.

   * ``git add <names of all modified files>``
   * ``git commit``
   * Make your commit descriptive. The above command will open your text editor.
   * Write the commit message on the first line and a short description about your change. Save and quit the editor to commit your change.

#. Ensure that the CLI works by using it. Try commands such as ``heiko --help``, ``heiko init``, ``heiko start``, etc.

#. (Optional) If you're updating the documentation, run the following:

   .. caution:: Update ``docs/quickstart.rst`` and ``README.md`` simultaneously.

   * Change to the docs directory: ``cd docs``
   * Build the documentation: ``make html``
   * Open ``_build/html/index.html`` in a browser to confirm that the documentation rendered correctly.

#. If all tests are passing, pull changes from the original remote with a rebase, and push the changes to your remote repository.

   .. caution:: If you are working on a feature branch, use that branch name instead of master.

   * ``git pull --rebase upstream master``
   * In the extremely small chance that you run into a conflict, just open the files having the conflict and remove the markers and edit the file to the one you want to push. After editing, run ``git rebase --continue`` and repeat till no conflict remains.
   * Verify that your program passes all the tests, and your change actually works in general.

   .. caution:: If you are working on a feature branch, use that branch name instead of master.

   * Push your changes to your fork: ``git push origin master``

#. Use the GitHub website to create a Pull Request and wait for the maintainers to review it.

   * Visit your forked repository and click on "Pull Request". The Pull Request must always be made to the ``psiayn/master`` branch.
     Add the relevant description, ensure that you link the original issue.
   * The maintainers will review your code and see if it is okay to merge. It is quite normal for them to suggest you to make some changes in this review.
   * If you are asked to make changes, all you need to do is::

      # make your change
      git add <files that you changed>
      git commit
      git push origin master      # if you are working on a feature branch, use that branch name instead of master

   * The changes are immediately reflected in the pull request. Once the maintainers are satisfied, they will merge your contribution :)

Release Overview
----------------

(for the more regular contributors)

- ``master`` branch for development. Small patches/enhancements go here.
- ``release`` branch for tagged releases. This is the branch that will be shipped to users.
- Separate ``feature-x`` branches for adding new "big" features. These branches are merged with master, on completion.
- Once we are satisfied with a certain set of features and stability, we pull the changes from master to release. A new release tag is made.

  * Ensure that version numbers are changed where necessary (``setup.py``, docs, etc.) - PyPI does
    not accept new files for the same version number, once a version is published it cannot be changed.

- If bugs were found on the stable release, we create a hotfix branch and fix the bug. The master branch must also pull the changes from hotfix. A new release tag is created (incrementing with a smaller number).

  * We follow `semantic versioning <https://semver.org/>`_ .

Code of Conduct
---------------

This project follows the `PES Open Source Code of Conduct <https://pesos.github.io/coc>`_ .
