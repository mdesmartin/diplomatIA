# extract_articles.py

import os
import zipfile
from bs4 import BeautifulSoup
import re
import shutil

def extract_epub(epub_path, extract_to):
    with zipfile.ZipFile(epub_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)

def normalize_spaces(text):
    return re.sub(r'\s+', ' ', text).strip()

def parse_xhtml_file(file_path, date):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    soup = BeautifulSoup(content, features='xml')

    articles = []

    # Find all divs with id starting with 'ancre'
    for article_div in soup.find_all('div', id=lambda x: x and x.startswith('ancre')):
        article_data = {}

        # Title
        title_tag = article_div.find('h1', class_='h1')
        if title_tag:
            article_data['title'] = normalize_spaces(title_tag.get_text(separator=' ', strip=True))
        else:
            continue  # Skip if no title

        # Author
        dates_auteurs_div = article_div.find('div', class_='dates_auteurs')
        if dates_auteurs_div:
            author_span = dates_auteurs_div.find('span', class_='auteurs')
            if author_span:
                author = normalize_spaces(author_span.get_text(separator=' ', strip=True))
                article_data['author'] = author.replace('&', ' & ')
            else:
                continue  # Skip if no author
        else:
            continue  # Skip if no author

        # Bio
        bio_div = article_div.find('div', class_='lesauteurs')
        if bio_div:
            bio_p = bio_div.find('div', class_=lambda x: x and 'bio' in x)
            if bio_p:
                article_data['bio'] = normalize_spaces(bio_p.get_text(separator=' ', strip=True))
            else:
                article_data['bio'] = ''
        else:
            article_data['bio'] = ''

        # Text
        texte_div = article_div.find('div', class_='texte')
        if texte_div:
            # Remove footnotes
            for footnote in texte_div.find_all('span', class_='spip_note_ref'):
                footnote.decompose()

            article_text = ''
            for p in texte_div.find_all('p'):
                paragraph_text = p.get_text(separator=' ', strip=True)
                article_text += paragraph_text + '\n'

            article_data['text'] = article_text.strip()
        else:
            continue  # Skip if no text

        # Date
        article_data['date'] = date

        articles.append(article_data)

    return articles

def extract_articles_from_epub(epub_file, extract_dir):
    # Extract EPUB
    extract_epub(epub_file, extract_dir)

    # Get date from the file
    date = ''
    for root, dirs, files in os.walk(extract_dir):
        for file in files:
            if file.endswith('.xhtml'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                soup = BeautifulSoup(content, features='xml')
                date_div = soup.find('div', class_='tetiere')
                if date_div:
                    date_text = date_div.get_text(strip=True)
                    if ',' in date_text:
                        date = date_text.split(',')[1].strip()
                    else:
                        date = ''
                    break
        if date:
            break

    # Parse articles
    articles = []
    pages_dir = os.path.join(extract_dir, 'pages')
    for filename in os.listdir(pages_dir):
        if filename.endswith('.xhtml'):
            file_path = os.path.join(pages_dir, filename)
            articles.extend(parse_xhtml_file(file_path, date))

    # Clean up extracted files
    shutil.rmtree(extract_dir)

    return articles

def extract_all_articles(data_dir):
    extract_base_dir = 'data/extracted_epubs'
    all_articles = []

    for epub_filename in os.listdir(data_dir):
        if epub_filename.endswith('.epub'):
            epub_path = os.path.join(data_dir, epub_filename)
            extract_dir = os.path.join(extract_base_dir, os.path.splitext(epub_filename)[0])

            articles = extract_articles_from_epub(epub_path, extract_dir)
            all_articles.extend(articles)

    return all_articles

if __name__ == "__main__":
    data_dir = 'data/raw'
    articles = extract_all_articles(data_dir)
    print(f"Total articles extracted: {len(articles)}")
    # You can save articles to a file or pass them directly to the next script