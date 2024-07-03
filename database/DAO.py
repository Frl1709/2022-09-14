from database.DB_connect import DBConnect
from model.album import Album


class DAO():

    @staticmethod
    def getNodes(durata):
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """select a.AlbumId, a.Title, a.ArtistId, sum(t.Milliseconds) as Durata
                    from track t, album a 
                    where t.AlbumId = a.AlbumId 
                    group by a.AlbumId 
                    having durata >= %s"""
        cursor.execute(query, (durata, ))
        for row in cursor:
            result.append(Album(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getEdge(idMap):
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """SELECT distinctrow t.AlbumId as a1, t2.AlbumId as a2
                    FROM playlisttrack p , track t , playlisttrack p2 , track t2 
                    WHERE p2.PlaylistId = p.PlaylistId
                    and p2.TrackId = t2.TrackId 
                    and p.TrackId = t.TrackId
                    and t.AlbumId < t2.AlbumId"""
        cursor.execute(query, )
        for row in cursor:
            if row["a1"] in idMap and row["a2"] in idMap:
                result.append((idMap[row["a1"]],
                               idMap[row["a2"]]))

        cursor.close()
        conn.close()
        return result
