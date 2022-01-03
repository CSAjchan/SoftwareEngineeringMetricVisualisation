from github import Github
import pygal

def main():
    print("Visualisation using Github API")
    token = input("\nEnter a Github token: ")
    
    try:
        g = Github(token)
        user = input("\nEnter a Github username: ")
        user = g.get_user(user)

        print(f"\nGithub User: {user.login} \nGithub User URL: https://github.com/{user.login}")

        getAllData(user)
    except Exception as e:
        print(e)

def getAllData(user):
    repo_languages = {}
    repo_names = []
    commit_info = []
    languages_used = {}
    forksByRepos = []

    for repo in user.get_repos():
        commits = 0

        repo_languages = repo.get_languages()
        for language in repo_languages:
            if language in languages_used:
                languages_used[language].append(repo_languages[language])
            else:
                languages_used[language] = [repo_languages[language]]

        if repo.get_stats_commit_activity():
            commits = repo.get_commits().totalCount
        else:
            commits = 0

        repo_names.append(repo.full_name)
        commit_info.append(commits)
        forksByRepos.append(repo.forks)
