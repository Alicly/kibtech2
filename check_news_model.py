from app import create_app, db
from app.models.news import News

app = create_app()
with app.app_context():
    print("News table columns:")
    for column in News.__table__.columns:
        print(f"  - {column.name}: {column.type}")
    
    print("\nSample news items:")
    news_items = News.query.limit(3).all()
    for news in news_items:
        print(f"  - ID: {news.id}, Title: {news.title}, Date: {news.date}")
        print(f"    Content: {news.content[:50]}...")
        print(f"    Image: {news.image_url}")
        print(f"    Published: {news.is_published}")
        print() 