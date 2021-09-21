

SECTOR_SIZE = 40000


def pixels2sector(x, y):
    return str(int(x/SECTOR_SIZE+.5)) + ":" + str(int(-y/SECTOR_SIZE+.5))


def sector2pixels(sec):
    x, y = sec.split(":")
    return int(x)*SECTOR_SIZE, -int(y)*SECTOR_SIZE
