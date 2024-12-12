import os
import re
import time
import platform
import pandas as pd
from flask import Flask
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin
from pyvirtualdisplay.display import Display
from typing import Optional, Union, List, Dict
from bs4 import BeautifulSoup as BS
from google.cloud import bigquery

app = Flask(__name__)

REGEX = {
    'title': re.compile(r'^titulo fuente_roboto_slab*'),
    'kicker': re.compile(r'^volanta fuente_roboto_slab*'),
    'news': re.compile(r'^slot slot_\d+ noticia*')
    }

class Scraper:
    def __init__(self):
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        self.driver  = webdriver.Chrome(options=options)
        self.page_url = 'https://www.yogonet.com/international/'
        self.all_news = list()

        try:
            if platform.system() == 'Linux':
                self.display = Display(visible=0, size=(1366, 768)).start()
        except Exception:
            pass

    def run(self):
        print("Inicio scraping")
        self.driver.get(self.page_url)
        self.scroll_down()

        html_content = self.driver.page_source
        soup = BS(html_content, 'lxml')
        raw_news = soup.find_all('div', attrs={'class': REGEX['news']})

        for raw_new in raw_news:
            payload = self.build_payload(raw_new)
            if payload:
                self.all_news.append(payload)

        self.driver.quit()
        return pd.DataFrame(self.all_news)

    def process_data(self, df):
        df["WordsCount"] = df["Title"].apply(lambda x: len(x.split()))
        df["CharCount"] = df["Title"].apply(lambda x: len(x.replace(' ', '')))
        df["CapitalizedWords"] = df["Title"].apply(lambda x: [word for word in x.split() if word.istitle()])
        return df

    def build_payload(self, raw_new):
        payload = None
        title = self.get_title(raw_new)
        kicker = self.get_kicker(raw_new)
        img = self.get_img(raw_new)
        link = self.get_url(raw_new)

        if title and kicker:
        
            payload = {
                "Title": title, 
                "Kicker": kicker,
                "Img":img,
                "Link": link
            }
            return payload

    def get_title(self, raw_new):
        title_container = raw_new.find('h2', attrs={'class': REGEX['title']})
        return title_container.text.strip() if title_container else None


    def get_kicker(self, raw_new):
        try:
            kicker = raw_new.find('div', attrs={'class': REGEX['kicker']}).text.strip()
        except AttributeError as e:
            return
        return kicker
    
    def get_img(self, raw_new):
        img_container = raw_new.find('div', attrs={'class': 'imagen'})
        return img_container.img.get('src') if img_container else None
    
    def get_url(self, raw_new):
        url_container = raw_new.find('h2', attrs={'class': REGEX['title']})
        return url_container.a.get('href') if url_container else None


    def scroll_down(self):
        footer = self.driver.find_element(By.CLASS_NAME, 'footer')
        scroll_origin = ScrollOrigin.from_element(footer, 0, -50)
        ActionChains(self.driver)\
            .scroll_from_origin(scroll_origin, 0, 200)\
            .perform()
        
    def insert_into_bigquery(self, df, insert=True):
        print("Inserting in BigQuery")
        if insert:
            project_id = os.getenv("PROJECT_ID")
            dataset = os.getenv("DATASET")
            table = os.getenv("TABLE")
            table_id = f"{project_id}.{dataset}.{table}" 

            client = bigquery.Client()
            client.load_table_from_dataframe(df, table_id).result()

@app.route('/', methods=['GET'])
def run_app():
    start_time = time.time()

    scraper = Scraper()
    scraped_data = scraper.run()
    processed_data = scraper.process_data(scraped_data)
    scraper.insert_into_bigquery(processed_data)
    data_dict = processed_data.head().to_dict(orient='records')
    scraper.insert_into_bigquery(processed_data)

    end_time =  time.time()
    time_elapsed = end_time - start_time
    print( f"Script ejecutado en {time_elapsed} segundos.")
    return {"message": "Scraping completed", "time_elapsed":time_elapsed, "data_sample": data_dict}

if __name__ == '__main__':
    app.run(port=int(os.environ.get("PORT", 8080)),host='0.0.0.0',debug=True)
