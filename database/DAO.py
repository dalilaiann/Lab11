from database import DB_connect
from database.DB_connect import DBConnect
from model.product import Product


class DAO():
    @staticmethod
    def getAllProducts():
        conn=DBConnect.get_connection()
        cursor=conn.cursor(dictionary=True)

        query="""select *
                from go_products gp """

        cursor.execute(query)
        res=[]

        for row in cursor:
            res.append(Product(**row))

        cursor.close()
        conn.close()
        return res

    @staticmethod
    def getAllColors():
        conn=DBConnect.get_connection()
        cursor=conn.cursor(dictionary=True)

        query="""select distinct Product_color 
                from go_products gp """

        cursor.execute(query)
        res=[]

        for row in cursor:
            res.append(row["Product_color"])

        cursor.close()
        conn.close()
        return res

    @staticmethod
    def getAllNodes(color):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)

        query = """select *
                from go_products gp 
                where Product_color=%s"""

        cursor.execute(query, (color,))
        res = []

        for row in cursor:
            res.append(Product(**row))

        cursor.close()
        conn.close()
        return res

    @staticmethod
    def getAllEdgesByYearColor(u,v, year):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)

        query = """select COUNT(DISTINCT gds1.date) as n
                    from go_daily_sales gds1, go_daily_sales gds2
                    where gds1.Product_number=%s and gds2.Product_number=%s and YEAR(gds1.Date)=%s and YEAR(gds1.Date)=%s
                    and gds1.date=gds2.date and gds1.Retailer_code=gds2.Retailer_code """

        cursor.execute(query, (u.Product_number,v.Product_number,year,year))
        res=0
        for row in cursor:
            res=row["n"]

        cursor.close()
        conn.close()
        return res

if __name__=="__main__":
    print(DAO.getAllNodes('Brown'))