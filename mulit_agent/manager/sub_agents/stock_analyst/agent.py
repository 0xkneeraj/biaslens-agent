from google.adk.agents import Agent
from datetime import datetime
import yfinance as yf

def get_stock_price(ticker:str) -> dict:
    # Retrieves current stock price and saves to session state
    print(f"--- Tool: get stock price called for {ticker} ---")

    try:
        # fetch stock data
        stock = yf.Ticker(ticker)
        current_price = stock.info.get('currentPrice')

        if current_price is None:
            return {
                "status": "error",
                "error_message": f"Could not fetch stock price for {ticker}."
            }
        # get current time
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        return {
                "status": "success",
                "ticker": ticker,
                "current_price": current_price,
                "fetched_at": current_time
            }
    except Exception as e:
            return {
                "status": "error",
                "error_message": str(e)
            }

# create the agent
stock_analyst = Agent(
    name="stock_analyst",
    description="A stock analyst agent that provides current stock prices.",
    instruction="""When asked to look up a stock price:
1. Use the get_stock_price tool to fetch the current stock price for the requested stock(s).
2. Format the response to show each stock's current price and the time it was fetched.
3. If a stock price couldn't be fetched, mention that the stock price is not available at the moment.

Example response format:
"Here are the current prices for your stocks:
- AAPL: $150.00 (fetched at 2023-10-01 12:00:00)
- GOOGL: $2800.00 (fetched at 2023-10-01 12:00:00)
- TSLA: $700.00 (fetched at 2023-10-01 12:00:00)
"

if the user asks about anything else,
you should delegate the task to the manager agent.
""",
    tools=[get_stock_price],
)