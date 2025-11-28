# Git Automation Script :computer: :octocat:

## Overview

This repository contains two Python scripts: `gitsync.py` and `multisync.py`.

- **`gitsync.py`** automates the synchronization of a single Git repository, handling commits, pushes, and fetches while managing conflicts.
- **`multisync.py`** extends the functionality of `gitsync.py` by synchronizing multiple repositories in parallel, using threading to manage multiple repositories at once.

Both `gitsync.py` and `multisync.py` files are designed in such a way that it is really easy to automate the syncing of repositories using these scripts in Windows and Linux. **You can very easily Schedule the running of these scripts in Windows 🖥️ or Linux 🐧.**

## Features :rocket:

### `gitsync.py`:

![gitsync](./assets/gitsync.png)

- **Automated Sync**: Synchronizes local and remote repositories.
- **Conflict Handling**: Alerts you about conflicts and prompts for manual resolution.
- **Untracked and Modified Files**: Automatically stages untracked and modified files.
- **Commit Messages**: Generates automatic commit messages based on changes.
- **Error Handling**: Captures and manages Git-related errors.

### `multisync.py`:

![gitsync](./assets/multisync.png)

- **Multiple Repository Sync**: Syncs multiple repositories listed in a text file.
- **Parallel Execution**: Uses threading to synchronize up to 4 repositories simultaneously.
- **Flexible Repository Management**: Automates the sync process for multiple Git repositories scattered across your system.

## <span style="color:red; font-weight:bold;"> Important Git Repo Initialization :warning:</span>

Before running the `gitsync.py` or `multisync.py` scripts, please ensure the following:

### 1.  **Upstream is Set** : 
Make sure that an upstream branch is configured for all the local Git repositories. This can be done using:

   For setting the upstream to `main`:
   
      git branch --set-upstream-to=origin/main
      
      
   or for `master`:
   
    git branch --set-upstream-to=origin/master
     

### 2.  **No Commit History Errors** : 
Ensure that there are no commit history mismatches between the local and remote branches. If there are any issues, such as:

 - Merge conflicts
 - Diverging commit histories

 Resolve these issues **before** running the scripts. You can do this by pulling the latest changes from the remote repository and resolving any conflicts manually:

 ```bash
 git pull origin main
 ```
 
 > **If needed, use Git merge tools to handle conflicts.**

### 3.  **Branch Restriction** : 
Currently, the `gitsync.py` script only works on the `main` or `master` branch by default. If your repository uses a different branch (e.g., `develop`), the script will not function correctly without modifications. Please ensure your primary branch is either `main` or `master`, or adjust the script as needed.

---

## Usage :wrench:

### Requirements :clipboard:

- Python 3.x
- `gitpython` library (`pip install gitpython`)

### Setup :gear:

1. Clone or download this repository.
2. Install Python 3.x if not already installed.
3. Install required dependencies using:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Scripts :arrow_forward:

---

### **Using `gitsync.py`**:

This script syncs changes between a single local Git repository and its corresponding remote repository.

#### For Windows :desktop_computer:

```powershell
py gitsync.py "C:\path\to\your\local\repository"
```

Replace `"C:\path\to\your\local\repository"` with the actual path to your local Git repository on Windows.

#### For Linux :penguin:

```bash
python3 gitsync.py "/path/to/your/local/repository"
```

Replace `"/path/to/your/local/repository"` with the actual path to your local Git repository on Linux.

---

### **Using `multisync.py`**:

This script automates synchronization for multiple repositories listed in a text file. It runs `gitsync.py` for each repository in parallel, handling up to 4 repositories simultaneously.

#### Prepare the Repository List:

1. Create a text file (`repos.txt`) that contains the paths to all the repositories you want to sync, with each path on a new line. Example:

   ```txt
   /path/to/repo1
   /path/to/repo2
   /path/to/repo3

   ```
> Your path can contain double quotes and single quotes no need to remove them. `multisync.py` automatically filters the quotes or any trailing spaces.

#### Running the Script:

#### For Windows :desktop_computer:

```powershell
py multisync.py "C:\path\to\gitsync.py" "C:\path\to\repos.txt"
```

#### For Linux :penguin:

```bash
python3 multisync.py "/path/to/gitsync.py" "/path/to/repos.txt"
```

Replace:

- `"/path/to/gitsync.py"` with the actual path to the `gitsync.py` script.
- `"/path/to/repos.txt"` with the path to your text file containing the list of repository paths.

---

## Functionality :hammer_and_wrench:

### `gitsync.py`:

1. **Sync Check**: Checks whether the local repository is ahead, behind, or in sync with the remote.
2. **Fetching Changes**: Automatically fetches and merges changes from the remote if the local repository is behind.
3. **Committing Changes**: Automatically commits untracked and modified files.
4. **Pushing Changes**: Pushes committed changes to the remote repository.
5. **Conflict Resolution**: Prompts for manual resolution if conflicts are detected.

### `multisync.py`:

1. **Multiple Repositories**: Reads the list of repositories from a text file and synchronizes each one.
2. **Parallel Processing**: Uses up to 4 threads to handle multiple repositories simultaneously.
3. **Integration with `gitsync.py`**: For each repository, the script invokes `gitsync.py` to manage the synchronization.

---

## Example :bulb:

### Running `gitsync.py` for a single repository:

#### For Windows :desktop_computer:

```powershell
py gitsync.py "C:\Users\YourUsername\Documents\YourRepository"
```

#### For Linux :penguin:

```bash
python3 gitsync.py "/home/username/Documents/YourRepository"
```

### Running `multisync.py` for multiple repositories:

#### For Windows :desktop_computer:

```powershell
py multisync.py "C:\path\to\gitsync.py" "C:\path\to\repos.txt"
```

#### For Linux :penguin:

```bash
python3 multisync.py "/home/username/gitsync.py" "/home/username/repos.txt"
```

---

## Notes :memo:

### For `gitsync.py`:

- **Ensure Commit Histories Match**: Make sure the commit histories of both the local and remote repositories match before running the script.
- **Permissions**: Ensure you have permission to push changes to the remote repository.
- **Clean Working Directory**: It's recommended to have a clean working directory with all changes staged before running the script.

### For `multisync.py`:

- Ensure that `gitsync.py` is executable from the provided path.
- The text file listing repositories should contain valid paths to Git repositories.

---

## Troubleshooting :warning:

- If encountering merge conflicts, resolve them manually and rerun the script.
- For `multisync.py`, ensure the text file has valid and accessible repository paths.
- Review the console output for error messages and follow prompts for conflict resolution.

---

## To Do :pencil:

1. **Customize Branch Selection**:
   - **Enhance `gitsync.py`**: Implement functionality to allow users to specify which branch to sync with the remote repository, rather than defaulting to `main` or `master`.
   - **Update `multisync.py`**: Ensure that `multisync.py` can pass branch selection options to `gitsync.py` for consistent behaviour across multiple repositories.

2. **Customize Number of Threads in `multisync.py`**:
   - Add an option to `multisync.py` to allow users to specify the number of threads to use for parallel repository synchronization. This will provide flexibility depending on the system’s capabilities and user needs.

3. **Improve Automatic Commit Messages**:
   - Enhance the commit message generation in `gitsync.py` to provide more detailed and informative messages about the changes being committed. This will help in better tracking of changes.

4. **Support for Custom Commit Messages**:
   - Implement a feature in `gitsync.py` to allow users to provide a custom commit message if needed, overriding the automatic message. This will be useful for scenarios where specific commit messages are required.

---

## License :scroll:

This project is licensed under the GNU General Public License - see the [LICENSE](../LICENSE) file for details.

---

