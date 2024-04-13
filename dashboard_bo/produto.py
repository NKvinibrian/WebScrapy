from builtins import staticmethod

from django.db import connection
from datetime import datetime


class Produto:

    def __init__(self, product_id: int = None, ean: int = None):
        self.product_id = product_id
        self.ean = ean

    @staticmethod
    def get_all_products_filtered() -> list[dict]:
        list_products = []
        with connection.cursor() as cursor:
            cursor.execute("""
            SELECT pd.ean, pd.id, pd.name, pd.value, pd.date_in
            FROM produtos AS pd
            INNER JOIN (
            SELECT ean, MAX(date_in) AS max_date
            FROM produtos
            GROUP BY ean
            ) AS pd_max ON pd.ean = pd_max.ean AND pd.date_in = pd_max.max_date
            WHERE pd.status;
            """)
            rows = cursor.fetchall()
            for row in rows:
                list_products.append(
                    {
                        "id": row[1],
                        "ean": row[0],
                        "name": row[2],
                        "value": row[3],
                        "data": str(row[4]) if row[4] else None
                    }
                )
            return list_products

    def __check__product_id(self) -> None:
        try:
            self.product_id = int(self.product_id)
        except:
            raise ValueError('O id precisar ser do tipo int')

    def get_product(self):
        self.__check__product_id()

        with connection.cursor() as cursor:
            cursor.execute("""
            SELECT pd.ean, pd.id, pd.name, pd.value, pd.date_in
            FROM produtos AS pd
            WHERE pd.status and pd.id = {}
            """.format(self.product_id))
            row = cursor.fetchone()
        if row:
            return {
                "id": row[1],
                "ean": row[0],
                "name": row[2],
                "value": row[3],
                "data": str(row[4]) if row[4] else None
            }
        return {}

    def update_product(self, fields: dict) -> None:
        self.__check__product_id()
        fiels_text = ''.join([f"{coluna} = {fields[coluna]}" for coluna in fields.keys()])

        query = f"UPDATE produtos SET {fiels_text} WHERE id = {self.product_id}"

        with connection.cursor() as cursor:
            cursor.execute(query)

    def delete_product(self) -> None:
        self.__check__product_id()
        with connection.cursor() as cursor:
            cursor.execute("UPDATE produtos SET status = %s WHERE id = %s", [False, self.product_id])

    @staticmethod
    def set_product(data: dict) -> None:
        with connection.cursor() as cursor:
            colunas = ', '.join(data.keys())
            values = ', '.join([f'\'{value}\'' for value in data.values()])
            colunas += ', status, date_in'
            values += f', true, \'{str(datetime.now())}\''
            sql = f"INSERT INTO produtos ({colunas}) VALUES ({values})"
            cursor.execute(sql, list(data.values()))
