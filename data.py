'''UK House Price data

extracted links from html source of 
http://www.nationwide.co.uk/hpi/historical.htm
'''
import os
import logging

logger = logging.getLogger(__name__)

base = 'http://www.nationwide.co.uk/hpi/'
fns = [
    'downloads/UK_house_price_since_1952.xls',
    ]
urls = [ base + fn for fn in fns ]

from swiss.cache import Cache 
import swiss.tabular as T
cache = os.path.join(os.path.dirname(__file__), 'cache')
retriever = Cache(cache)

class Parser(object):

    def download(self):
        self.localfps = [ retriever.retrieve(url) for url in urls ]

    def extract(self):
        logger.info('Extracting data from Xls')
        self.download()
        fp = self.localfps[0]
        reader = T.XlsReader(fp)
        # notes are on 2nd page but ignore for time being
        tdata = reader.read()
        data = tdata.data
        out = T.TabularData()
        out.header = [ 'Date', 'Price (All)', 'Price (New)', 'Price (Modern)', 'Price (Older)' ]
        data = data[6:]
        data = zip(*data)
        def fix_date(indate): # e.g Q1 1952
            q,year = indate.split()
            return int(year) + int(q[1])/4.0
        data = [ [fix_date(x) for x in data[0]], data[2], data[5], data[8], data[11] ]
        out.data = list(zip(*data))
        # outfp = 'data.js'
        # writer = T.JsonWriter()
        outfp = 'data.csv'
        writer = T.CsvWriter()
        writer.write(out, open(outfp, 'w'))
        logger.info('Data successfully extracted to: %s' % outfp)

import optparse
import inspect
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    methods = dict(inspect.getmembers(Parser, lambda x: inspect.ismethod(x) and not
            x.__name__.startswith('_')))
    usage = '''%%prog {action}

Actions:
    %s''' % '\n    '.join(methods.keys())
    parser = optparse.OptionParser(usage)
    options, args = parser.parse_args()
    action = args[0] if args else ''
    if action in methods.keys():
        p = Parser()
        getattr(p, action)()
    else:
        parser.print_help()

