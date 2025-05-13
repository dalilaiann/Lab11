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
    def getAllEdgesByYearColor(year, color, idMap):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)

        query = """select gds1.Product_number as p1, gds2.Product_number as p2, COUNT(DISTINCT gds1.date) as n
                    from go_daily_sales gds1, go_daily_sales gds2
                    where gds1.Product_number<gds2.Product_number and YEAR(gds1.Date)=%s and YEAR(gds1.Date)=%s
                    and gds1.date=gds2.date and gds1.Retailer_code=gds2.Retailer_code
                    group by gds1.Product_number, gds2.Product_number """

        cursor.execute(query, (year,year))
        res = []

        for row in cursor:
            o1=idMap[row["p1"]]
            o2=idMap[row["p2"]]
            if o1.Product_color==color and o2.Product_color==color:
                res.append((o1, o2, row["n"]))

        cursor.close()
        conn.close()
        return res

if __name__=="__main__":
    print(DAO.getAllNodes('Brown'))