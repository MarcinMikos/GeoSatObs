# Libraries
from bs4 import BeautifulSoup
import os
import requests

# The Class that loads html data
class HTMLDownloader:
    """
    The class retrieves HTML information from the IGS service.

    url - path to the website
    save_path - path to save data
    """

    def __init__(self, url, save_path):
        self.url = url
        self.save_path = save_path
        self.saved_file_path = None

    def download_html(self):
        try:
            html_response = requests.get(self.url)
            html_response.raise_for_status()
            return html_response.text
        except requests.exceptions.RequestException as e:
            print(f"Error during HTML download: {e}")
            return None

    def save_to_file(self, html_content, filename=None, custom_path=None):
        try:
            if not filename:
                filename = "output.html"
            if custom_path:
                file_path = os.path.join(custom_path, filename)
            else:
                file_path = os.path.join(self.save_path, filename)

            with open(file_path, "w", encoding="utf-8") as html_file:
                html_file.write(html_content)
            self.saved_file_path = file_path
            print(f"HTML content saved to {self.saved_file_path}")
        except Exception as e:
            print(f"Error saving HTML content to file: {e}")

    def get_unique_th_values(self):
        html_content = self.download_html()
        if html_content:
            soup = BeautifulSoup(html_content, 'html.parser')
            th_tags = soup.select('table tr > th')

            unique_th_values = []
            seen_values = set()

            for th in th_tags:
                value = th.get_text(strip=True)
                if value not in seen_values:
                    unique_th_values.append(value)
                    seen_values.add(value)

            return unique_th_values
        else:
            return []