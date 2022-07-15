import csv


TRIGGER_CSV="trigger.csv"
TRIGGER_LIST = []

def init_trigger():
	with open(TRIGGER_CSV, newline='') as csvfile:
		# 讀取 CSV 檔案內容
		rows = csv.DictReader(csvfile)
		for row in rows:
			TRIGGER_LIST.append(row)
			
def add_trigger(key,value):
	with open(TRIGGER_CSV, "a+") as csvfile:
		r = csv.writer(csvfile)
		r.writerow([key,value])
	init_trigger()
