from django.db import connection
from typing import List, Dict


class SearchProduct:

    @staticmethod
    def search_ean_product(value: str, max_result: int = 5) -> List[Dict]:
        """
        Função para realizar busca no banco de dados de produtos
        :param value: conteudo a ser buscado ean ou nome
        :param max_result: numero maximo de linhas
        :return: Lista com dicionario contendo os valores da busca
        """

        if value is None:
            return []

        if value.isnumeric():
            query_filter = f"where ean = {value}"
        else:
            query_filter = f"where to_tsvector('portuguese', name) @@ websearch_to_tsquery('portuguese', '{value}')"

        query = f"""
            select ean, name
            from (select pd.ean, pd.name
                  from produtos as pd
                  UNION
                  select spd.ean, spd.name
                  from scraped_produtos as spd) as enen
            {query_filter}
            group by ean, name limit {max_result};
            """

        list_result = []

        with connection.cursor() as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()

            for row in rows:
                list_result.append(
                    {
                        "ean": row[0],
                        "name": row[1]
                    }
                )

        return list_result
