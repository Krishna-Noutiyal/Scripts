from git import Repo, Remote    

import sys


def Commit_Changes(remote:Remote, repo:Repo = None, message:str = None, only_remote:bool=False) -> None:
    """### Inputs:
        `repo`: Local Git Repository
        `remote`: Remote Git Repository
        `message`: Commit Message
        `only_remote`: `True` if you want to push to remote repo only, else `False`

        By Default commit is done locally. Rquires `remote`, `repo` and `message` 

    #### If  `only_remote` is True :
        Changes are pushed to remote repo only.
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


def Commit_Dates(repo: Repo, remote: Remote) -> bool:
    """`Return`: `Tuple(int)` a tuple of two integer elements reperentation of commit date.
    Where the first element is `Local_`Commit_Date`` and the second element is `Remote_Commit_Date`
    """
    
    
    last_commit_local = repo.head.commit.committed_date
    last_commit_remote = remote.refs[0].commit.committed_date 

    return (last_commit_local,last_commit_remote)


def Check_Untraced_Files(repo:Repo) -> list[str] | None:
    """### Inputs:
        `repo`: Local Git Repository

        Checks if there are any untracked files in the local repository

    ### Returns: 
    `List[str]` of untracked files if any else `none`

    """
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
        print(HELP)
        exit()

    DIR = args[1]

    # Change Commit Message as you wish
    MSG = "Automated Commit"

    repo = Repo(DIR)
    remote = repo.remote("origin")
    print(repo.git.status())

    
    # Checking and adding untraced files to staging area ( including commit )
    print("Checking for untracked files...")

    UT_FILES = Check_Untraced_Files(repo)

    if UT_FILES is not None:

        print("Untracked files found:")
        print("\n".join(UT_FILES))
        print("Pushing untracked files to stagging area...")

        repo.index.add(UT_FILES)
        Commit_Changes(remote, repo,MSG)

    else:
        print("No untracked files found.")
    

    """
    *********** CHECKING FOR COMMIT DIFFERENCES ***********
    This section checks if the local and remote repositories are in sync
    If Both the repositories are not in sync. Tries to SYNC both repository
    """

    # Fetching and merging changes from Remote Repository
    Date_of_Commits = Commit_Dates(repo, remote)
    L_commit, R_commit = Date_of_Commits[0], Date_of_Commits[1]

    if L_commit == R_commit:
        print("Both Local and Remote Repositories are in SYNC")
        pass
    
    #If Local Repository is behind Remote Repository then Fetch and Merge Changes
    elif L_commit < R_commit:
        print("Checking for changes in Remote Repository...")

        print("Remote Repository is up to date")
        print("Local Repository might be Outdated")
        print("\nFetching Changes...")

        remote.fetch()
        print("Fetched Changes successfully")
        
        # Check_Difference = repo.index.diff(remote.refs[0].commit)

        # # If Changes are found then Merge Changes
        # if len(Check_Difference) > 0:  
        print("Merging changes...")
        repo.git.merge(remote.refs[0])
        print("Merged Changes successfully")
    
    # If Local Repository is ahead of Remote Repository then Commit and Push
    else:
        print("Remote Repository is not up to date.")
        print("\nPushing code remote repo...")

        Commit_Changes(remote, only_remote=True)
        

        print("Pushed code to remote repo")
        print("Continuing with Local Repository...")

    
    print("Checking for file modifications...")

    # assert not repo.is_dirty();

    # Check for changes in Local Repository
    if not Commit_Dates(repo, remote):
        print("No changes found.")
    
    else:
        print("Changes found.")

        print("Files to be committed:\n")

        for item in repo.index.diff(remote.refs[0].commit): 
            print(f"\t{item.a_path} -> {item.b_path}")


        print("\nCommiting changes locally and pushing to remote...")

        # msg = input("\n\tEnter commit message: ")


        Commit_Changes(remote, repo, MSG)

        # status of Local Git Repository
        print(repo.git.status())

    
    print("\n\t*** WORK SYNCED SUCCESSFULLY ***\n")
    # print(args)

    
