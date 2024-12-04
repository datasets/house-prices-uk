import logging
import urllib.request
import pandas as pd
import argparse

logger = logging.getLogger(__name__)

nationwide_archive_fp = 'archive/nationwide.xls'
nationwide_data_fp = 'data/data.csv'

class Parser:

    def download(self):
        """Download the data to the archive (cache)"""
        nationwide = 'https://www.nationwidehousepriceindex.co.uk/download/uk-house-prices-since-1952'
        urllib.request.urlretrieve(nationwide, nationwide_archive_fp)
        logger.info('Data downloaded to: %s', nationwide_archive_fp)

    def process(self):
        """Extract data from archive to output data file"""
        logger.info('Extracting data from XLS')

        df = pd.read_excel(nationwide_archive_fp, sheet_name=0)

        def fix_date(indate):
            """Convert quarter-year format to a date."""
            q, year = indate.split()
            return f"{int(year)}-{(int(q[1]) - 1) * 3 + 2:02d}-01"

        def fixup(series, decplaces=0):
            """Convert values to desired decimal places or integers."""
            return [round(float(x), decplaces) if isinstance(x, (int, float)) else 0 for x in series]

        # Data extraction - assuming specific columns exist; adjust indices if necessary
        data = {
            'Date': [fix_date(x) for x in df.iloc[6:, 0]],
            'Price (All)': fixup(df.iloc[6:, 2]),
            'Change (All)': fixup(df.iloc[6:, 3], 1),
            'Price (New)': fixup(df.iloc[6:, 5]),
            'Change (New)': fixup(df.iloc[6:, 6], 1),
            'Price (Modern)': fixup(df.iloc[6:, 8]),
            'Change (Modern)': fixup(df.iloc[6:, 9], 1),
            'Price (Older)': fixup(df.iloc[6:, 11]),
            'Change (Older)': fixup(df.iloc[6:, 12], 1)
        }

        # Create DataFrame and write to CSV
        output_df = pd.DataFrame(data)
        output_df.to_csv(nationwide_data_fp, index=False)
        logger.info('Data successfully extracted to: %s', nationwide_data_fp)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    parser = argparse.ArgumentParser(description="Process UK House Price data")
    parser.add_argument("action", choices=['download', 'process'], help="Action to perform")
    args = parser.parse_args()

    p = Parser()
    action = args.action
    if hasattr(p, action):
        getattr(p, action)()
    else:
        parser.print_help()