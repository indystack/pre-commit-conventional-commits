# Conventional Commits pre-commit hook

A [`pre-commit`](https://pre-commit.com) hook to check commit messages for [Conventional Commits](https://conventionalcommits.org) formatting.

## Installation
Add the following entry into your `.pre-commit-config.yaml` file:
```
repos:
  # - repo: ...

  - repo: https://github.com/indystack/pre-commit-conventional-commits
    rev: v1.0.0
    hooks:
      - id: pre-commit-conventional-commits
        stages: [commit-msg]
        args: [] # optional: list of Conventional Commits types to allow e.g. [feat, fix, ci, chore, test]
```

Install the script:
```
pre-commit install --hook-type commit-msg
```

## Usage
Write a commit message using incorrect format:
```bash
$ git commit -m "wrong format"

Conventional Commit ..............................................Failed
- hook id: pre-commit-conventional-commits
- duration: 0.05s
- exit code: 1

Bad commit message: wrong format
Your commit message does not follow Conventional Commits formatting.

Conventional Commits start with one of the below types, followed by a colon,
followed by the commit message:

feat fix

Good examples:
feat: Added new feature
feat(billing): Improved invoices
fix: Fixed speed of execution
feat!: This is breaking change
```

Write a commit message using correct format:
```bash
$ git commit -m "feat: Updated something"

Conventional Commit ..............................................Passed
```
