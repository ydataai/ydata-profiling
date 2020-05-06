=======================
Contribution Guidelines
=======================

Contributing a new feature
--------------------------

* Open a new Github pull request with the patch.

* Ensure the PR description clearly describes the problem and solution.
  Include the relevant issue number if applicable.

Developer tools
---------------

There are tools available to ease the development cycle. These can be called from the root directory with the ``make`` command.

The following commands are supported:

.. code-block::

        make lint
        make install
        make examples
        make docs
        make test
        make typing


Git workflow
------------

The git workflow used in this project is based on `this blog post <https://nvie.com/posts/a-successful-git-branching-model/>`_.
Using this workflow allows for better collaboration between contributors and automation of repetitive tasks.

In addition to the workflow described in the blog post, Github Actions lints the code automatically on the release branches and builds documentation from each push to the master branch. For now, we don't use hotfix branches.

.. figure::  ../_static/figure-git-workflow.svg
  :alt: Workflow

  Git workflow for this project. Based on work by Vincent Driessen, Creative Commons BY-SA.


More information
----------------

Read more on getting involved in the `Contribution Guide <https://github.com/pandas-profiling/pandas-profiling/blob/master/CONTRIBUTING.md>`_ on Github.