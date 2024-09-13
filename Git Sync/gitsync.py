from git import Repo, Remote, GitCommandError, FetchInfo
import sys

# ANSI color codes
RESET = "\033[0m"
BOLD = "\033[1m"
BLUE = "\033[1;34m"
GREEN = "\033[1;32m"
YELLOW = "\033[1;33m"
RED = "\033[1;31m"


def Commit_Dates(repo: Repo, remote: Remote) -> list[int]:
    """`Return`: `Tuple(int)` a tuple of two integer elements representation of commit date.
    Where the first element is `Local_Commit_Date` and the second element is `Remote_Commit_Date`
    """

    remote.fetch()

    last_commit_local = repo.head.commit.committed_date
    last_commit_remote = remote.refs[0].commit.committed_date

    return [last_commit_local, last_commit_remote]


if __name__ == "__main__":

    HELP = f"""
{BLUE}\t\t********** GIT AUTOMATION SCRIPT **********{RESET}

{GREEN}\tDescription:{RESET}
\tThis script automates the synchronization of changes between your local Git repository and a remote repository. 
\tIt manages commits, pushes, and resolves conflicts to keep your codebase up-to-date.

{GREEN}\tUsage:{RESET}
\t\t{YELLOW}python gitsync.py <Local_Repository_Path>{RESET}

{GREEN}\tParameters:{RESET}
\t\t<Local_Repository_Path> : Path to your local Git repository.

{GREEN}\tFunctionality:{RESET}
\t- Checks if the local repository is ahead of the remote repository.
\t- Fetches and merges changes from the remote repository if local is behind.
\t- Automatically stages untracked files for commit.
\t- Manages modifications in tracked files, staging them for commit.
\t- Handles deletions of tracked files.
\t- Commits changes locally with an automatic message.
\t- Displays the synchronized status of the local Git repository.

{GREEN}\tOutput:{RESET}
\t- Provides status updates on repository synchronization.
\t- Alerts about untracked, modified, and deleted files staged for commit.
\t- Reports the outcome of commit and push operations.

{GREEN}\tNotes:{RESET}
\t- {BOLD}Make sure the commit histories of both repositories match before running the scripts{RESET}
\t- Ensure permissions allow pushing changes to the remote repository.
\t- Keep the working directory clean with staged changes before running the script.

{BLUE}\n\t\t********** END OF HELP MESSAGE **********{RESET}

"""

    args = sys.argv

    if len(args) < 2:
        print(HELP)
        exit()

    DIR = args[1]
    repo = Repo(DIR)
    remote = repo.remote("origin")

    diff = repo.index.diff(None)
    flags = {
        "d": 0,
        "u": len(repo.untracked_files),
        "m": 0,
    }  # d = deleted, u = untracked, m = modified

    # Checking for Untracked Files
    print(f"\n{BLUE}Checking for Untracked Files:{RESET}")

    for i in repo.untracked_files:
        print(f"\t{YELLOW}Untracked:{RESET} {i}")
    repo.index.add(repo.untracked_files)

    # Checking for file deletion or modification
    print(f"\n{BLUE}Checking for Deleted or Modified Files:{RESET}")
    for i in diff:
        if i.deleted_file:
            flags["d"] += 1
            repo.index.remove(i.a_path)
            print(f"\t{RED}Deleted: {RESET}" + i.a_path)
        else:
            flags["m"] += 1
            if i.change_type == "A":
                print(f"\t{GREEN}Added: {RESET}" + i.a_path)
            else:
                print(f"\t{GREEN}Modified: {RESET}" + i.a_path)
                repo.index.add(i.a_path)

    # Generating the commit message
    msg = "Automatic Commit : "
    msg += f"Added {flags['u']} Files " if flags["u"] != 0 else ""
    msg += f"Deleted {flags['d']} Files " if flags["d"] != 0 else ""
    msg += f"Modified {flags['m']} Files " if flags["m"] != 0 else ""

    # Committing Changes
    if flags["d"] > 0 or flags["u"] > 0 or flags["m"] > 0:
        print("\nCommitting changes locally...")

        print(f"\n{BLUE}Files to be committed:{RESET}")

        for item in repo.index.diff(remote.refs[0].commit):
            print(f"\t{item.a_path}")
        try:
            repo.index.commit(msg)
        except Exception as e:
            print(f"\n{RED}Unable to commit changes{RESET}")
            print(f"{RED}Error: {e}{RESET}")

    else:
        print("No changes found in local repository")

    # Fetching and merging changes from Remote Repository
    Date_of_Commits = Commit_Dates(repo, remote)
    L_commit, R_commit = Date_of_Commits[0], Date_of_Commits[1]

    # Syncing changes in Local and Remote Repository
    if L_commit == R_commit:
        print("Both Local and Remote Repositories are in SYNC")
        pass

    elif L_commit < R_commit:
        print("Checking for changes in Remote Repository...")

        print("Remote Repository is up to date")
        print("Local Repository might be Outdated")
        print("\nFetching Changes...")
        print("Fetched Changes successfully")

        # Merging Changes
        try:
            repo.git.merge(remote.refs[0])
        except GitCommandError as e:
            if "conflict" in e.stdout.lower():
                print(
                    f"{RED}Conflict detected. Please resolve conflicts manually.{RESET}"
                )
                sys.exit(1)  # Exit the script to allow manual conflict resolution

            elif e.status == 128:
                print(
                    f"{BOLD}Unrelated histories detected.{RESET} {RED}Please merge manually using `git merge --allow-unrelated-histories` if necessary.{RESET}"
                )
                sys.exit(1)

            else:
                print(f"{BOLD}An error occurred during the merge:\n {RESET}", e)
                print("Trying to pull changes from remote repo...")

                try:
                    remote.pull()
                except:
                    print(f"{BOLD}An error occurred during the pull:\n {RESET}", e)
                    sys.exit(1)

        print("Merged Changes successfully")

    # If Local Repository is ahead of Remote Repository, then Commit and Push
    else:
        print("Remote Repository is not up to date.")
        print("\nTrying to Push code to remote repo...")

        if repo.is_dirty(untracked_files=True):
            print(
                f"\n{RED}Unresolved conflicts detected. Please resolve conflicts manually.\n{RESET}"
            )
            sys.exit(1)

        elif len(repo.index.diff(remote.refs[0].commit)) > 0:
            # Check for merge conflicts
            print("Merge conflicts detected.")
            print("Trying to pull changes from remote repo...")
            try:
                remote.pull()
                print("Pull successful.")
                print("Trying to push changes to remote repo...")

                remote.push()

                print("Pushed code to remote repo")
                print("Continuing with Local Repository...")

                print(f"\n\t{GREEN}*** WORK SYNCED SUCCESSFULLY ***\n{RESET}")

                remote.push()

            except Exception as e:
                print(f"{BOLD}An error occurred during the push:\n {RESET}", e)
                print(f"{BOLD}\nResolve Conflicts Manually !!\n {RESET}", e)

        else:
            print("No merge conflicts detected.")
            print("Trying to push changes to remote repo...")

            remote.push()

            print("Pushed code to remote repo")
            print("Continuing with Local Repository...")

            print(f"\n\t{GREEN}*** WORK SYNCED SUCCESSFULLY ***\n{RESET}")
