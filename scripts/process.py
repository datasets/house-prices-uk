"""
UK House Price data

extracted links from html source of 
http://www.nationwide.co.uk/hpi/historical.htm
"""
import logging
import urllib
import datautil.tabular as T
import optparse
import inspect

logger = logging.getLogger(__name__)


class Parser(object):
    nationwide_archive_fp = 'archive/nationwide.xls'
    nationwide_data_fp = 'data/data.csv'

    def download(self):
        '''Download the data to the archive (cache)'''
        nationwide = 'http://www.nationwide.co.uk/~/media/MainSite/documents/about/house-price-index/downloads/uk-house-price-since-1952.xls'
        urllib.urlretrieve(nationwide, self.nationwide_archive_fp)

    def process(self):
        '''Extract data from archive to output data file'''
        logger.info('Extracting data from Xls')

        # the remote site has ssl problem
        # IOError: [Errno socket error] [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed (_ssl.c:590)
        # self.download()
        # fp = self.nationwide_archive_fp

        # so I downloaded source file manually (jan2018)
        fp = 'archive/uk-house-price-since-1952.xls'

        reader = T.XlsReader(fp)
        # notes are on 2nd page but ignore for time being
        tdata = reader.read()
        data = tdata.data
        out = T.TabularData()
        out.header = [ 'Date', 'Price (All)', 'Change (All)', 'Price (New)', 'Change (New)', 'Price (Modern)', 'Change (Modern)', 'Price (Older)', 'Change (Older)' ]
        data = data[6:]
        data = zip(*data)

        def fix_date(indate): # e.g Q1 1952
            q,year = indate.split()
            return '%s-%02d-01' % (int(year), (int(q[1])-1) * 3 + 2)

        def fixup(series, decplaces=0):
            out = [round((x if type(x) is float else 0), decplaces) for x in series]

            if decplaces == 0:
                out = [int(x) for x in out]
            return out

        data = [
            [fix_date(x) for x in data[0]],
            fixup(data[2]),
            fixup(data[3], 1),
            fixup(data[5]),
            fixup(data[6], 1),
            fixup(data[8]),
            fixup(data[9], 1),
            fixup(data[11]),
            fixup(data[12], 1)
            ]
        out.data = list(zip(*data))
        writer = T.CsvWriter()
        writer.write(out, open(self.nationwide_data_fp, 'w'))
        logger.info('Data successfully extracted to: %s' % self.nationwide_data_fp)

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

