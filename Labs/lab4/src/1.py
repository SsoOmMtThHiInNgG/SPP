from datetime import datetime, timedelta
import requests
from urllib.parse import urlparse
import qrcode
from PIL import Image
import os


def get_data(url, params=None):
    try:
        response = requests.get(
            url,
            timeout=10,
            headers={"Accept": "application/vnd.github+json"},
            params=params
        )
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Ошибка {response.status_code} при запросе {url}")
            return None
    except Exception as e:
        print(f"Исключение при запросе {url}: {e}")
        return None


def get_all_pages(url, params=None):
    all_data = []
    page = 1
    
    while True:
        if params is None:
            params = {}
        params['page'] = page
        params['per_page'] = 100
        
        data = get_data(url, params)
        
        if data is None:
            break
        
        if isinstance(data, dict) and 'message' in data:
            print(f"API ошибка: {data['message']}")
            break
            
        if not isinstance(data, list):
            break
            
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
            return f"{parts[0]}/{parts[1]}", f"https://github.com/{parts[0]}/{parts[1]}"
    
    return None, None


def generate_qr_code(url, filename="repository_qr.png"):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    
    qr_image = qr.make_image(fill_color="black", back_color="white")
    qr_image.save(filename)
    
    return filename


def calculate_stats(commits, issues_closed, pulls_closed, stars, forks):
    kr_score = 0
    max_score = 100
    
    kr_score += min(commits * 2, 30)
    kr_score += min(issues_closed * 3, 25)
    kr_score += min(pulls_closed * 4, 25)
    kr_score += min(stars * 1, 10)
    kr_score += min(forks * 1, 10)
    
    kr_percentage = (kr_score / max_score) * 100
    
    if kr_percentage >= 90:
        grade = "A+ (Отлично)"
    elif kr_percentage >= 80:
        grade = "A (Очень хорошо)"
    elif kr_percentage >= 70:
        grade = "B (Хорошо)"
    elif kr_percentage >= 60:
        grade = "C (Удовлетворительно)"
    elif kr_percentage >= 50:
        grade = "D (Слабо)"
    else:
        grade = "F (Неудовлетворительно)"
    
    return kr_percentage, grade


input_url = input("Введите ссылку на репозиторий GitHub: ")

repository, full_url = extract_repo_from_url(input_url)

if not repository:
    print("Неверная ссылка на репозиторий!")
    exit()

hours = int(input("Введите диапазон времени в часах: "))

time_limit = datetime.utcnow() - timedelta(hours=hours)

base_url = f"https://api.github.com/repos/{repository}"

print("\nЗагрузка данных...")

commits = get_all_pages(f"{base_url}/commits")

if not isinstance(commits, list):
    commits = []

issues = get_all_pages(f"{base_url}/issues", {'state': 'all'})

if not isinstance(issues, list):
    issues = []

pulls = get_all_pages(f"{base_url}/pulls", {'state': 'all'})

if not isinstance(pulls, list):
    pulls = []

repo_info = get_data(base_url)

if repo_info is None or (isinstance(repo_info, dict) and 'message' in repo_info):
    print(f"Не удалось получить информацию о репозитории: {repo_info.get('message', 'Неизвестная ошибка') if repo_info else 'Нет данных'}")
    exit()

new_commits = 0

for commit in commits:
    try:
        if isinstance(commit, dict) and 'commit' in commit and 'author' in commit['commit']:
            commit_date = datetime.strptime(
                commit["commit"]["author"]["date"],
                "%Y-%m-%dT%H:%M:%SZ",
            )
            if commit_date > time_limit:
                new_commits += 1
    except (KeyError, TypeError, ValueError):
        continue

open_issues = 0
closed_issues = 0

for issue in issues:
    try:
        if isinstance(issue, dict) and "pull_request" not in issue:
            if issue.get("state") == "open":
                open_issues += 1
            elif issue.get("state") == "closed":
                closed_issues += 1
    except (KeyError, TypeError):
        continue

open_pulls = 0
closed_pulls = 0

for pull in pulls:
    try:
        if isinstance(pull, dict):
            if pull.get("state") == "open":
                open_pulls += 1
            elif pull.get("state") == "closed":
                closed_pulls += 1
    except (KeyError, TypeError):
        continue

print("\n" + "="*50)
print("МОНИТОРИНГ РЕПОЗИТОРИЯ")
print("="*50)
print(f"Репозиторий: {repository}")
print(f"Период: последние {hours} часов")
print("-"*50)
print(f"📝 Коммитов за период: {new_commits}")
print(f"🐛 Открытых issues: {open_issues}")
print(f"✅ Закрытых issues: {closed_issues}")
print(f"🔀 Открытых pull requests: {open_pulls}")
print(f"✨ Закрытых pull requests: {closed_pulls}")
print(f"⭐ Звезды: {repo_info.get('stargazers_count', 0)}")
print(f"🍴 Форки: {repo_info.get('forks_count', 0)}")
print("="*50)

print("\n📱 ГЕНЕРАЦИЯ QR-КОДА")
print("="*50)

qr_filename = generate_qr_code(full_url)

print(f"✅ QR-код создан: {qr_filename}")
print(f"🔗 Ссылка: {full_url}")

try:
    img = Image.open(qr_filename)
    img.show()
    print("🖼️ QR-код открыт в просмотрщике изображений")
except Exception as e:
    print(f"Не удалось открыть изображение: {e}")
    print(f"Файл сохранен как: {qr_filename}")

print("="*50)