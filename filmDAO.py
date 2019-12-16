import mysql.connector


class FilmDAO:
    db = ""

    def __init__(self):
        self.db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="GaBi2011",
        #user="datarep",  # this is the user name on my mac
        #passwd="password" # for my mac
        database="datarepresentation"
        )

    def create(self, values):
        cursor = self.db.cursor()
        sql = "insert into film (title, genre, director, price) values (%s,%s,%s,%s)"
        cursor.execute(sql, values)

        self.db.commit()
        return cursor.lastrowid

    def getAll(self):
        cursor = self.db.cursor()
        sql = "select * from film"
        cursor.execute(sql)
        results = cursor.fetchall()
        returnArray = []
        print(results)
        for result in results:
            print(result)
            returnArray.append(self.convertToDictionary(result))

        return returnArray

    def findByID(self, id):
        cursor = self.db.cursor()
        sql = "select * from film where id = %s"
        values = (id,)

        cursor.execute(sql, values)
        result = cursor.fetchone()
        return self.convertToDictionary(result)

    def update(self, values):
        cursor = self.db.cursor()
        sql = "update film set title= %s, genre=%s, director=%s, price=%s  where id = %s"
        cursor.execute(sql, values)
        self.db.commit()

    def delete(self, id):
        cursor = self.db.cursor()
        sql ="delete from film where id = %s"
        values = (id,)

        cursor.execute(sql, values)

        self.db.commit()
        print("delete done")

    def convertToDictionary(self, result):
        colnames = ['id', 'Title', 'Genre', 'Director', 'Price']

        item = {}

        if result:

            for i, colName in enumerate(colnames):
                value = result[i]
                item[colName] = value

        return item


filmDAO = FilmDAO()

