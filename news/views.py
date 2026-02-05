from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import News, Category
from bs4 import BeautifulSoup
import feedparser

rss_links = [
    ("The Verge", "https://www.theverge.com/rss/index.xml", "Tech"),
    ("Wired", "https://www.wired.com/feed/rss", "Tech"),
    ("BBC World", "http://feeds.bbci.co.uk/news/world/rss.xml", "World"),
    ("CNN Business", "http://rss.cnn.com/rss/money_latest.rss", "Business"),
    ("Python.org", "https://www.python.org/channews.xml", "Coding"),
]

def get_image(entry):
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

    content_html = entry.get('summary', '') or entry.get('description', '')

    if content_html:
        soup = BeautifulSoup(content_html, 'html.parser')

        img_tag = soup.find('img')

        if img_tag and img_tag.get('src'):
            return img_tag['src']

    return None


def run_parser(request):
    total_added = 0

    for source_name, url, category_name in rss_links:
        print(f"Scanning: {source_name} [{category_name}]...")
        feed = feedparser.parse(url)

        category_obj, created = Category.objects.get_or_create(name=category_name)

        for entry in feed.entries:
            if News.objects.filter(link=entry.link).exists():
                continue

            News.objects.create(
                category=category_obj,
                source=source_name,
                title=entry.title,
                link=entry.link,
                pub_date=entry.get('published', 'No Date'),
                description=entry.get('description', 'No Description'),
                image_url=get_image(entry),
            )
            total_added += 1

    return HttpResponse(f"Done! Added {total_added} articles. <a href='/'>Go Home</a>")

def index(request):
    filter_category = request.GET.get('category')

    news_list = News.objects.all().order_by('-id')

    if filter_category:
        news_list = news_list.filter(category__name=filter_category)

    categories = Category.objects.all()

    context = {
        'news_list': news_list,
        'categories': categories,
        'selected_category': filter_category
    }
    return render(request, 'index.html', context)