import csv

TRIGGER_CSV = "trigger.csv"
TRIGGER_LIST = []


def init_trigger():
    trigger_list = []
    with open(TRIGGER_CSV, newline='', encoding='UTF-8') as csvfile:
        # 讀取 CSV 檔案內容
        rows = csv.DictReader(csvfile)
        for row in rows:
            trigger_list.append(row)
    global TRIGGER_LIST
    TRIGGER_LIST = trigger_list


def add_trigger(key, value):
    init_trigger()
    with open(TRIGGER_CSV, "a+", newline='', encoding='UTF-8') as csvfile:
        r = csv.writer(csvfile)
        r.writerow([key, value])
    init_trigger()


def remove_trigger(key):
    init_trigger()
    print(TRIGGER_LIST)
    for row in TRIGGER_LIST:
        if row['key'] == key:
            TRIGGER_LIST.pop(TRIGGER_LIST.index(row))
    print(TRIGGER_LIST)
    with open(TRIGGER_CSV, "w", newline='', encoding='UTF-8') as csvfile:
        r = csv.DictWriter(csvfile, fieldnames=["key", "value"])
        r.writeheader()
        for row in TRIGGER_LIST:
            r.writerow(row)


if __name__ == '__main__':
    # add_trigger("test","312")
    # add_trigger("123","123")
    remove_trigger("test")
