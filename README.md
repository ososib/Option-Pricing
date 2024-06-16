# Option Pricing Program

This program is designed to price options using provided market data and trade information. It calculates the present value, equity delta, and equity vega for each trade entry.

## Description

This program is designed to price options using provided market data and trade information. It calculates the present value, equity delta, and equity vega for each trade entry.

## Requirements

- Python 3.x
- Pandas library

Ensure Python and Pandas are installed on your system. If Pandas is not installed, you can install it using pip:

```bash
pip install pandas
```


## Input Files

The program requires two CSV input files and produces one CSV output file:

1. Trade CSV File ("trade_data.csv") - Contains the trade details such as trade ID, quantity, underlying, expiry, payment time, strike, call/put type, and currency.
2. Market Data CSV File ("market_data.csv") - Contains the market data such as asset class, underlying, spot price, and volatility.

The names of these files need to be passed as arguments to the program. Or simply provided in "main" block if running on IDE.

## Output File

The output CSV file contains the following columns:

    Trade ID - Identifier for each trade row.
    PV (Present Value in USD) - The calculated present value of the option.
    Equity Delta - Sensitivity of the PV to a 1% relative increase in the underlying spot price.
    Equity Vega - Sensitivity of the PV to a 1% increase in the underlying spot price implied volatility.


## How to Run the Program

To run the program, use the following command in the terminal:

```bash
python option_pricer.py <trade_csv_file> <market_data_csv_file> <result_csv_file>
```

Replace <trade_csv_file>, <market_data_csv_file>, and <result_csv_file> with the paths to your input trade data file, market data file, and the desired output file name for the results, respectively.

### Example

```bash
python option_pricer.py trades.csv market_data.csv results.csv
```

This command will read the trades from trades.csv and market data from market_data.csv, then output the results to results.csv.

## Assumptions


For detailed assumptions and pricing models, refer to the theoretical framework discussed in the pdf files (not included, can be provided).

