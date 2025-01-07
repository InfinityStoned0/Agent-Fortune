import os, json, csv, time, requests
import pandas as pd
from tabulate import tabulate
from datetime import datetime
from collections import deque

class TokenAnalyzer:
    def __init__(self, token_list_file="predefined_tokens.txt", analysis_file="tokens_analyzed.json"):
        self.token_list_file = token_list_file
        self.analysis_file = analysis_file
        self.price_array = deque(maxlen=20)

    def log(self, message):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_message = f"{timestamp} - {message}"
        print(log_message)

    def calculate_rsi(self, prices, period=14):
        if len(prices) < period:
            return None  # Not enough data to calculate RSI

        gains = []
        losses = []

        for i in range(1, len(prices)):
            change = prices[i] - prices[i - 1]
            if change > 0:
                gains.append(change)
                losses.append(0)
            elif change < 0:
                gains.append(0)
                losses.append(abs(change))
            else:
                gains.append(0)
                losses.append(0)

        avg_gain = sum(gains[-period:]) / period
        avg_loss = sum(losses[-period:]) / period

        if avg_loss == 0:
            return 100  # If no losses, RSI is 100

        rs = avg_gain / avg_loss
        return float(100 - (100 / (1 + rs)))

    def analyze_data(self):
        if os.path.isfile(self.analysis_file):
            os.remove(self.analysis_file)

        analysis_results = []

        with open(self.token_list_file, "r") as file:
            tokens = [line.strip() for line in file.readlines()]

        for token in tokens:
            url = f'https://api.dexscreener.com/latest/dex/tokens/{token}'
            response = requests.get(url)

            if response.status_code != 200:
                self.log(f"Failed to fetch data for token: {token}")
                continue

            token_metadata = response.json().get('pairs', [{}])[0]
            symbol = token_metadata.get('baseToken', {}).get('symbol', '')
            price_usd = float(token_metadata.get('priceUsd', 0))
            buys_5m = int(token_metadata.get('txns', {}).get('m5', {}).get('buys', 0))
            buys_1h = int(token_metadata.get('txns', {}).get('h1', {}).get('buys', 0))
            sales_5m = int(token_metadata.get('txns', {}).get('m5', {}).get('sells', 0))
            sales_1h = int(token_metadata.get('txns', {}).get('h1', {}).get('sells', 0))
            volume_5m = int(token_metadata.get('volume', {}).get('m5', 0))
            volume_1h = int(token_metadata.get('volume', {}).get('h1', 0))
            price_change_5m = float(token_metadata.get('priceChange', {}).get('m5', 0))
            price_change_1h = float(token_metadata.get('priceChange', {}).get('h1', 0))
            self.price_array.append(price_usd)

            rsi = self.calculate_rsi(self.price_array)
            if rsi is not None:
                self.log(f"RSI for {symbol}: {rsi:.2f}")

            analysis_results.append({
                "Symbol": symbol,
                "Price": price_usd,
                "RSI": rsi,
                "buys_5m": buys_5m,
                "buys_1h": buys_1h,
                "sales_5m": sales_5m,
                "sales_1h": sales_1h,
                "vol_5m": volume_5m,
                "vol_1h": volume_1h,
                "priceChg_5m": price_change_5m,
                "priceChg_1h": price_change_1h
            })

        if analysis_results:
            with open(self.analysis_file, 'w') as f:
                json.dump(analysis_results, f, indent=4)
            self.log(f"Data analysis complete. Results saved to {self.analysis_file}.")
        else:
            self.log("No tokens detected with the set criteria.")

    def save_to_csv_and_tabulate(self):
        if os.path.isfile(self.analysis_file):
            with open(self.analysis_file, 'r') as f:
                analyzed_data = json.load(f)

            df = pd.DataFrame(analyzed_data)
            output_file = "output.csv"
            df.to_csv(output_file, index=False)

            with open(output_file, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.reader(file)
                headers = next(reader)
                data = list(reader)

            os.remove(output_file)

            tabulated_tokens = "tabulated_tokens.txt"
            with open(tabulated_tokens, 'w', encoding='utf-8') as f:
                f.write(tabulate(data, headers=headers, tablefmt="pretty"))
                f.write("\n")

            self.log(f"Tabulated data saved to {tabulated_tokens}")

    def run(self):
        while True:
            self.analyze_data()
            self.save_to_csv_and_tabulate()
            self.log("Script run complete.")
            time.sleep(5)  # Sleep for 5 seconds

if __name__ == "__main__":
    analyzer = TokenAnalyzer()
    analyzer.run()

