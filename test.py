from git import Repo



repo = Repo("./")
remote = repo.remote()
# diff = repo.index.diff(remote.refs[0].commit)

print(repo.untracked_files)



repo.index.commit("Test")