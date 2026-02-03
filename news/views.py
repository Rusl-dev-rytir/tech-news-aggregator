from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import News
from bs4 import BeautifulSoup
import feedparser

rss_links = [
    ("The Verge", "https://www.theverge.com/rss/index.xml"),
    ("TechCrunch", "https://techcrunch.com/feed/"),
    ("Wired", "https://www.wired.com/feed/rss"),
    ("BBC Tech", "http://feeds.bbci.co.uk/news/technology/rss.xml"),
    ("Habr (IT)", "https://habr.com/ru/rss/all/all/"),
]


# --- Улучшенная функция-детектив ---
def get_image(entry):
    # Уровень 1. Проверяем стандартные RSS-карманы (как раньше)
    if 'media_content' in entry and len(entry.media_content) > 0:
        if 'url' in entry.media_content[0]:
            return entry.media_content[0]['url']

    if 'media_thumbnail' in entry and len(entry.media_thumbnail) > 0:
        if 'url' in entry.media_thumbnail[0]:
            return entry.media_thumbnail[0]['url']

    if 'links' in entry:
        for link in entry.links:
            if link.get('type') in ['image/jpeg', 'image/png']:
                return link.get('href', '')

    # --- Уровень 2. Рентген (НОВОЕ!) ---
    # Если в карманах пусто, ищем внутри текста статьи.

    # 1. Берем текст описания (он может быть в 'summary' или 'description')
    content_html = entry.get('summary', '') or entry.get('description', '')

    # 2. Если текст есть, натравливаем на него BeautifulSoup
    if content_html:
        # "Свари мне суп из этого HTML"
        soup = BeautifulSoup(content_html, 'html.parser')

        # "Найди мне первый попавшийся тег <img>"
        img_tag = soup.find('img')

        # Если тег найден И у него есть ссылка (src)
        if img_tag and img_tag.get('src'):
            return img_tag['src']  # Возвращаем эту ссылку!

    # --- Уровень 3. Капитуляция ---
    # Если вообще ничего не помогло, возвращаем None (пустоту),
    # а не уродливую заглушку.
    return None


def run_parser(request):
    total_added = 0

    for source_name, url in rss_links:
        print(f"Скачиваю: {source_name}...")
        feed = feedparser.parse(url)

        for entry in feed.entries:
            if News.objects.filter(link=entry.link).exists():
                continue

            News.objects.create(
                source=source_name,
                title=entry.title,
                link=entry.link,
                pub_date=entry.get('published', 'No Date'),
                description=entry.get('description', 'No Description'),
                image_url=get_image(entry),
            )
            total_added += 1

    return HttpResponse(
        f"<h1> Готово!</h1><p>Добавлено новых статей: {total_added}</p><a href='/'>Вернуться на главную</a>")

def index(request):
    news_list = News.objects.all().order_by('-id')
    return render(request, 'index.html', {'news': news_list})