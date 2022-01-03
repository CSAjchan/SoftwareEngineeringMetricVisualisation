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

    doTheVisualisation(user, repo_names, commit_info, languages_used, forksByRepos)

def doTheVisualisation(user, repo_names, commit_info, languages_used, forksByRepos):
    #overall languages used pie chart for the user(number of charactes written in each language)
    language_pie_chart = pygal.Pie(height = 1000, width = 1000, explicit_size = 1000)
    language_pie_chart._title = f'Languages used by {user.login}'
    languages = languages_used.keys()
    for language in languages:
        language_pie_chart.add(language, languages_used[language])
    language_pie_chart.render_in_browser()

    #commits bar chart for each repository
    commits_bar_chart = pygal.Bar(height = 1000, width = 1000, explicit_size = 1000)
    commits_bar_chart.title = f'Commits for different Repositories by {user.login}'
    commits_bar_chart.x_labels = map(str, repo_names)
    commits_bar_chart.add("Commits", commit_info)
    commits_bar_chart.render_in_browser()

    #followers vs following gauge chart
    following_gauge_chart = pygal.Gauge(height = 1000, width = 1000, explicit_size = 1000)
    following_gauge_chart.title = f'Following vs Followers for the {user.login}'
    following_gauge_chart.add("Following", user.following)
    following_gauge_chart.add("Followers", user.followers)
    following_gauge_chart.render_in_browser()

    #number of times each repository was forked by other users from the user we inquired about
    forks_line_chart = pygal.Line(height = 1000, width = 1000, explicit_size = 1000)
    forks_line_chart.title = f'Number of forks from a repositories from {user.login}'
    forks_line_chart.x_labels = map(str, repo_names)
    forks_line_chart.add("Forks", forksByRepos)
    forks_line_chart.render_in_browser()

if __name__ == "__main__":
    main()