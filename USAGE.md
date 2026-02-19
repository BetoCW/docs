# Repository Documentation Automation

This project includes a script to automate the process of adding new repositories to the documentation.

## Prerequisites

- Python 3.x installed.

## Usage

To add a new repository to the documentation, run the following command from the root of the project:

```bash
python3 scripts/add_repo.py <repository-name> [--url <repository-url>]
```

### Arguments

- `repository-name`: **Required**. The name of the repository you want to document. This will be used as the directory name and the title in the navigation.
- `--url`: **Optional**. The URL of the repository (e.g., GitHub URL). If provided, it will be added as a link in the generated `index.mdx` file.

### Example

```bash
python3 scripts/add_repo.py my-awesome-project --url https://github.com/my-org/my-awesome-project
```

This will:
1. Create a directory `repositories/my-awesome-project`.
2. Generate a starter `index.mdx` file in that directory.
3. Add "my-awesome-project" to the "Repositories" tab in `docs.json`.
