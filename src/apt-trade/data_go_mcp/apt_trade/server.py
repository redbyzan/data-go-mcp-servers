"""MCP server for Ministry of Land, Infrastructure and Transport Apartment Trade API."""

import os
import asyncio
from typing import Optional, Dict, Any
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
from .api_client import AptTradeAPIClient

# 환경변수 로드
load_dotenv()

# MCP 서버 인스턴스 생성
mcp = FastMCP("Apartment Trade")


def _parse_deal_amount(amount_str: Optional[str]) -> Optional[int]:
    """거래금액 문자열을 정수로 변환. '185,000' → 185000 (만원)."""
    if not amount_str:
        return None
    try:
        return int(amount_str.replace(",", "").replace(" ", ""))
    except (ValueError, TypeError):
        return None


@mcp.tool()
async def get_apt_trade(
    lawd_cd: str,
    deal_ymd: str,
    page_no: int = 1,
    num_of_rows: int = 100,
) -> Dict[str, Any]:
    """
    아파트 매매 실거래가를 조회합니다.

    Search for apartment sale transaction records from the Ministry of Land,
    Infrastructure and Transport real estate transaction data.

    Args:
        lawd_cd: 법정동코드 5자리 (예: 11680=강남구, 11110=종로구, 11650=서초구)
        deal_ymd: 거래연월 YYYYMM 형식 (예: 202603)
        page_no: 페이지 번호 (기본값: 1)
        num_of_rows: 한 페이지 결과 수 (기본값: 100, 최대: 1000)

    Returns:
        Dictionary containing:
        - items: List of apartment transaction records
        - page_no: Current page number
        - num_of_rows: Number of rows per page
        - total_count: Total number of results
    """
    async with AptTradeAPIClient() as client:
        try:
            result = await client.get_apt_trade(
                lawd_cd=lawd_cd,
                deal_ymd=deal_ymd,
                page_no=page_no,
                num_of_rows=num_of_rows,
            )

            if result["items"]:
                result["message"] = (
                    f"Found {result['total_count']} apartment sale transaction(s) "
                    f"for lawd_cd={lawd_cd}, deal_ymd={deal_ymd}"
                )
            else:
                result["message"] = (
                    f"No sale transactions found for lawd_cd={lawd_cd}, "
                    f"deal_ymd={deal_ymd}"
                )

            return result

        except Exception as e:
            return {
                "error": str(e),
                "items": [],
                "total_count": 0,
                "message": f"Error searching apartment trades: {str(e)}",
            }


@mcp.tool()
async def get_apt_rent(
    lawd_cd: str,
    deal_ymd: str,
    page_no: int = 1,
    num_of_rows: int = 100,
) -> Dict[str, Any]:
    """
    아파트 전월세 실거래가를 조회합니다.

    Search for apartment rent/lease transaction records from the Ministry of Land,
    Infrastructure and Transport real estate transaction data.

    Args:
        lawd_cd: 법정동코드 5자리 (예: 11680=강남구)
        deal_ymd: 거래연월 YYYYMM 형식 (예: 202603)
        page_no: 페이지 번호 (기본값: 1)
        num_of_rows: 한 페이지 결과 수 (기본값: 100, 최대: 1000)

    Returns:
        Dictionary containing:
        - items: List of apartment rent/lease transaction records
        - page_no: Current page number
        - num_of_rows: Number of rows per page
        - total_count: Total number of results
    """
    async with AptTradeAPIClient() as client:
        try:
            result = await client.get_apt_rent(
                lawd_cd=lawd_cd,
                deal_ymd=deal_ymd,
                page_no=page_no,
                num_of_rows=num_of_rows,
            )

            if result["items"]:
                result["message"] = (
                    f"Found {result['total_count']} apartment rent/lease transaction(s) "
                    f"for lawd_cd={lawd_cd}, deal_ymd={deal_ymd}"
                )
            else:
                result["message"] = (
                    f"No rent/lease transactions found for lawd_cd={lawd_cd}, "
                    f"deal_ymd={deal_ymd}"
                )

            return result

        except Exception as e:
            return {
                "error": str(e),
                "items": [],
                "total_count": 0,
                "message": f"Error searching apartment rents: {str(e)}",
            }


@mcp.tool()
async def estimate_apt_price(
    lawd_cd: str,
    apt_nm: str,
    excl_use_area: Optional[float] = None,
    recent_months: int = 6,
) -> Dict[str, Any]:
    """
    특정 아파트 단지의 최근 실거래가를 기반으로 시세를 추정합니다.

    Estimate apartment market price based on recent actual transaction data
    by collecting multi-month records and computing weighted statistics.

    Args:
        lawd_cd: 법정동코드 5자리 (예: 11680=강남구)
        apt_nm: 아파트 단지명 (예: "래미안파크스위트", "힐스테이트")
        excl_use_area: 전용면적(㎡) — 제공 시 ±2㎡ 범위로 필터링 (선택)
        recent_months: 조회할 최근 개월수 (기본값: 6, 최대: 12)

    Returns:
        Dictionary containing:
        - apt_nm: searched apartment name
        - lawd_cd: region code
        - sample_count: number of matched transactions
        - price_min: minimum trade amount in 만원
        - price_max: maximum trade amount in 만원
        - price_median: median trade amount in 만원
        - price_p25: 25th percentile in 만원
        - price_p75: 75th percentile in 만원
        - recent_trades: list of matched recent transactions
    """
    import datetime

    # recent_months cap
    recent_months = min(recent_months, 12)

    # 최근 N개월의 YYYYMM 리스트 생성
    now = datetime.datetime.now()
    months = []
    for i in range(recent_months):
        dt = now - datetime.timedelta(days=i * 30)
        months.append(dt.strftime("%Y%m"))

    months.reverse()  # 오래된 것부터 조회

    async with AptTradeAPIClient() as client:
        try:
            result = await client.get_apt_trade_multi_month(
                lawd_cd=lawd_cd,
                months=months,
            )

            # 단지명 필터링
            matched = []
            for item in result["items"]:
                name = item.get("apt_nm") or ""
                if apt_nm in name or name in apt_nm:
                    # 전용면적 필터링 (±2㎡)
                    if excl_use_area is not None:
                        try:
                            area = float(item.get("excl_use_ar") or 0)
                            if abs(area - excl_use_area) > 2.0:
                                continue
                        except (ValueError, TypeError):
                            continue
                    matched.append(item)

            if not matched:
                return {
                    "apt_nm": apt_nm,
                    "lawd_cd": lawd_cd,
                    "sample_count": 0,
                    "message": f"No transactions found for '{apt_nm}' in the last {recent_months} months",
                }

            # 거래금액 파싱 및 통계
            prices = []
            for item in matched:
                amt_str = item.get("deal_amount") or ""
                amt = _parse_deal_amount(amt_str)
                if amt and amt > 0:
                    prices.append(amt)

            if not prices:
                return {
                    "apt_nm": apt_nm,
                    "lawd_cd": lawd_cd,
                    "sample_count": len(matched),
                    "message": "Found transactions but could not parse prices",
                }

            prices.sort()
            n = len(prices)

            def percentile(p: float) -> int:
                idx = int(n * p / 100)
                return prices[min(idx, n - 1)]

            return {
                "apt_nm": apt_nm,
                "lawd_cd": lawd_cd,
                "sample_count": n,
                "price_min": prices[0],
                "price_max": prices[-1],
                "price_median": prices[n // 2],
                "price_p25": percentile(25),
                "price_p75": percentile(75),
                "price_as_of": months[-1],
                "recent_trades": matched[:20],  # 최대 20개까지만 반환
                "message": f"Estimated price for '{apt_nm}' based on {n} trades",
            }

        except Exception as e:
            return {
                "error": str(e),
                "apt_nm": apt_nm,
                "lawd_cd": lawd_cd,
                "sample_count": 0,
                "message": f"Error estimating price: {str(e)}",
            }


def main():
    """Run the MCP server."""
    import sys
    import logging

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    api_key = os.getenv("APT_TRADE_API_KEY") or os.getenv("API_KEY")
    if not api_key:
        logging.error(
            "APT_TRADE_API_KEY or API_KEY environment variable not found"
        )
        logging.error(
            "Please set API key from https://www.data.go.kr "
            "(아파트매매 실거래가 상세 자료)"
        )
        sys.exit(1)

    mcp.run()


if __name__ == "__main__":
    main()
