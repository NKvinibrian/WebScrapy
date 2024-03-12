from SiteMapScraping import WebSrap
import re
import asyncio
import requests


class Nissei(WebSrap):
    
    def __init__(self):
        super().__init__('https://www.farmaciasnissei.com.br', 'Nissei')
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0'
        }

    async def pegar_preco(self, codigo):
        s = requests.session()
        url = self.url + '/pegar/preco'
        s.get(self.url)

        headers = {
            'Referer': url,
            'X-CSRFToken': s.cookies.get('csrftoken'), }

        payload = {'produtos_ids[]': codigo}

        response = s.request("POST", url, headers=headers, data=payload)
        result = re.findall(r'\"valor_fim\": \"(.*?)\",', response.text)
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
        result = re.findall(pattern, response.text)
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
        result = re.findall(pattern, response.text)
        result = result[0] if result else None
        result = re.findall(r"\d+", result)
        result = result[0] if result else None
        codigo = result
        if codigo:
            data['value'] = await self.pegar_preco(codigo)

        result = response.text.strip().replace('\n', '').replace('\r', '')
        pattern = r'<h1 data-target=\"nome_produto\" style=\"font-size: 25px !important;\" class=\"font-weight-bold text-extradark-grey\">(.*?)</h1>'
        result = re.findall(pattern, result)
        result = result[0] if result else None
        data['name'] = result.strip()

        self.save_data(data)

    async def __asyc_run(self):
        list_url = self.get_all_url_products()
        tasks = [asyncio.create_task(self.scraping(item)) for item in list_url]
        done, padding = await asyncio.wait(tasks)

    def run(self):
        asyncio.run(self.__asyc_run())
        print('Finalizado')


