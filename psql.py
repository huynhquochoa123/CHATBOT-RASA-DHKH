import psycopg2
from underthesea import word_tokenize, ner

textwr = 'Môn toán học rời rạc có thầy cô nào dạy'

print(ner(textwr))

def create_connection():
	""" create a database connection to a postgreSQL database """
	conn = None
	try:
		conn = psycopg2.connect(user='postgres', password='123456', host='127.0.0.1', port='5432', database='DHKH_TEST')
	except (Exception, psycopg2.Error) as e:
		print(e)
	return conn

def get_info_from_masv(masv):
	conn = create_connection()
	try:
		cur = conn.cursor()
		sql = """ SELECT MaHocPhan, Score
	              FROM Score 
	              WHERE MaSinhVien = %s 
	          """
		cur.execute(sql, (masv,))
		conn.commit()
		records = cur.fetchall()
		return records
	except:
		conn.rollback()

def get_info_gv_from_mon_hoc(subjects):
	conn = create_connection()
	try:
		cur = conn.cursor()
		sql = """ SELECT GiaoVien.TenGiaoVien 
					FROM HocPhan
					join GiaoVien_HocPhan on GiaoVien_HocPhan.MaHocPhan = HocPhan.MaHocPhan
					join GiaoVien on GiaoVien_HocPhan.MaGiaoVien = GiaoVien.MaGiaoVien 
					WHERE HocPhan.TenHocPhan ilike %s
	          """
		cur.execute(sql, (subjects,))
		conn.commit()
		records = cur.fetchall()
		return records
	except:
		conn.rollback()


# if __name__ == '__main__':
# 	record = get_info_gv_from_mon_hoc('%t%o%á%n%r%ờ%i%r%ạ%c%')
#
# 	sr = ', '.join([', '.join(i) for i in record])
# 	text = "Môn học " +
# 	print(sr)

