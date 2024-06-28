from git import Repo, Remote    
import sys

# Function to print colored messages
def print_colored(text, color_code="0"):
    print(f"\033[{color_code}m{text}\033[0m")

# Centralized function for different log levels
def log(message, level="info"):
    """Prints the message in the specified level and color"""
    levels = {
        "info": "1;32",  # Green
        "warning": "1;33",  # Yellow
        "error": "1;31",  # Red
        "status": "1;36",  # Cyan
        "help": "1;34"  # Blue
    }
    color_code = levels.get(level, "0")
    print_colored(message, color_code)


def Commit_Changes(remote: Remote, repo: Repo = None, message: str = None, only_remote: bool = False) -> None:
    """### Inputs:
        `repo`: Local Git Repository
        `remote`: Remote Git Repository
        `message`: Commit Message
        `only_remote`: `True` if you want to push to remote repo only, else `False`

        By Default commit is done locally. 
        If `only_remote` is set to `True`, 
        Changes are pushed to remote repo only.
        #### If  `only_remote` is True :
            \t`repo = None` and `message = None` 

    ### Returns: 
    `True` if commit is successful, else `False`

    """
    
    if not only_remote:
        assert repo is not None
        assert message is not None
        repo.index.commit(message)
    else:
        remote.push()
    return True

def Is_ahead(repo: Repo, remote: Remote) -> bool:
    """Returns `True` if local repo is ahead of remote repo, else `False`."""
    last_commit_local = repo.head.commit.committed_date
    last_commit_remote = remote.refs[0].commit.committed_date 
    return True if last_commit_local > last_commit_remote else False

def Check_Untraced_Files(repo: Repo) -> list[str] | None:
    """Checks if there are any untracked files in the local repository."""
    UT_FILES = repo.untracked_files
    if len(repo.untracked_files) > 0:
        return UT_FILES
    return None

if __name__ == "__main__":
    args = sys.argv
    HELP = """
\033[1;34m\t\t********** GIT AUTOMATION SCRIPT **********\033[0m

\033[1;32m\tDescription:\033[0m
\tThis script automates the process of committing changes to your local Git repository and 
\tpushing them to a remote repository. It handles checking for untracked files, 
\tcommitting changes locally, and ensuring your remote repository is up-to-date.

\033[1;32m\tUsage:\033[0m
\t\t\033[1;33mpython gitsync.py <Repository_Path>\033[0m

\033[1;32m\tParameters:\033[0m
\t\t<Repository_Path> : The path to your local Git repository.

\033[1;32m\tExample:\033[0m
\t\t\033[1;33mpython gitsync.py "S:/C_Plus_Plus"\033[0m

\033[1;32m\tFunctionality:\033[0m
\t1. Checks if the local repository is ahead of the remote repository.
\t   - If not, it fetches and merges changes from the remote repository.
\t   - If yes, it pushes the local changes to the remote repository.
\t2. Checks for untracked files in the local repository and stages them for commit.
\t3. Checks for any modifications in tracked files.
\t4. Commits changes locally with a user-provided message and pushes them to the remote repository.
\t5. Displays the status of the local Git repository after synchronization.

\033[1;32m\tOutput:\033[0m
\t- Messages indicating the status of the repository, any untracked files found, 
\t  and the result of commit and push operations.

\033[1;32m\tNote:\033[0m
\t- Ensure you have the necessary permissions to push changes to the remote repository.
\t- Make sure your working directory is clean and all necessary changes are staged before running the script.

\033[1;34m\t********** END OF HELP MESSAGE **********\033[0m
"""
    if len(args) < 2:
        log(HELP, "help")
        exit()

    DIR = args[1]
    repo = Repo(DIR)
    remote = repo.remote("origin")
    log(repo.git.status(), "status")

    # Fetching and merging changes from Remote Repository
    if not Is_ahead(repo, remote):
        log("Checking for changes in Remote Repository...", "warning")
        log("Remote Repository is up to date", "info")
        log("Local Repository might be Outdated", "error")
        log("Fetching Changes...", "warning")

        remote.fetch()

        log("Fetched Changes successfully", "info")

        Check_Difference = repo.index.diff(remote.refs[0].commit)

        # If Changes are found then Merge Changes

        if len(Check_Difference) > 0:  

            log("Merging changes...", "warning")

            repo.git.merge(remote.refs[0])

            log("Merged Changes successfully", "info")
            
    
    # If Local Repository is ahead of Remote Repository then Commit and Push
    else:
        log("Remote Repository is not up to date.", "error")
        log("Pushing code to remote repo...", "warning")

        Commit_Changes(remote, only_remote=True)

        log("Pushed code to remote repo", "info")
        log("Continuing with Local Repository...", "warning")
    


    # Checking and adding untraced files to staging area ( including commit )
    log("Checking for untracked files...", "warning")
    UT_FILES = Check_Untraced_Files(repo)

    if UT_FILES is not None:
        log("Untracked files found:", "error")

        print("\n".join(UT_FILES))

        log("Pushing untracked files to staging area...", "warning")

        repo.index.add(UT_FILES)
        Commit_Changes(remote,repo)


    else:
        log("No untracked files found.", "info")
    
    log("Checking for file modifications...", "warning")


    # assert not repo.is_dirty()

    # Check for changes in Local Repository
    if not Is_ahead(repo, remote):
        log("No changes found.", "info")
    else:
        log("Changes found.", "error")
        log("Files to be committed:\n", "error")

        for item in repo.index.diff(remote.refs[0].commit): 
            log(f"\t{item.a_path} -> {item.b_path}", "info")

        log("\nCommitting changes locally and pushing to remote...", "warning")

        msg = input("\n\tEnter commit message: ")

        # msg = "Automated Commit"

        log("\nCommitting changes...", "warning")

        Commit_Changes(remote, repo, msg)
        
        log(repo.git.status(), "status")
    
    log("\n\t*** WORK SYNCED SUCCESSFULLY ***\n", "info")

