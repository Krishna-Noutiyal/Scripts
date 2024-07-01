from git import Repo, Remote, GitCommandError, FetchInfo
import sys



def Commit_Dates(repo: Repo, remote: Remote) -> list[int]:
    """`Return`: `Tuple(int)` a tuple of two integer elements reperentation of commit date.
    Where the first element is `Local_Commit_Date` and the second element is `Remote_Commit_Date`
    """
    
    remote.fetch()

    last_commit_local = repo.head.commit.committed_date
    last_commit_remote = remote.refs[0].commit.committed_date 

    return [last_commit_local,last_commit_remote]


if __name__ == "__main__":


    HELP = """
\033[1;34m\t\t********** GIT AUTOMATION SCRIPT **********\033[0m

\033[1;32m\tDescription:\033[0m
\tThis script automates the synchronization of changes between your local Git repository and a remote repository. It manages commits, pushes, and resolves conflicts to keep your codebase up-to-date.

\033[1;32m\tUsage:\033[0m
\t\t\033[1;33mpython gitsync.py <Local_Repository_Path>\033[0m

\033[1;32m\tParameters:\033[0m
\t\t<Local_Repository_Path> : Path to your local Git repository.

\033[1;32m\tFunctionality:\033[0m
\t- Checks if the local repository is ahead of the remote repository.
\t- Fetches and merges changes from the remote repository if local is behind.
\t- Automatically stages untracked files for commit.
\t- Manages modifications in tracked files, staging them for commit.
\t- Handles deletions of tracked files.
\t- Commits changes locally with an automatic message.
\t- Displays the synchronized status of the local Git repository.

\033[1;32m\tOutput:\033[0m
\t- Provides status updates on repository synchronization.
\t- Alerts about untracked, modified, and deleted files staged for commit.
\t- Reports the outcome of commit and push operations.

\033[1;32m\tNotes:\033[0m
\t- \033[1mMake sure the commit histories of both repositories match before running the scripts\033[0m
\t- Ensure permissions allow pushing changes to the remote repository.
\t- Keep the working directory clean with staged changes before running the script.

\033[1;34m\n\t\t********** END OF HELP MESSAGE **********\033[0m

"""

    args = sys.argv


    if len(args) < 2:
        print(HELP)
        exit()

    
    DIR = args[1]

    repo = Repo(DIR)
    remote = repo.remote("origin")

    

    diff = repo.index.diff(None)
    flags = {"d":0,"u":len(repo.untracked_files),"m":0} # d = deleted, u = untracked, m = modified

    # Checking for Untracked Files
    print("\n\033[1;34mChecking for Untracked Files :\033[0m")

    for i in repo.untracked_files:
        print(f"\t\033[1;33mUntracked:\033[0m {i}")
    repo.index.add(repo.untracked_files)


    # Checking for file deletion or modification
    print("\n\033[1;34mChecking for Deleted or Modified Files :\033[0m")
    for i in diff:
        if i.deleted_file:
            flags["d"] += 1
            repo.index.remove(i.a_path)
            print("\t\033[1;31mDeleted: \033[0m" + i.a_path)
        else:
            flags["m"] += 1
            if i.change_type == "A":
                print("\t\033[1;32mAdded: \033[0m" + i.a_path)
            else:
                print("\t\033[1;32mModified: \033[0m" + i.a_path)
                repo.index.add(i.a_path)
        

    # Generating the commit message
    msg = "Automatic Commit : "
    msg += f"Added {flags['u']} Files " if flags["u"] != 0 else ""
    msg += f"Deleted {flags['d']} Files " if flags["d"] != 0 else ""
    msg += f"Modified {flags['m']} Files " if flags["m"] != 0 else ""

    # Committing Changes
    if flags["d"] > 0 or flags["u"] > 0 or flags["m"] > 0:
        print("\nCommitting changes locally...")
        
        print("\n\033[1;34mFiles to be committed:\033[0m")

        for item in repo.index.diff(remote.refs[0].commit): 
            print(f"\t{item.a_path}")
        try:
            repo.index.commit(msg)
        except Exception as e:
            print("\n\033[1;31mUnable to commit changes\033[0m")
            print(f"\033[1;31mError: {e}\033[0m")

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
        
        Check_Difference = repo.index.diff(remote.refs[0].commit)

        # Merging Changes
        try:
            repo.git.merge(remote.refs[0])
        except GitCommandError as e:
            if 'conflict' in e.stdout.lower():
                print("Conflict detected. Please resolve conflicts manually.")
                sys.exit(1)  # Exit the script to allow manual conflict resolution


            elif e.status == 128:
                print("\033[1mUnrelated histories detected.\033[0m \033[1;31mPlease merge manually using `git merge --allow-unrelated-histories` if necessary.\033[0m")
                sys.exit(1)

            else:
                print("\033[1mAn error occurred during the merge:\n \033[0m", e)
                print("Trying to pull changes from remote repo...")

                try:
                    remote.pull()
                except:
                    print("\033[1mAn error occurred during the pull:\n \033[0m", e)
                    sys.exit(1)

        print("Merged Changes successfully")
    
    # If Local Repository is ahead of Remote Repository then Commit and Push
    else:
        print("Remote Repository is not up to date.")
        print("\nTrying to Push code to remote repo...")


        if repo.is_dirty(untracked_files=True):
            print("\n\033[1;31mUnresolved conflicts detected. Please resolve conflicts manually.\n\033[0m")
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
    
    
                print("\n\t\033[1;32m*** WORK SYNCED SUCCESSFULLY ***\n\033[0m")

                remote.push()

            except Exception as e:
                print("\033[1mAn error occurred during the push:\n \033[0m", e)
                print("\033[1m\nResolve Conflicts Manually !!\n \033[0m", e)
                

        else:
            print("No merge conflicts detected.")
            print("Trying to push changes to remote repo...")

            remote.push()

            print("Pushed code to remote repo")
            print("Continuing with Local Repository...")
    
    
            print("\n\t\033[1;32m*** WORK SYNCED SUCCESSFULLY ***\n\033[0m")

    

