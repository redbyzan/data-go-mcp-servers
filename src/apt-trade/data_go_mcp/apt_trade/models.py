"""Data models for Apartment Trade API (아파트 매매/전월세 실거래가)."""

from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


class AptTradeItem(BaseModel):
    """아파트 매매 실거래가 아이템"""
    apt_nm: Optional[str] = Field(None, alias="아파트", description="아파트명")
    deal_amount: Optional[str] = Field(None, alias="거래금액", description="거래금액(만원, 콤마 포함)")
    excl_use_area: Optional[str] = Field(None, alias="전용면적", description="전용면적(㎡)")
    deal_year: Optional[str] = Field(None, alias="년", description="거래연도")
    deal_month: Optional[str] = Field(None, alias="월", description="거래월")
    deal_day: Optional[str] = Field(None, alias="일", description="거래일")
    floor: Optional[str] = Field(None, alias="층", description="층")
    bdong_nm: Optional[str] = Field(None, alias="법정동", description="법정동명")
    regional_cd: Optional[str] = Field(None, alias="지역코드", description="법정동코드 5자리")
    road_nm: Optional[str] = Field(None, alias="도로명", description="도로명주소")
    road_nm_bonbun: Optional[str] = Field(None, alias="도로명건물본번호코드", description="도로명 건물본번호")
    road_nm_bubun: Optional[str] = Field(None, alias="도로명건물부번호코드", description="도로명 건물부번호")
    build_year: Optional[str] = Field(None, alias="건축년도", description="건축연도")
    dealing_gbn: Optional[str] = Field(None, alias="거래유형", description="거래유형")
    sler_gbn: Optional[str] = Field(None, alias="매도자", description="매도자")
    buyr_gbn: Optional[str] = Field(None, alias="매수자", description="매수자")
    rgst_date: Optional[str] = Field(None, alias="등기일자", description="등기일자")

    model_config = ConfigDict(populate_by_name=True)


class AptRentItem(BaseModel):
    """아파트 전월세 실거래가 아이템"""
    apt_nm: Optional[str] = Field(None, alias="아파트", description="아파트명")
    deposit: Optional[str] = Field(None, alias="보증금(만원)", description="보증금(만원, 콤마 포함)")
    monthly_rent: Optional[str] = Field(None, alias="월세(만원)", description="월세금(만원, 콤마 포함)")
    excl_use_area: Optional[str] = Field(None, alias="전용면적", description="전용면적(㎡)")
    deal_year: Optional[str] = Field(None, alias="년", description="계약연도")
    deal_month: Optional[str] = Field(None, alias="월", description="계약월")
    deal_day: Optional[str] = Field(None, alias="일", description="계약일")
    floor: Optional[str] = Field(None, alias="층", description="층")
    bdong_nm: Optional[str] = Field(None, alias="법정동", description="법정동명")
    regional_cd: Optional[str] = Field(None, alias="지역코드", description="법정동코드 5자리")
    build_year: Optional[str] = Field(None, alias="건축년도", description="건축연도")
    contract_term: Optional[str] = Field(None, alias="계약구간", description="계약구간")
    contract_type: Optional[str] = Field(None, alias="계약구분", description="계약구분(전세/월세)")
    rgst_date: Optional[str] = Field(None, alias="등기일자", description="등기일자")

    model_config = ConfigDict(populate_by_name=True)
