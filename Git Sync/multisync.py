import os
import sys
import subprocess
import threading

# ANSI color codes
RESET = "\033[0m"
BOLD = "\033[1m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BLUE = "\033[94m"
CYAN = "\033[96m"

# Help message
HELP_MESSAGE = f"""
{BOLD}{CYAN}********** MULTIPLE GIT REPOSITORY SYNCHRONIZATION SCRIPT **********{RESET}

{BOLD}{CYAN}Description:{RESET}
This script automates the synchronization of multiple Git repositories using the gitsync.py script. 
It executes gitsync.py for each repository listed in a text file and manages up to 4 repositories in parallel.

{BOLD}{CYAN}Usage:{RESET}
        {YELLOW}python multisync.py <Path_to_gitsync.py> <Path_to_txt_file_with_repos>{RESET}

{BOLD}{CYAN}Parameters:{RESET}
        {YELLOW}<Path_to_gitsync.py>{RESET} : Path to the gitsync.py script.
        {YELLOW}<Path_to_txt_file_with_repos>{RESET} : Path to a text file containing the paths to local Git repositories.

{BOLD}{CYAN}Functionality:{RESET}
- Reads the text file to get the list of repository paths.
- Executes gitsync.py for each repository.
- Runs 4 repositories at a time using threading for parallel execution.
- Provides status updates for each repository as the synchronization progresses.

{BOLD}{CYAN}Output:{RESET}
- Displays status updates on synchronization for each repository.
- Logs the completion status ({GREEN}success{RESET}/{RED}failure{RESET}) for each gitsync.py execution.

{BOLD}{CYAN}Notes:{RESET}
- Ensure that gitsync.py is accessible and executable from the provided path.
- Make sure the text file with repositories contains valid paths to Git repositories.

{BOLD}{CYAN}********** END OF HELP MESSAGE **********{RESET}
"""


# Function to run gitsync.py for a given repository
def run_gitsync(gitsync_path, repo_path):
    try:
        print(
            f"{BOLD}{BLUE}Starting synchronization for repository:{RESET} {YELLOW}{repo_path}{RESET}"
        )
        # Execute gitsync.py as a subprocess
        result = subprocess.run(
            ["python", gitsync_path, repo_path], capture_output=True, text=True
        )
        if result.returncode == 0:
            print(
                f"{BOLD}{GREEN}Synchronization completed successfully for {YELLOW}{repo_path}{RESET}"
            )
        else:
            print(
                f"{BOLD}{RED}Error occurred in {YELLOW}{repo_path}{RED}:{RESET} {result.stderr}"
            )
    except Exception as e:
        print(
            f"{BOLD}{RED}An exception occurred for {YELLOW}{repo_path}{RED}:{RESET} {e}"
        )


# Function to process repositories with threading
def process_repos_in_threads(gitsync_path, repo_paths, max_threads=4):
    threads = []

    for repo_path in repo_paths:
        # Start a new thread to run gitsync.py for each repo
        thread = threading.Thread(target=run_gitsync, args=(gitsync_path, repo_path))
        threads.append(thread)
        thread.start()

        # If we have reached the max_threads limit, wait for all to finish
        if len(threads) == max_threads:
            for t in threads:
                t.join()  # Wait for all current threads to finish
            threads = []  # Reset the thread list for the next batch

    # Ensure any remaining threads are completed
    for t in threads:
        t.join()


# Main function
def main():
    if len(sys.argv) != 3:
        print(HELP_MESSAGE)
        sys.exit(1)

    gitsync_path = sys.argv[1]
    txt_file_path = sys.argv[2]

    # Check if gitsync.py exists
    if not os.path.isfile(gitsync_path):
        print(
            f"{BOLD}{RED}Error:{RESET} gitsync.py not found at {YELLOW}{gitsync_path}{RESET}"
        )
        sys.exit(1)

    # Check if the text file with repo paths exists
    if not os.path.isfile(txt_file_path):
        print(
            f"{BOLD}{RED}Error:{RESET} Repository text file not found at {YELLOW}{txt_file_path}{RESET}"
        )
        sys.exit(1)

    # Read the text file to get the repository paths
    with open(txt_file_path, "r") as file:
        repo_paths = [(line.strip()).replace("'","").replace('"','') for line in file if line.strip()]

    if not repo_paths:
        print(
            f"{BOLD}{RED}No valid repository paths found in {YELLOW}{txt_file_path}{RESET}"
        )
        sys.exit(1)

    # Run gitsync.py for each repository using threading
    process_repos_in_threads(gitsync_path, repo_paths)


if __name__ == "__main__":
    main()
