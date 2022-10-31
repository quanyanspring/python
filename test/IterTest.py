
if __name__ == "__main__":
    seq_tuple = (1,2,3,4,5)

    seq_it = iter(seq_tuple)

    print("第一个元素是：%s" % next(seq_it))
    print("第二个元素是：%s" % next(seq_it))
    print("第三个元素是：%s" % next(seq_it))

    i = iter(seq_tuple)
    for x in i:
        print(x,end="\n")



