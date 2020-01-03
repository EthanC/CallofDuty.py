# How to Contribute

Contributions to this project are gladly accepted, there are a just a few guidelines that need to be followed.

## Reporting Issues

Bugs and feature requests should be directed to the [GitHub Issue Tracker](https://github.com/EthanC/CallofDuty.py/issues).

If reporting a bug, please try and provide as much context as possible such as your operating system, Python version, and anything else that might be relevant to the bug. Security related bugs should also be reported in the Issue Tracker, or if they are more sensitive, Direct Messaged to [@Mxtive on Twitter](https://twitter.com/Mxtive) or `Lacking#0001` on [Discord](https://discord.gg/CallofDuty).

For feature requests, please explain what you're trying to do and how the requested feature would help you do that. Assuming the feature is currently available in the Call of Duty Companion App or My Call of Duty Website, please explain where it can be found.

## Submitting a Contribution

1. It's generally best to start by opening a new Issue describing the bug or feature you're intending to fix. Even if you think it's relatively minor, it's helpful to know what people are working on. Mention in the initial Issue that you are planning to work on that bug or feature so that it can be assigned to you.
2. Follow the normal process of [Forking](https://help.github.com/articles/fork-a-repo) the repository, then setup a new Branch to work in. It's important that each group of changes be done in separate Branches in order to ensure that a Pull Request only includes the commits related to that bug or feature.
3. [Pylint](https://github.com/PyCQA/pylint) and [Black](https://github.com/psf/black) are used in this project and make it very simple to ensure properly formatted code, so always run the two on your code before committing it.
4. Any significant changes should almost always be accompanied by tests. The project already has good test coverage, so look at some of the existing tests if you're unsure how to go about it.
5. Do your best to have [well-formed Commit messages](http://tbaggery.com/2008/04/19/a-note-about-git-commit-messages.html) for each change. This provides consistency throughout the project, and ensures that Commit messages are able to be formatted properly by various git tools.
6. Finally, push the Commits to your Fork and submit a [Pull Request](https://help.github.com/articles/creating-a-pull-request). Please do not use Force-Push on Pull Requests in this repository, as it makes it more difficult for reviewers to see what has changed since the last code review.
