from pyvx import *

def main():
    g = Graph()
    with g:
        img = Play("t.avi")
        Show(img)
    g.verify()
    while True:
        g.process()

if __name__ == '__main__':
    main()
