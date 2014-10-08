from pyvx import *
from time import sleep

def main():
    g = Graph()
    with g:
        img = Play("test.avi")
        Show(img)
    g.verify()
    while not g.process():
        pass

if __name__ == '__main__':
    main()
