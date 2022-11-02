import pymysql
import decimal
import csv, json, xml.etree.ElementTree as ET

class DB_Utils:

    # SQL 질의문을 전달받아 실행하는 메소드
    def queryExecutor(self, db, sql, params):
        conn = pymysql.connect(host='localhost', user='guest', password='bemyguest', db=db, charset='utf8')

        try:
            with conn.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute(sql, params)
                rows = cursor.fetchall()
                return rows
        except Exception as e:
            print(e)
            print(type(e))
        finally:
            cursor.close()
            conn.close()

    # SQL 갱신문을 전달받아 실행하는 메소드
    def updateExecutor(self, db, sql, params):
        conn = pymysql.connect(host='localhost', user='guest', password='bemyguest', db=db, charset='utf8')

        try:
            with conn.cursor() as cursor:
                cursor.execute(sql, params)
                conn.commit()
        except Exception as e:
            print(e)
            print(type(e))
        finally:
            cursor.close()
            conn.close()


class DB_Queries:

    # 검색문을 각각 하나의 메소드로 정의
    def selectAllName(self):
        sql = "SELECT DISTINCT name FROM customers ORDER BY name"
        params = ()

        util = DB_Utils()
        rows = util.queryExecutor(db="classicmodels", sql=sql, params=params)
        return rows
    def selectAllCountry(self):
        sql = "SELECT DISTINCT country FROM customers ORDER BY country"
        params = ()

        util = DB_Utils()
        rows = util.queryExecutor(db="classicmodels", sql=sql, params=params)
        return rows

    def selectAllCity(self):
        sql = "SELECT DISTINCT city FROM customers ORDER BY city"
        params = ()

        util = DB_Utils()
        rows = util.queryExecutor(db="classicmodels", sql=sql, params=params)
        return rows

    def selectCityByCountry(self, country):
        sql = "SELECT DISTINCT city FROM customers WHERE country = %s ORDER BY city"
        params = (country)

        util = DB_Utils()
        rows = util.queryExecutor(db="classicmodels", sql=sql, params=params)
        return rows

    def selectAllOrder(self):
        sql = "SELECT orderNo, orderDate, requiredDate, shippedDate, status, name AS customer, comments" \
              " FROM customers JOIN orders USING(customerId) ORDER BY orderNo"
        params = ()

        util = DB_Utils()
        rows = util.queryExecutor(db="classicmodels", sql=sql, params=params)
        return rows

    def selectOrderByName(self, name):
        sql = "SELECT orderNo, orderDate, requiredDate, shippedDate, status, name, comments" \
              " FROM customers JOIN orders USING(customerId) WHERE name = %s ORDER BY orderNo"
        params = (name)

        util = DB_Utils()
        rows = util.queryExecutor(db="classicmodels", sql=sql, params=params)
        return rows

    def selectOrderByCountry(self, country):
        sql = "SELECT orderNo, orderDate, requiredDate, shippedDate, status, name, comments" \
              " FROM customers JOIN orders USING(customerId) WHERE country = %s ORDER BY orderNo"
        params = (country)

        util = DB_Utils()
        rows = util.queryExecutor(db="classicmodels", sql=sql, params=params)
        return rows

    def selectOrderByCity(self, city):
        sql = "SELECT orderNo, orderDate, requiredDate, shippedDate, status, name, comments" \
              " FROM customers JOIN orders USING(customerId) WHERE city = %s ORDER BY orderNo"
        params = (city)

        util = DB_Utils()
        rows = util.queryExecutor(db="classicmodels", sql=sql, params=params)
        return rows

    def selectOrderDetailsByOrderNo(self, orderNo):
        sql = "SELECT orderLineNo, productCode, name, quantity, priceEach, quantity * priceEach AS 상품주문액" \
              " FROM orderDetails JOIN products USING(productCode) WHERE orderNo = %s ORDER BY orderLineNo"
        params = (orderNo)

        util = DB_Utils()
        rows = util.queryExecutor(db="classicmodels", sql=sql, params=params)
        return rows


class WriteFile():

    def writeCSV(self, orderNo, rows):
        with open(f'../files/CSV/{orderNo}.csv', 'w', encoding='utf-8', newline='') as f:
            wr = csv.writer(f)
            columnNames = list(rows[0].keys())

            wr.writerow(columnNames)
            for row in rows:
                player = list(row.values())
                wr.writerow(player)

    def writeJSON(self, orderNo, rows):
        for order in rows:
            for k, v in order.items():
                if isinstance(v, decimal.Decimal):
                    order[k] = float(v)

        newDict = dict(orderNo=rows)

        with open(f'../files/JSON/{orderNo}.json', 'w', encoding='utf-8') as f:
            json.dump(newDict, f, indent=4, ensure_ascii=False)

    def writeXML(self, orderNo, rows):
        for order in rows:
            for k, v in order.items():
                if isinstance(v, decimal.Decimal):
                    order[k] = float(v)

        newDict = dict(orderNo=rows)

        tableName = list(newDict.keys())[0]
        tableRows = list(newDict.values())[0]

        rootElement = ET.Element('Table')
        rootElement.attrib['name'] = tableName

        for row in tableRows:
            rowElement = ET.Element('Row')
            rootElement.append(rowElement)

            for columnName in list(row.keys()):
                if row[columnName] == None:
                    rowElement.attrib[columnName] = ''
                elif type(row[columnName]) in (int, float):
                    rowElement.attrib[columnName] = str(row[columnName])
                else:
                    rowElement.attrib[columnName] = row[columnName]

        ET.ElementTree(rootElement).write(f'../files/XML/{orderNo}.xml', encoding='utf-8', xml_declaration=True)