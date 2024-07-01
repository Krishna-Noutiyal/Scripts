# Git Automation Script</span> :computer: :octocat:
## Overview

This Python script automates the synchronization of changes between a local Git repository and a remote repository. It is designed to streamline the process of committing local changes and pushing them to a remote repository, while also handling common Git operations such as fetching changes, merging, and resolving conflicts.

## Features :rocket:

- **Automated Sync**: Checks and syncs changes between local and remote repositories.
- **Conflict Handling**: Detects and alerts about conflicts, allowing manual resolution.
- **Untracked Files**: Stages untracked files for commit automatically.
- **Modified Files**: Stages and commits modified files with a generated commit message.
- **Error Handling**: Catches GitCommandError exceptions to manage merge conflicts and other errors.

## Usage :wrench:

### Requirements :clipboard:

- Python 3.x
- `gitpython` library (`pip install gitpython`)

### Setup :gear:

1. Clone or download this repository.
2. Install Python 3.x if not already installed.
3. Install required dependencies using `pip install -r requirements.txt`.

### Running the Script :arrow_forward:

#### For Windows :desktop_computer:
---

```powershell
py gitsync.py "C:\path\to\your\local\repository"
```

Replace `"C:\path\to\your\local\repository"` with the actual path to your local Git repository on Windows.

---

#### For Linux :penguin:

```bash
python3 gitsync.py "/path/to/your/local/repository"
```
Replace `"/path/to/your/local/repository"` with the actual path to your local Git repository on Linux.

---

### Functionality :hammer_and_wrench:

1. **Sync Check**: Determines if the local repository is ahead of, behind, or in sync with the remote.
2. **Fetching Changes**: Fetches and merges changes from the remote repository if local is behind.
3. **Committing Changes**: Commits untracked and modified files automatically.
4. **Pushing Changes**: Pushes committed changes to the remote repository.
5. **Conflict Resolution**: Alerts about conflicts and prompts manual resolution if needed.

### Example :bulb:

#### For Windows :desktop_computer:

```cmd
python gitsync.py "C:\Users\YourUsername\Documents\YourRepository"
```

#### For Linux :penguin:

```bash
python3 gitsync.py "/home/username/Documents/YourRepository"
```

### Notes :memo:

- **Make sure the commit histories of both repositories match before running the scripts**
- Ensure you have the necessary permissions to push changes to the remote repository.
- It's recommended to have a clean working directory with all necessary changes staged before running the script.

## Troubleshooting :warning:

- If encountering merge conflicts, resolve them manually and rerun the script.
- Check console output for error messages and follow prompts for conflict resolution.

## License :scroll:

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

Feel free to customize further according to your specific repository paths and any additional instructions you want to include.
