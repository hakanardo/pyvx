from pyvx import *

def main():
    g = Graph()
    with g:
        img = Play("test.avi")
        Show(img)
    g.verify()
    while True:
        g.process()

if __name__ == '__main__':
    main()
