from git import Repo, Remote, GitCommandError
import sys



def Commit_Dates(repo: Repo, remote: Remote) -> bool:
    """`Return`: `Tuple(int)` a tuple of two integer elements reperentation of commit date.
    Where the first element is `Local_`Commit_Date`` and the second element is `Remote_Commit_Date`
    """
    
    
    last_commit_local = repo.head.commit.committed_date
    last_commit_remote = remote.refs[0].commit.committed_date 

    return (last_commit_local,last_commit_remote)


if __name__ == "__main__":


    HELP = """
\033[1;34m\t\t********** GIT AUTOMATION SCRIPT **********\033[0m

\033[1;32m\tDescription:\033[0m
\tThis script automates the process of committing changes to your local Git repository and 
\tpushing them to a remote repository. It handles checking for untracked files, modified files,
\tcommitting changes locally, and ensuring your remote repository is up-to-date.

\033[1;32m\tUsage:\033[0m
\t\t\033[1;33mpython gitsync.py <Local_Repository_Path>\033[0m

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

    args = sys.argv


    if len(args) < 2:
        print(HELP)
        exit()

    
    DIR = args[1]

    repo = Repo(DIR)
    remote = repo.remote("origin")
    print(repo.git.status())

    
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

        remote.fetch()
        print("Fetched Changes successfully")
        
        Check_Difference = repo.index.diff(remote.refs[0].commit)

        # If Changes are found then Merge Changes
        if len(Check_Difference) > 0:  
            print("Merging changes...")
            
            # Merging Changes *** Merge --allow-unrelated-histories ***
            # if normal merge is not possible and return status is is 128 then use --allow-unrelated-histories
            try:
                repo.git.merge(remote.refs[0])
            except GitCommandError as e:
                if e.status == 128:
                    repo.git.merge(remote.refs[0], '--allow-unrelated-histories')

            print("Merged Changes successfully")
    
    # If Local Repository is ahead of Remote Repository then Commit and Push
    else:
        print("Remote Repository is not up to date.")
        print("\nPushing code remote repo...")

        remote.push()
        

        print("Pushed code to remote repo")
        print("Continuing with Local Repository...")
    

    

    diff = repo.index.diff(None)
    flags = {"d":0,"u":len(repo.untracked_files),"m":0} # d = deleted, u = untracked, m = modified

    for i in repo.untracked_files:
        print(f"\t\033[1;33mUntracked:\033[0m {i}")
    repo.index.add(repo.untracked_files)



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
        

    msg = "Automatic Commit : " + f"Added {flags["u"]} Files, " if flags["u"] !=0 else "" + "Deleted Files, " if flags["d"] !=0 else "" + "Modified Files " if flags["m"] !=0 else ""



    # Committing Changes
    if flags["d"] > 0 or flags["u"] > 0 or flags["m"] > 0:
        print("\nCommitting changes locally...")
        repo.index.commit("Auto Commit")

    else:
        print("No changes found in local repository")

    

    Date_of_Commits = Commit_Dates(repo, remote)
    L_commit, R_commit = Date_of_Commits[0], Date_of_Commits[1]

    if L_commit == R_commit:
        print("No changes found.")
    
    else:
        print("Changes found.")

        print("Files to be committed:\n")

        for item in repo.index.diff(remote.refs[0].commit): 
            print(f"\t{item.a_path}")


        print("\nPushing Code To Remote...")

        # msg = input("\n\tEnter commit message: ")

        remote.push()

        # status of Local Git Repository
        print(repo.git.status())

    
    print("\n\t*** WORK SYNCED SUCCESSFULLY ***\n")

    
