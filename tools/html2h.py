from HTMLParser import HTMLParser
import sys

class MyHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.path = []
        self.class_path = []
        self.out = sys.stdout

    def handle_starttag(self, tag, attrs):
        self.path.append(tag)
        cls = dict(attrs).get('class')
        self.class_path.append(cls)
        if cls == 'lineno':
            self.out.write('\n')
        #print ' ' * len(self.path), tag, cls

    def handle_endtag(self, tag):
        assert self.path[-1] == tag
        self.path.pop()
        self.class_path.pop()

    def handle_data(self, data):
        if 'line' in self.class_path and 'lineno' not in self.class_path:
            self.out.write(data)

    def handle_entityref(self, name):
        self.handle_data({'quot': '"', 'lt': '<', 'gt': '>',
                        'amp': '&'}[name])

    def handle_charref(self, name):
        i = int(name)
        if i < 127:
            self.handle_data(chr(i))

parser = MyHTMLParser()
parser.feed(open(sys.argv[1]).read())
parser.out.write('\n')
