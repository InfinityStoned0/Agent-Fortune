# Agent-Fortune
This API fetches the trading information of a crypto coin from dexscreener's free API and outputs it's RSI and price movement information.
The contract address of the token(s) should be put into the "predefined_tokens.txt" file.

# Usage
Install required dependencies

`pip install -r requirements.txt`

Run the script

`python agent_fortune.py`

**NOTE**: If you're working on an SoC (Raspberry Pi models and as such), you need to run the above commands in a virtual environment by following steps

`python -m venv <custom_venv_name>`

`. <custom_venv_name>/bin/activate`

`pip install -r requirements.txt`

`python agent_fortune.py`


**OUTPUT**

![image](https://github.com/user-attachments/assets/4490e235-b177-4190-9a5e-8ed613fadb91)

# Future Scope

The following technical indicators are being 
1. MACD - Moving Average Convergence Divergence
2. 50 DMA - 50 Day Moving Average
3. 200 DMA - 200 Day Moving Average
4. OBV - On-Balance Volume
5. ADI - Average Directional Index

# FAQS

1. Why use data from Dexscreener?
   Dexscreener has some useful API(s) for free. The rate limit is 60 per minute but it would be sufficient to collect all the data without overloading the server.

2. Will there be more functionalities added to this repository?
   Yes! There are plans to extend this repo with additional features. More information on this to be released soon.
