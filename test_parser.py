import feedparser

RSS_URL = "http://rss.cnn.com/rss/edition.rss"


def get_news():
    print(f"Подключаюсь к {RSS_URL}...")
    feed = feedparser.parse(RSS_URL)

    print(f"Найдено новостей: {len(feed.entries)}\n")
    for entry in feed.entries[:5]:
        print("ЗАГОЛОВОК:", entry.get("title", "Без заголовка"))
        print("ССЫЛКА:", entry.get("link", "Нет ссылки"))
        print("ОПУБЛИКОВАНО:", entry.get("published", "Дата неизвестна"))

        print("-" * 20)


if __name__ == "__main__":
    get_news()