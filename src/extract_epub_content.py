import os
import zipfile
from bs4 import BeautifulSoup
import pandas as pd
import re
import shutil

def extract_epub(epub_path, extract_to):
	"""
	Décompresse un fichier EPUB dans le répertoire spécifié.
	"""
	with zipfile.ZipFile(epub_path, 'r') as zip_ref:
		zip_ref.extractall(extract_to)

def normalize_spaces(text):
	"""
	Remplace les multiples espaces par un seul espace et supprime les espaces en début et fin de chaîne.
	"""
	return re.sub(r'\s+', ' ', text).strip()

def parse_xhtml_file(file_path):
	"""
	Analyse un fichier XHTML et extrait les articles et leurs métadonnées.
	"""
	with open(file_path, 'r', encoding='utf-8') as f:
		content = f.read()
	soup = BeautifulSoup(content, features='xml')

	articles = []

	date_div = soup.find('div', class_='tetiere')
	if date_div:
		date_text = date_div.get_text(strip=True)
		if ',' in date_text:
			date = date_text.split(',')[1].strip()
		else:
			date = ''
	else:
		date = ''

	for article_div in soup.find_all('div', id=lambda x: x and x.startswith('ancre')):
		article_data = {}

		title_tag = article_div.find('h1', class_='h1')
		if title_tag:
			article_data['title'] = title_tag.get_text(separator=' ', strip=True)
			article_data['title'] = normalize_spaces(article_data['title'])
		else:
			article_data['title'] = ''

		dates_auteurs_div = article_div.find('div', class_='dates_auteurs')
		if dates_auteurs_div:
			author_span = dates_auteurs_div.find('span', class_='auteurs')
			if author_span:
				article_data['author'] = author_span.get_text(separator=' ', strip=True)
				article_data['author'] = normalize_spaces(article_data['author'])
				article_data['author'] = article_data['author'].replace('&', ' & ')
			else:
				article_data['author'] = ''
		else:
			article_data['author'] = ''

		bio_div = article_div.find('div', class_='lesauteurs')
		if bio_div:
			bio_p = bio_div.find('div', class_=lambda x: x and 'bio' in x)
			if bio_p:
				article_data['bio'] = bio_p.get_text(separator=' ', strip=True)
				article_data['bio'] = normalize_spaces(article_data['bio'])
			else:
				article_data['bio'] = ''
		else:
			article_data['bio'] = ''

		texte_div = article_div.find('div', class_='texte')
		if texte_div:
			for footnote in texte_div.find_all('span', class_='spip_note_ref'):
				footnote.decompose()

			article_text = ''
			for p in texte_div.find_all('p'):
				paragraph_text = p.get_text(separator=' ', strip=True)
				article_text += paragraph_text + '\n'

			article_data['text'] = article_text.strip()
		else:
			article_data['text'] = ''

		article_data['date'] = date

		if article_data['title'] and article_data['author'] and article_data['text']:
			articles.append(article_data)
		else:
			pass

	return articles

def process_epub(epub_file, extract_dir):
	"""
	Traite un fichier EPUB pour extraire tous les articles et leurs métadonnées.
	"""
	extract_epub(epub_file, extract_dir)

	pages_dir = os.path.join(extract_dir, 'pages')

	all_articles = []

	for filename in os.listdir(pages_dir):
		if filename.endswith('.xhtml'):
			file_path = os.path.join(pages_dir, filename)
			articles = parse_xhtml_file(file_path)
			all_articles.extend(articles)

	return all_articles

if __name__ == "__main__":
	data_dir = 'data/raw'
	extract_base_dir = 'data/extracted_epubs'

	all_articles = []

	for epub_filename in os.listdir(data_dir):
		if epub_filename.endswith('.epub'):
			epub_path = os.path.join(data_dir, epub_filename)
			extract_dir = os.path.join(extract_base_dir, os.path.splitext(epub_filename)[0])

			articles = process_epub(epub_path, extract_dir)
			all_articles.extend(articles)

			if os.path.exists(extract_dir):
				shutil.rmtree(extract_dir)

	if os.path.exists(extract_base_dir) and not os.listdir(extract_base_dir):
		os.rmdir(extract_base_dir)

	df = pd.DataFrame(all_articles)
	df.to_csv('db/articles.csv', index=False)

	print("Nombre total d'articles extraits :", len(df))
	print("\nAffichage de quelques articles :\n")
	for index, row in df.head(5).iterrows():
		print(f"Article {index+1}:")
		print(f"Titre: {row['title']}")
		print(f"Auteur: {row['author']}")
		print(f"Bio: {row['bio']}")
		print(f"Date: {row['date']}")
		print(f"Début de l'article:\n{row['text'][:500]}")
		print(f"\nFin de l'article:\n{row['text'][-500:]}")
		print("\n" + "-"*80 + "\n")