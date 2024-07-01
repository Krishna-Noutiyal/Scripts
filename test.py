from git import Repo



repo = Repo("./")
remote = repo.remote()
diff = repo.index.diff(remote.refs[0].commit)

# print(repo.untracked_files)
# for i in diff:
#     print(i.a_path)
msg = """
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

print(msg)

# repo.index.commit("Test")