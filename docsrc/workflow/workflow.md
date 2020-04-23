# Git workflow 

The git workflow used in this project is based on [this blog post](https://nvie.com/posts/a-successful-git-branching-model/).
Using this workflow allows for better collaboration between contributors and automation of repetitive tasks.

In addition to the workflow described in the blog post, Github Actions lints the code automatically on the release branches and builds documentation from each push to the master branch. For now, we don't use hotfix branches.

![Workflow](figure-git-workflow.svg)

_Git workflow for this project. Based on work by Vincent Driessen, Creative Commons BY-SA._