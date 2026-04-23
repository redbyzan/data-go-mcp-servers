"""API client for Ministry of Land, Infrastructure and Transport Apartment Trade API."""

import os
from typing import Any, Dict, Optional
from urllib.parse import quote

import httpx
from dotenv import load_dotenv

from .models import AptTradeItem, AptRentItem

load_dotenv()


class AptTradeAPIClient:
    """국토교통부 아파트 실거래가 API 클라이언트"""

    # 공공데이터포털 엔드포인트
    TRADE_URL = "https://apis.data.go.kr/1613000/RTMSDataSvcAptTrade/getRTMSDataSvcAptTrade"
    RENT_URL = "https://apis.data.go.kr/1613000/RTMSDataSvcAptRent/getRTMSDataSvcAptRent"

    def __init__(self):
        self.api_key = os.getenv("APT_TRADE_API_KEY") or os.getenv("API_KEY")

        if not self.api_key:
            raise ValueError(
                "APT_TRADE_API_KEY or API_KEY environment variable is required. "
                "Get your API key from https://www.data.go.kr"
            )

        # 공공데이터포털은 decode 키를 URL 인코딩 없이 전달해야 함
        self.client = httpx.AsyncClient(timeout=30.0)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.aclose()

    def _parse_items(self, body: Dict) -> list:
        """API 응답 body에서 items 배열을 파싱.

        공공데이터포털 API는 결과가 1개일 때 배열이 아닌 단일 객체로 반환하므로
        이를 항상 리스트로 정규화합니다.
        """
        if not body or "items" not in body or not body["items"]:
            return []

        item_data = body["items"].get("item", [])
        if not isinstance(item_data, list):
            item_data = [item_data]

        return item_data

    async def _make_request(self, url: str, params: Dict[str, Any]) -> Dict:
        """API 요청 실행"""
        # serviceKey는 URL 인코딩하면 안 됨 (공공데이터포털 특이사항)
        params["_type"] = "json"
        params["serviceKey"] = self.api_key

        try:
            response = await self.client.get(url, params=params)
            response.raise_for_status()

            data = response.json()

            if "response" in data:
                resp = data["response"]
                header = resp.get("header", {})
                if header.get("resultCode") != "00":
                    raise Exception(
                        f"API Error: {header.get('resultMsg', 'Unknown error')} "
                        f"(code: {header.get('resultCode')})"
                    )
                return resp.get("body", {})

            return data

        except httpx.HTTPStatusError as e:
            raise Exception(f"HTTP Error {e.response.status_code}: {e.response.text}")
        except Exception as e:
            if "API Error" in str(e):
                raise
            raise Exception(f"Request failed: {str(e)}")

    async def get_apt_trade(
        self,
        lawd_cd: str,
        deal_ymd: str,
        page_no: int = 1,
        num_of_rows: int = 1000,
    ) -> Dict[str, Any]:
        """아파트 매매 실거래가 조회

        Args:
            lawd_cd: 법정동코드 5자리 (예: 11680 = 강남구)
            deal_ymd: 거래연월 YYYYMM (예: 202603)
            page_no: 페이지 번호
            num_of_rows: 페이지당 건수 (최대 1000)
        """
        params = {
            "LAWD_CD": lawd_cd,
            "DEAL_YMD": deal_ymd,
            "pageNo": page_no,
            "numOfRows": num_of_rows,
        }

        body = await self._make_request(self.TRADE_URL, params)

        items = []
        for raw in self._parse_items(body):
            try:
                items.append(AptTradeItem(**raw).model_dump())
            except Exception:
                items.append(raw)

        return {
            "items": items,
            "page_no": body.get("pageNo", page_no),
            "num_of_rows": body.get("numOfRows", num_of_rows),
            "total_count": body.get("totalCount", 0),
        }

    async def get_apt_rent(
        self,
        lawd_cd: str,
        deal_ymd: str,
        page_no: int = 1,
        num_of_rows: int = 1000,
    ) -> Dict[str, Any]:
        """아파트 전월세 실거래가 조회

        Args:
            lawd_cd: 법정동코드 5자리
            deal_ymd: 거래연월 YYYYMM
            page_no: 페이지 번호
            num_of_rows: 페이지당 건수 (최대 1000)
        """
        params = {
            "LAWD_CD": lawd_cd,
            "DEAL_YMD": deal_ymd,
            "pageNo": page_no,
            "numOfRows": num_of_rows,
        }

        body = await self._make_request(self.RENT_URL, params)

        items = []
        for raw in self._parse_items(body):
            try:
                items.append(AptRentItem(**raw).model_dump())
            except Exception:
                items.append(raw)

        return {
            "items": items,
            "page_no": body.get("pageNo", page_no),
            "num_of_rows": body.get("numOfRows", num_of_rows),
            "total_count": body.get("totalCount", 0),
        }

    async def get_apt_trade_multi_month(
        self,
        lawd_cd: str,
        months: list[str],
        page_no: int = 1,
        num_of_rows: int = 1000,
    ) -> Dict[str, Any]:
        """여러 월의 아파트 매매 실거래가를 통합 조회.

        시세 추정을 위해 최근 N개월치 데이터를 한번에 가져올 때 사용합니다.

        Args:
            lawd_cd: 법정동코드 5자리
            months: 거래연월 리스트 (예: ["202601", "202602", "202603"])
            page_no: 페이지 번호
            num_of_rows: 페이지당 건수
        """
        all_items = []
        total_count = 0

        for ymd in months:
            result = await self.get_apt_trade(
                lawd_cd=lawd_cd,
                deal_ymd=ymd,
                page_no=page_no,
                num_of_rows=num_of_rows,
            )
            all_items.extend(result["items"])
            total_count += result["total_count"]

        return {
            "items": all_items,
            "total_count": total_count,
            "months_queried": months,
        }
