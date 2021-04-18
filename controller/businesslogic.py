from mtcnn.mtcnn import MTCNN
import mysql.connector
import math

def businesslogic(img):
	lowest_name = ai(img)
	return '/static/sounds/' + lowest_name + '.mp3'

def ai(img):
    face_detector = MTCNN()
    faces = face_detector.detect_faces(img)
    array = []

    for key, value in faces[0]['keypoints'].items():
        array.append(list(value))

    le_lm = math.sqrt(((array[0][0] - array[1][0]) ** 2) + ((array[0][1] - array[1][1]) ** 2))
    le_re = math.sqrt(((array[0][0] - array[4][0]) ** 2) + ((array[0][1] - array[4][1]) ** 2))
    le_n = math.sqrt(((array[0][0] - array[3][0]) ** 2) + ((array[0][1] - array[3][1]) ** 2))
    re_n = math.sqrt(((array[3][0] - array[4][0]) ** 2) + ((array[3][1] - array[4][1]) ** 2))
    re_rm = math.sqrt(((array[4][0] - array[2][0]) ** 2) + ((array[4][1] - array[2][1]) ** 2))
    rm_n = math.sqrt(((array[2][0] - array[3][0]) ** 2) + ((array[2][1] - array[3][1]) ** 2))
    lm_n = math.sqrt(((array[1][0] - array[3][0]) ** 2) + ((array[1][1] - array[3][1]) ** 2))
    rm_lm = math.sqrt(((array[1][0] - array[2][0]) ** 2) + ((array[1][1] - array[2][1]) ** 2))

    return matchFaceGetArtistName(le_re, le_n, le_lm, re_n, re_rm, rm_n, rm_lm, lm_n)

def matchFaceGetArtistName(ile_re, ile_n, ile_lm, ire_n, ire_rm, irm_n, irm_lm, ilm_n):
    db = mysql.connector.connect(
        host = 'localhost',
        user = 'ben',
        password = 'ben',
        database = 'music_artists'
    )
    cursor = db.cursor()
    query = ("SELECT artist_name, le_re, le_n, le_lm, re_n, re_rm, rm_n, rm_lm, lm_n FROM five_artists;")
    cursor.execute(query)
    lowest_value = 9999
    lowest_name = -1
    for (artist_name, le_re, le_n, le_lm, re_n, re_rm, rm_n, rm_lm, lm_n) in cursor:
        distance_sum = abs(ile_re-int(float(le_re)))+abs(ile_n-int(float(le_n)))+abs(ile_lm-int(float(le_lm)))+abs(ire_n-int(float(re_n)))+abs(ire_rm-int(float(re_rm)))+abs(irm_n-int(float(rm_n)))+abs(irm_lm-int(float(rm_lm)))+abs(ilm_n-int(float(lm_n)))
        if distance_sum<lowest_value:
            lowest_value = distance_sum
            lowest_name = artist_name
    cursor.close()
    db.close()
    return lowest_name