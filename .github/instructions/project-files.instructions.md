---
applyTo: '.gitignore,README.md'
description: This file describes the general guidelines for project files.
---

# .GITIGNORE

Add the following patterns to the .gitignore file to ensure that certain files and directories are not tracked by Git:

# Ignore Python bytecode files
__pycache__/
*.pyc
# Ignore SQLite database files
data/*.db
# Ignore environment variable files
.env
# Ignore OS files
.DS_Store
Thumbs.db
# Ignore credentials file
creds.yaml
# Ignore generated images
images/

# README.MD

The README file should have the following sections:

**Description**: A brief overview of the project, its purpose, and its main features.

**Update Log**: A section that lists recent changes and updates to the project, including any new features, bug fixes, or improvements. This section is additive only. It shoud not remove any previous entries. Each entry should include a brief description of the change and the date it was made. This will help users keep track of the project's development and understand how it has evolved over time. Use this format: `**YYYY-MM-DD**: Description of the change.`

DO NOT include any other sections in the README file.