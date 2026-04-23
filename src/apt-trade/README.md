# data-go-mcp.apt-trade

MCP server for Korea Ministry of Land, Infrastructure and Transport (국토교통부) apartment transaction price API from [data.go.kr](https://www.data.go.kr).

## API Source

- **아파트매매 실거래가 상세 자료**: Apartment sale transaction records
- **아파트전월세 실거래가 상세 자료**: Apartment rent/lease transaction records

API provided by Ministry of Land, Infrastructure and Transport (국토교통부) via 공공데이터포털.

## Features

- **get_apt_trade**: Query apartment sale transaction records by region and month
- **get_apt_rent**: Query apartment rent/lease transaction records by region and month
- **estimate_apt_price**: Estimate apartment market price based on recent transaction data with filtering and percentile statistics

## Setup

### 1. Get API Key

1. Register at [공공데이터포털](https://data.go.kr)
2. Search for "아파트매매 실거래가 상세 자료" and "아파트전월세 실거래가 상세 자료"
3. Apply for each service (auto-approved, free)
4. Copy the **Decoding Key** (not Encoding Key)

### 2. Configure

```bash
export APT_TRADE_API_KEY='your-decoding-key-here'
```

Or create a `.env` file:
```
APT_TRADE_API_KEY=your-decoding-key-here
```

## Usage

### As MCP Server

```bash
# Install dependencies
uv sync

# Run the server
uv run python -m data_go_mcp.apt_trade.server
```

### As Python Package

```python
import asyncio
from data_go_mcp.apt_trade import AptTradeAPIClient

async def main():
    async with AptTradeAPIClient() as client:
        # Get sale transactions for Gangnam-gu, March 2026
        result = await client.get_apt_trade(
            lawd_cd="11680",  # 강남구
            deal_ymd="202603"
        )
        for item in result["items"]:
            print(f"{item['apt_nm']} - {item['deal_amount']}만원")

asyncio.run(main())
```

## Common Law Codes (법정동코드)

| Region | Code |
|--------|------|
| 종로구 | 11110 |
| 용산구 | 11170 |
| 마포구 | 11440 |
| 서초구 | 11650 |
| 강남구 | 11680 |
| 송파구 | 11710 |
| 분당구 | 41135 |

Full list: https://www.code.go.kr/stdcode/regCodeL.do

## Development

```bash
# Install dev dependencies
uv sync --dev

# Run tests
uv run pytest tests/ -v

# Run with coverage
uv run pytest tests/ -v --cov=data_go_mcp.apt_trade
```

## License

Apache-2.0
