from flask import Flask, request, jsonify, render_template
import time
import random
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

folders = {
    "Nom du folder 1": ["Article A", "Article B", "Article C"],
    "Nom du folder 2": ["Article A", "Article B", "Article C"],
    "Nom du folder 3": ["Article A", "Article B"],
    "Nom du folder 4": ["Article A"]
}

def fetch_page(url, retries=5, backoff_factor=0.3):
    for i in range(retries):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                return response
            elif response.status_code == 429:
                print("Rate limit exceeded. Retrying...")
                time.sleep(backoff_factor * (2 ** i) + random.uniform(0, 1))
            else:
                print(f"Failed to retrieve page with status code: {response.status_code}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return None
    return None

@app.route('/')
def home():
    return render_template('index.html', folders=folders)

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '')
    url = 'https://www.ncbi.nlm.nih.gov/pmc/?term=' + query.replace(" ", "+")
    response = fetch_page(url)

    if response:
        soup = BeautifulSoup(response.content, 'html.parser')
        struct_div = soup.find_all('div', {'class': 'rprt'})
        
        results = []
        for card in struct_div[0:5]:
            title_tag = card.find('div', {'class': 'rslt'}).find('div', {'class': 'title'})
            if title_tag and title_tag.find('a'):
                title = title_tag.find('a').text.strip()
                link = 'https://www.ncbi.nlm.nih.gov' + title_tag.find('a')['href'] + 'pdf' if title_tag.find('a')['href'] else None
                authors = card.find('div', {'class':'desc'}).text.strip()
                publication_date = card.find('div', {'class':'details'}).find_all('span')[1].text.strip()
                results.append({
                    'title': title,
                    'link': link,
                    'authors': authors,
                    'publication_date': publication_date
                })
        return jsonify(results)
    else:
        return jsonify({'error': 'Failed to retrieve page after multiple attempts.'}), 500

@app.route('/add_folder', methods=['POST'])
def add_folder():
    folder_name = request.form['folder_name']
    if folder_name not in folders:
        folders[folder_name] = []
    return jsonify(folders)

@app.route('/delete_folder', methods=['POST'])
def delete_folder():
    folder_name = request.form['folder_name']
    if folder_name in folders:
        del folders[folder_name]
    return jsonify(folders)

@app.route('/rename_folder', methods=['POST'])
def rename_folder():
    old_name = request.form['old_name']
    new_name = request.form['new_name']
    if old_name in folders:
        folders[new_name] = folders.pop(old_name)
    return jsonify(folders)

@app.route('/add_article_to_folder', methods=['POST'])
def add_article_to_folder():
    folder_name = request.form['folder_name']
    article_name = request.form['article_name']
    if folder_name in folders:
        folders[folder_name].append(article_name)
    return jsonify(folders)

if __name__ == '__main__':
    app.run(debug=True)
