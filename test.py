from git import Git,Repo, Remote


cdw = "S:\\C_Plus_Plus"

repo = Repo(cdw)
remote = repo.remote("origin")

# d = [i[0] for i in repo.index.entries.keys()]
# d = [i for i in repo.index.diff(remote.refs[0].commit)]


print(len(repo.index.diff(None)))
# print(d)