"""Data models for Apartment Trade API (아파트 매매/전월세 실거래가)."""

from typing import Optional, Union
from pydantic import BaseModel, ConfigDict, Field


class AptTradeItem(BaseModel):
    """아파트 매매 실거래가 아이템"""
    apt_nm: Optional[str] = Field(None, alias="aptNm", description="아파트명")
    deal_amount: Optional[str] = Field(None, alias="dealAmount", description="거래금액(만원, 콤마 포함)")
    excl_use_ar: Optional[Union[str, float]] = Field(None, alias="excluUseAr", description="전용면적(㎡)")
    deal_year: Optional[Union[str, int]] = Field(None, alias="dealYear", description="거래연도")
    deal_month: Optional[Union[str, int]] = Field(None, alias="dealMonth", description="거래월")
    deal_day: Optional[Union[str, int]] = Field(None, alias="dealDay", description="거래일")
    floor: Optional[Union[str, int]] = Field(None, alias="floor", description="층")
    umd_nm: Optional[str] = Field(None, alias="umdNm", description="법정동명")
    sgg_cd: Optional[Union[str, int]] = Field(None, alias="sggCd", description="법정동코드 5자리")
    build_year: Optional[Union[str, int]] = Field(None, alias="buildYear", description="건축연도")
    dealing_gbn: Optional[str] = Field(None, alias="dealingGbn", description="거래유형")
    sler_gbn: Optional[str] = Field(None, alias="slerGbn", description="매도자")
    buyer_gbn: Optional[str] = Field(None, alias="buyerGbn", description="매수자")
    rgst_date: Optional[str] = Field(None, alias="rgstDate", description="등기일자")
    estate_agent_sgg_nm: Optional[str] = Field(None, alias="estateAgentSggNm", description="중개업소 시군구명")

    model_config = ConfigDict(populate_by_name=True)


class AptRentItem(BaseModel):
    """아파트 전월세 실거래가 아이템"""
    apt_nm: Optional[str] = Field(None, alias="aptNm", description="아파트명")
    deposit: Optional[str] = Field(None, alias="deposit", description="보증금(만원, 콤마 포함)")
    monthly_rent: Optional[str] = Field(None, alias="monthlyRent", description="월세금(만원, 콤마 포함)")
    excl_use_ar: Optional[Union[str, float]] = Field(None, alias="excluUseAr", description="전용면적(㎡)")
    deal_year: Optional[Union[str, int]] = Field(None, alias="dealYear", description="계약연도")
    deal_month: Optional[Union[str, int]] = Field(None, alias="dealMonth", description="계약월")
    deal_day: Optional[Union[str, int]] = Field(None, alias="dealDay", description="계약일")
    floor: Optional[Union[str, int]] = Field(None, alias="floor", description="층")
    umd_nm: Optional[str] = Field(None, alias="umdNm", description="법정동명")
    sgg_cd: Optional[Union[str, int]] = Field(None, alias="sggCd", description="법정동코드 5자리")
    build_year: Optional[Union[str, int]] = Field(None, alias="buildYear", description="건축연도")
    contract_term: Optional[str] = Field(None, alias="contractTerm", description="계약구간")
    contract_type: Optional[str] = Field(None, alias="contractType", description="계약구분(전세/월세)")
    rgst_date: Optional[str] = Field(None, alias="rgstDate", description="등기일자")

    model_config = ConfigDict(populate_by_name=True)
