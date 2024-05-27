from SiteMapScraping import WebScrap
import re
import asyncio
import aiohttp
import datetime


class Nissei(WebScrap):
    
    def __init__(self):
        super().__init__('https://www.farmaciasnissei.com.br', 'Nissei')
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0'
        }

    @staticmethod
    async def get_cookies(url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                cookies = response.cookies
                return cookies

    @staticmethod
    async def post_request(url, cookies, data, headers):
        form_data = aiohttp.FormData()
        for key, value in data.items():
            form_data.add_field(key, value)

        async with aiohttp.ClientSession() as session:
            async with session.post(url, data=form_data, cookies=cookies, headers=headers) as response:
                return await response.text()

    async def get_price(self, codigo):
        url = self.url + '/pegar/preco'
        cookies = await self.get_cookies(self.url)

        headers = {
            'Referer': url,
            'X-CSRFToken': cookies.get('csrftoken').value, }

        payload = {'produtos_ids[]': codigo}

        response = await self.post_request(url=url, headers=headers, data=payload, cookies=cookies)
        result = re.findall(r'\"valor_fim\": \"(.*?)\",', response)
        value = 0
        if result:
            value = float(result[0])
            for item in result:
                item = float(item)
                if item < value:
                    value = item
        return value

    async def scraping(self, url: str):
        print('Iniciando: {}'.format(url))
        response = await self.async_request_get(url, headers=self.headers)
        data = {
            'ean': None,
            'value': 0,
            'name': None,
            'seller': self.name,
        }

        pattern = r"<span class=\"mr-3\">(.*?)</span>"
        result = re.findall(pattern, response)
        result = result[0] if result else None
        if result is None:
            print('{} EAN não encontrado em {}'.format(self.name, url))
            return

        result = re.findall(r"\d+", result)
        result = result[0] if result else None
        data['ean'] = result

        if data['ean'] is None:
            print('{} EAN não encontrado em {}'.format(self.name, url))
            return

        pattern = r"<span class=\"ml-3\">(.*?)</span>"
        result = re.findall(pattern, response)
        result = result[0] if result else None
        result = re.findall(r"\d+", result)
        result = result[0] if result else None
        codigo = result
        if codigo:
            data['value'] = await self.get_price(codigo)

        result = response.strip().replace('\n', '').replace('\r', '')
        pattern = r'<h1 data-target=\"nome_produto\" style=\"font-size: 25px !important;\" class=\"font-weight-bold text-extradark-grey\">(.*?)</h1>'
        result = re.findall(pattern, result)
        result = result[0] if result else None
        data['name'] = result.strip()

        self.save_data(data)

    async def __asyc_run(self):
        list_url = self.get_all_url_products()
        lista_separada = []
        tamanho_sublista = 1000
        for i in range(0, len(list_url), tamanho_sublista):
            lista_separada.append(list_url[i:i + tamanho_sublista])
        for i in lista_separada:
            tasks = [asyncio.create_task(self.scraping(item)) for item in i]
            done, padding = await asyncio.wait(tasks)

    def run(self):
        dat_init = datetime.datetime.now()
        print('Iniciado Scraping em: {}'.format(dat_init))
        asyncio.run(self.__asyc_run())
        print('Finalizado em {}'.format(datetime.datetime.now()))
        print('Total de tempo {}'.format(datetime.datetime.now() - dat_init))
