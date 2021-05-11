=======================
Contribution Guidelines
=======================

Contributing a new feature
--------------------------

* Open a new Github pull request with the patch.

* Ensure the PR description clearly describes the problem and solution.
  Include the relevant issue number if applicable.
  
Slack community
---------------
A low threshold place to ask questions or start contributing is by reaching out on the pandas-profiling Slack. `Join the Slack community <https://join.slack.com/t/pandas-profiling/shared_invite/zt-oe5ol4yc-YtbOxNBGUCb~v73TamRLuA>`_.

Developer tools
---------------

There are tools available to ease the development cycle. These can be called from the root directory with the ``make`` command.

The following commands are supported:

.. code-block:: console

    make lint
    make install
    make examples
    make docs
    make test
    make clean


Git workflow
------------

The git workflow used in this project is based on `this blog post <https://nvie.com/posts/a-successful-git-branching-model/>`_.
Using this workflow allows for better collaboration between contributors and automation of repetitive tasks.

In addition to the workflow described in the blog post, Github Actions lints the code automatically on the release branches and builds documentation from each push to the master branch. For now, we don't use hotfix branches.

Branch naming:
- develop: development branch
- master: master branch
- feature/[FEATURE NAME]: feature branches
- release/v[VERSION]: releases
- gh-pages: documentation and examples are hosted here

.. figure::  ../_static/figure-git-workflow.svg
  :alt: Workflow
  :width: 80%

  Git workflow for this project. Based on work by Vincent Driessen, Creative Commons BY-SA.


Contributor License Agreement (CLA)
-----------------------------------
This package does not have a Contributor License Agreement (CLA), as the GitHub Terms of Service provides a sensible `explicit default <https://help.github.com/en/github/site-policy/github-terms-of-service#6-contributions-under-repository-license>`_:

        *Whenever you make a contribution to a repository containing notice of a license, you license your contribution under the same terms, and you agree that you have the right to license your contribution under those terms.*

Read Github's `open source legal guide <https://opensource.guide/legal/#does-my-project-need-an-additional-contributor-agreement>`_ for further details.

More information
----------------

Read more on getting involved in the `Contribution Guide <https://github.com/pandas-profiling/pandas-profiling/blob/master/CONTRIBUTING.md>`_ on Github.
