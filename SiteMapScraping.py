import requests
import re
import DataBaseControl
import Models
import aiohttp
from typing import List
from sqlalchemy import create_engine

engine = create_engine('sqlite:///mydatabase.db')


class WebSrap:

    def __init__(self, url: str, name: str):
        self.url: str = url
        self.name: str = name.lower()

    @staticmethod
    def request_get(url: str) -> requests.Response:
        """
        Função para realizar o request e tratar os status code
        :param: url -> str
        :return: class requisição -> obj
        """
        response = requests.get(url)
        if response.status_code not in [200, 201, 202, 203, 204]:
            raise ConnectionRefusedError('A conexão foi recusada pelo host')
        return response

    @staticmethod
    async def async_request_get(url: str, headers: dict = None) -> aiohttp.ClientSession.get:
        """
        Função Asincrona para realizar o request e tratar os status code
        :param: url -> str
        :return: class requisição -> obj
        """
        if headers is None:
            headers = {}
        async with aiohttp.ClientSession() as session:
            async with session.get(url=url, headers=headers) as response:
                if response.status not in [200, 201, 202, 203, 204]:
                    raise ConnectionRefusedError('A conexão foi recusada pelo host')
                return await response.text()

    @staticmethod
    def __get_loc_content(data: str) -> List[str]:
        """
        Função para pegar todos os dados dentro das tags <loc></loc>
        :param data: Texto a ser filtrado -> str
        :return: Lista com o texto filtrado -> List[str]
        """
        return re.findall(r"<loc>(.*)</loc>", data)

    def get_site_map(self) -> str:
        """
        Função para pegar a url do sitemap
        :return: url -> str
        """
        response = self.request_get(self.url+'/robots.txt')
        return re.findall(r'(?<=Sitemap: ).*', response.text)[0]

    def __read_sitemap(self):
        """
        Função para carregar o sitemap
        :return: Lista de urls -> List[str]
        """
        url: str = self.get_site_map()
        if url.find('https://') == -1:
            url = 'https://' + url
        return self.request_get(url)

    def get_urls_sitemap(self) -> List[str]:
        """
        Função para retornar todas as urls do sitemap
        :return: Lista com todas as url -> List[str]
        """
        response = self.__read_sitemap()
        list_loc = self.__get_loc_content(response.text)
        return list_loc

    def get_url_products_sitemap(self) -> List[str]:
        """
        Função para retornar todas as urls de produtos do sitemap
        :return: Lista com todas as url produtos -> List[str]
        """
        response = self.__read_sitemap()
        keys = ['produtos', 'produto', 'product']
        list_url = re.findall(r"(<loc>.*?(" + "|".join(keys) + r").*?</loc>)", response.text, flags=re.IGNORECASE)
        filtered_list = []
        item: List[str]
        for item in list_url:
            filtered_list.append(item[0].replace('<loc>', '').replace('</loc>', ''))
        return filtered_list

    def get_all_url_products(self):
        list_urls = self.get_url_products_sitemap()
        new_list = []
        url: str
        for url in list_urls:
            response = self.request_get(url)
            new_list += self.__get_loc_content(response.text)
        return new_list

    @staticmethod
    def save_data(values: dict):
        session = DataBaseControl.Control().get_session()
        table = Models.ScrapedProdutos(**values)
        session.add(table)
        session.commit()

