import requests
from bs4 import BeautifulSoup
import json
from urllib.parse import urljoin
from datetime import datetime

# Function to scrape the article page and extract the image URL
def get_article_image_url(article_url):
    try:
        # Send a request to the article's webpage
        response = requests.get(article_url, headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(response.content, 'html.parser')

        # 1. Try og:image (Open Graph)
        og_image = soup.find('meta', property='og:image')
        if og_image and og_image.get('content'):
            return og_image['content']

        # 2. Try twitter:image (Twitter Card)
        twitter_image = soup.find('meta', property='twitter:image')
        if twitter_image and twitter_image.get('content'):
            return twitter_image['content']

        # 3. Fallback to first <img> tag (if no og or twitter image found)
        img_tag = soup.find('img')
        if img_tag and img_tag.get('src'):
            return urljoin(article_url, img_tag['src'])

        return None
    except Exception as e:
        print(f"Error fetching image for {article_url}: {e}")
        return None

def scrape_google_news():
    headers = {'User-Agent': 'Mozilla/5.0'}
    url = 'https://news.google.com/rss?hl=en-IN&gl=IN&ceid=IN:en'
    response = requests.get(url, headers=headers)
    
    # Parse the RSS feed
    soup = BeautifulSoup(response.content, 'xml')
    items = soup.find_all('item')

    articles = []
    for item in items[:100]:  # limit to 100 articles
        article_url = item.link.text
        
        # Scrape the image URL from the article page
        image_url = get_article_image_url(article_url)

        # Add article data to list
        articles.append({
            'title': item.title.text,
            'description': item.description.text,
            'url': article_url,
            'publishedAt': item.pubDate.text,
            'urlToImage': image_url  # Include the image URL if available
        })

    # Write the articles data to a JSON file
    with open('news.json', 'w', encoding='utf-8') as f:
        json.dump(articles, f, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    scrape_google_news()
