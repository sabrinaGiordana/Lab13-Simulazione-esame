from database.DB_connect import DBConnect
from model.drivers import Drivers
from model.arco import Arco

class DAO():

    @staticmethod
    def getArchi(p1, p2, anno):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)

        query = """select count(*) as N
                    from results r, results r2, races rac
                    where r.driverId = %s  and r2.driverId = %s
                    and r.position > 0 and r2.`position` >0
                    and rac.`year` = %s
                    and rac.raceId = r.raceId  and rac.raceId = r2.raceId
                    and r.position < r2.`position`"""
        cursor.execute(query, (p1.driverId, p2.driverId, anno))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        return Arco(p1, p2, row['N'])  #  ritorni un singolo oggetto Arco

    @staticmethod
    def getAnni():
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary = True)
        query = """ select s.`year` 
                    from seasons s """

        cursor.execute(query)
        for row in cursor:
            result.append(row)

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getVertici(anno):
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """ select distinct d.* 
                    from drivers d, results r , races rac
                    where rac.`year` = %s
                    and rac.raceId = r.raceId 
                    and d.driverId = r.driverId 
                    and r.`position` >0 """


        cursor.execute(query,(anno,))
        for row in cursor:
            result.append(Drivers(**row))

        cursor.close()
        conn.close()

    @staticmethod
    def getArchiV2(anno):
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """ select c.circuitId, c2.circuitId, count(distinct r2.driverId) as piloti
                    from circuits c , circuits c2 , results r , results r2, races rac , races rac3 
                    where rac3.circuitId  = c2.circuitId 
                    and rac.circuitId  = c.circuitId 
                    and r2.raceId = rac3.raceId 
                    and r.raceId = rac.raceId
                    and rac3.`year` = %s and rac.`year` = %s
                    and r2.driverId = r.driverId
                    and r.statusId = 1 
                    and r2.statusId = 1 
                    and rac.circuitId < rac3.circuitId
                    group by c.circuitId, c2.circuitId"""


        cursor.execute(query,(anno,))
        for row in cursor:
            result.append(row))

        cursor.close()
        conn.close()
        

        return result


