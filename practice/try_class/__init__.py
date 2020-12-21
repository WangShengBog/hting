
__author__ = 'bog'
__doc__ = """"""


class Robot:
    total = 0

    @classmethod
    def __init__(cls):
        cls.total += 1
        print(f"现在有{cls.total}个robot")

    @classmethod
    def __del__(cls):
        cls.total -= 1
        print(f"死了一个 还剩{cls.total}个")


if __name__ == '__main__':
    a = Robot()
    b = Robot()
    c = Robot()
