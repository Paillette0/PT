# -*- coding: utf-8 -*-
"""
Created on Sun Nov 17 15:32:52 2024

@author: kslw
"""

from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/scrape', methods=['GET'])
def scrape():
    url = "http://quotes.toscrape.com/"
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        quotes = soup.find_all('div', class_='quote')

        results = []
        for quote in quotes:
            text = quote.find('span', class_='text').text.strip()
            author = quote.find('small', class_='author').text.strip()
            tags = [tag.text for tag in quote.find_all('a', class_='tag')]
            results.append({'quote': text, 'author': author, 'tags': tags})

        return jsonify(results)
    else:
        return jsonify({'error': 'Failed to fetch data'}), 500

if __name__ == '__main__':
    app.run(debug=True)
