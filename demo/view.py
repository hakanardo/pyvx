from pyvx import *

def main(path="v4l2:///dev/video0"):
    g = Graph()
    with g:
        img = Play(path)
        Show(img)
    g.verify()
    while g.process() == SUCCESS:
        pass

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 2:
        print "Usage %s <video>" % sys.argv[0]
    else:
        main(*sys.argv[1:])
