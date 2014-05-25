UK house prices since 1953 as monthly time-series. Data comes from the Nationwide.

Source: <http://www.nationwide.co.uk/hpi/historical.htm>

## Data

Data can be found in the `data/data.csv` file. See datapackage.json for
source info.

### Notes

From the source XLS file (notes tab):

> "The Nationwide house price methodology has developed over time and this
  needs to be considered when interpreting the long run series of house
  prices.  Maintenance in terms of updating weights for the mix-adjustment
  process is carried out at regular intervals.  Significant developments
  include:"
> * 1952 - 1959 Q4 Simple average of purchase price.
> * 1960 Q1 - 1973 Q4  - weighted average using floor area (thus allowing
>   for the influence of house size).
> * 1974 Q1 - 1982 Q4 - weighted averages using floor area, region and
>   property type.
> * 1983 Q1 -  Development of new house price methodology.  A statistical
>   'regression' technique was introduced under guidance of ‘Fleming and
>   Nellis’ (Loughborough University and Cranfield Institute of Technology).
>   This was introduced in 1989 but data was revised back to 1983 Q1.
> * 1993 - Information about neighbourhood classification (ACORN) used in
>   the model were significantly updated following Census 1991 publication -
>   regular updates since but typically for new postcodes.

## Preparation

Run:

    python data.py process

