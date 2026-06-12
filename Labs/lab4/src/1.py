from datetime import datetime, timedelta
import requests
from urllib.parse import urlparse


def get_data(url, params=None):
    response = requests.get(
        url,
        timeout=10,
        headers={"Accept": "application/vnd.github+json"},
        params=params
    )
    return response.json()


def get_all_pages(url, params=None):
    all_data = []
    page = 1
    
    while True:
        if params is None:
            params = {}
        params['page'] = page
        params['per_page'] = 100
        
        data = get_data(url, params)
        
        if not data:
            break
            
        all_data.extend(data)
        page += 1
        
        if len(data) < 100:
            break
    
    return all_data


def extract_repo_from_url(url):
    parsed = urlparse(url)
    path = parsed.path.strip('/')
    
    if 'github.com' in parsed.netloc:
        parts = path.split('/')
        if len(parts) >= 2:
            return f"{parts[0]}/{parts[1]}"
    
    return None


input_url = input("Введите ссылку на репозиторий GitHub: ")

repository = extract_repo_from_url(input_url)

if not repository:
    print("Неверная ссылка на репозиторий!")
    exit()

hours = int(input("Введите диапазон времени в часах: "))

time_limit = datetime.utcnow() - timedelta(hours=hours)

base_url = f"https://api.github.com/repos/{repository}"

print("\nЗагрузка данных...")

commits = get_all_pages(f"{base_url}/commits")

issues = get_all_pages(f"{base_url}/issues", {'state': 'all'})

pulls = get_all_pages(f"{base_url}/pulls", {'state': 'all'})

repo_info = get_data(base_url)

new_commits = 0

for commit in commits:
    try:
        commit_date = datetime.strptime(
            commit["commit"]["author"]["date"],
            "%Y-%m-%dT%H:%M:%SZ",
        )
        if commit_date > time_limit:
            new_commits += 1
    except (KeyError, TypeError):
        continue

open_issues = 0
closed_issues = 0

for issue in issues:
    if "pull_request" not in issue:
        if issue["state"] == "open":
            open_issues += 1
        elif issue["state"] == "closed":
            closed_issues += 1

open_pulls = 0
closed_pulls = 0

for pull in pulls:
    if pull["state"] == "open":
        open_pulls += 1
    elif pull["state"] == "closed":
        closed_pulls += 1

print("\nМониторинг репозитория")
print(f"Репозиторий: {repository}")
print(f"Коммитов за {hours} часов: {new_commits}")
print(f"Всего открытых issues: {open_issues}")
print(f"Всего закрытых issues: {closed_issues}")
print(f"Всего issues: {open_issues + closed_issues}")
print(f"Открытых pull requests: {open_pulls}")
print(f"Закрытых pull requests: {closed_pulls}")
print(f"Всего pull requests: {open_pulls + closed_pulls}")
print(f"Звезды: {repo_info.get('stargazers_count', 0)}")
print(f"Форки: {repo_info.get('forks_count', 0)}")