# Contributing

Contributions are welcome, and they are greatly appreciated! Every little bit helps, and credit will always be given.

## Types of Contributions
You can contribute in many ways:
### Report Bugs

Report bugs at https://github.com/amiraref/post-tracker/issues

If you are reporting a bug, please include:

- Your operating system name and version.
- Any details about your local setup that might be helpful in troubleshooting.
- Detailed steps to reproduce the bug.

### Fix Bugs

Look through the GitHub issues for bugs. Anything tagged with "bug" and "help wanted" is open to whoever wants to implement a fix for it.
Implement Features

Look through the GitHub issues for features. Anything tagged with "enhancement" and "help wanted" is open to whoever wants to implement it.

### Submit Feedback

The best way to send feedback is to file an issue at https://github.com/amiraref/post-tracker/issues.

### If you are proposing a new feature:

- Explain in detail how it would work.
- Keep the scope as narrow as possible, to make it easier to implement.
- Remember that this is a volunteer-driven project, and that contributions are welcome :)  


## Get Started!

Ready to contribute? Here's how to set up post-tracker for local development. Please note this documentation assumes you already have poetry and Git installed and ready to go.
1. Fork the post-tracker repo on GitHub.
2. Clone your fork locally:
    ```bash
    cd <directory_in_which_repo_should_be_created>
    git clone https://github.com/YOUR_NAME/post-tracker.git
    ```
3. Now we need to install the environment. Navigate into the directory
    ```bash
    cd post-tracker
    ```
4. Create a branch for local development:
    ```bash
    git checkout -b name-of-your-bugfix-or-feature
    ```
    Now you can make your changes locally.

5. Don't forget to add test cases for your added functionality to the tests directory.
6. Now, validate that all unit tests are passing:
    ```bash
    pytest
    ```
7. Commit your changes and push your branch to GitHub:
    ```bash
    git add .
    git commit -m "Your detailed description of your changes."
    git push origin name-of-your-bugfix-or-feature
    ```
8. Submit a pull request through the GitHub website.

## Pull Request Guidelines

Before you submit a pull request, check that it meets these guidelines:

- The pull request should include tests.
- If the pull request adds functionality, the docs should be updated. Put your new functionality into a function with a docstring.

