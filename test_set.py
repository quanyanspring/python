if __name__ == "__main__":

    file = open("/Users/admin/Desktop/transNo_set.txt", mode="r", encoding="utf-8")
    file_1 = open("/Users/admin/Desktop/test.txt", mode="r", encoding="utf-8")

    readlines = file.readlines()
    file_1 = file_1.readlines()

    set_1 = set(readlines)

    set_2 = set(file_1)

    set_3 = []
    set_4 = []
    for index, item in enumerate(set_1):
        set_3.append(item.replace("'","").replace("\n","").replace(",",""))

    for index, item in enumerate(set_2):
        set_4.append(item.replace("'","").replace("\n",""))

    dif = list(set(set_3) & set(set_4))

    dif_1 = list(set(dif) ^ set(set_4))

    for index, item in enumerate(dif_1):
        print(item)




