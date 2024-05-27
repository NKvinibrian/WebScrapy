from django.db import connection
from typing import List, Dict


class Seller:

    @staticmethod
    def get_all_sellers() -> List[Dict]:
        """
        Função para retornar uma lista com todos o seller
        :return: Lista de dicionario com sellers
        """
        list_sellers = []
        with connection.cursor() as cursor:
            cursor.execute("""
            select id, name, date_in from sellers where status
            """)
            rows = cursor.fetchall()
            for item in rows:
                list_sellers.append(
                    {
                        'id': item[0],
                        'name': item[1],
                        'update': str(item[2]) if item[2] else '',
                    }
                )
        return list_sellers
