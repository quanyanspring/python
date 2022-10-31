money = input('请输入您的工资:')
shop = [("iphone", 5800), ("ipod", 3000), ("book", 210), ("Archer python", 80)]
while not money.isdigit():
    print("请正确输入整数", end=':')
    money = input()
money = int(money)
while True:
    print("商品详情".center(50, '-'))
    for i in range(len(shop)):
        print("%d. %s $%s".center(50, ' ') % (i, shop[i][0], shop[i][1]))
    print("请输入你要购买的商品序号,(退出请按'q'):", end='')
    num = input()
    while not (num == 'q' or num.isdigit() and int(num) < len(shop) and int(num) >= 0):
        print("请正确输入商品序号:", end='')
        num = input()
    if num == 'q':
        break
    num = int(num)
    if money >= int(shop[num][1]):
        money -= int(shop[num][1])
        print("您购买了%s 价格为%d --您还有余额为\033[31;1m$%d\033[1m" % (shop[num][0], shop[num][1], money))
    elif money <= int(shop[num][1]):
        print("您当前余额不足,剩余余额为:\033[31;1m$%d\033[1m" % (money))
