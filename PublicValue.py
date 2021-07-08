##경유정류소목록조회
ROUTE_STATION_URL = 'http://apis.data.go.kr/6410000/busrouteservice/getBusRouteStationList'
##노선정보
ROUTE_INFO_URL = 'http://apis.data.go.kr/6410000/busrouteservice/getBusRouteInfoItem'
##정류소 경유하는 노선목록 조회
STATION_STOP_BY_ROUTR_URL = 'http://apis.data.go.kr/6410000/busstationservice/getBusStationViaRouteList'
##기반정보
BASE_INFO_URL = 'http://apis.data.go.kr/6410000/baseinfoservice/getBaseInfoItem'

##경유정류소목록조회 항목태그
ROUTE_STATION_TAG = ("stationSeq", "centerYn", "districtCd", "mobileNo", "regionName", "stationId", "stationName", "x", "y", "turnYn")
##경유정류소목록조회DB 항목태그
ROUTE_STATION_DB_TAG = ("routeId", "stationSeq", "centerYn", "districtCd", "mobileNo", "regionName", "stationId", "stationName", "x", "y", "turnYn")
##노선정보 항목태그
ROUTE_INFO_TAG = ("companyId", "companyNm", "telNo", "districtCd", "downFirstTime", "downLastTime", "edStaNo", "edStaId", "edStaNm", "peekAlloc", "regionName", "routeId", "routeNm", "routeTp", "routeTypeName", "stStaNo", "stStaId", "stStaNm", "upFirstTime", "upLastTime", "nPeekAlloc")
##노선정보DB 항목태그
ROUTE_INFO_DB_TAG = ("companyId", "companyNm", "telNo", "districtCd", "downFirstTime", "downLastTime", "edStaNo", "edStaId", "edStaNm", "peekAlloc", "regionName", "routeId", "routeNm", "routeTp", "routeTypeName", "stStaNo", "stStaId", "stStaNm", "upFirstTime", "upLastTime", "nPeekAlloc", "middleStationName", "isOneWay")
##정류소 경유하는 노선목록 조회 항목태그
STATION_STOP_BY_ROUTR_TAG = ("districtCd", "regionName", "routeId", "routeNm", "routeTp", "routeTypeName")
##기반 정보 태그
BASE_INFO_TAG = ("areaDownloadUrl", "areaVersion", "routeDownloadUrl", "routeLineDownloadUrl", "routeLineVersion", "routeStationDownloadUrl", "routeStationVersion", "routeVersion", "stationDownloadUrl", "stationVersion", "vehicleDownloadUrl", "vehicleVersion")
##조암지역 노선 저장DB 태그
ROUTE_LIST_IN_JOAM_TAG = "routeId"

##필요한 기반 정보 태그
BASE_INFO_NEED_TAG = ("areaVersion", "routeDownloadUrl", "routeStationDownloadUrl", "stationDownloadUrl")

##경유정류소목록조회 항목태그 byte
ROUTE_STATION_DB_TAG_BYTE = (11, 4, 2, 3, 6, 7, 11, 40, 11, 11, 2)
##노선정보 항목태그 byte
ROUTE_INFO_TAG_BYTE = (11, 10, 3, 11, 40, 6, 11, 40, 6, 6, 6, 6, 6, 6, 6, 10, 30, 13, 30, 3)
##노선정보DB 항목태그 byte
ROUTE_INFO_DB_TAG_BYTE = (10, 30, 13, 3, 6, 6, 6, 11, 40, 6, 30, 11, 10, 3, 30, 6, 11, 40, 6, 6, 6, 40,2)
##정류소 경유하는 노선목록 조회 항목태그 byte
STATION_STOP_BY_ROUTR_TAG_BYTE = (3, 13, 11, 6, 3, 30)
##조암지역 노선 저장DB 태그 byte
ROUTE_LIST_IN_JOAM_TAG_BYTE = 11

##DLL
ROUTE_DLL = """CREATE TABLE `route` (
  `ROUTE_ID` int NOT NULL COMMENT '노선번호',
  `ROUTE_NM` varchar(10) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL COMMENT '노선이름',
  `ROUTE_TP` int NOT NULL COMMENT '노선종류',
  `ST_STA_ID` int NOT NULL COMMENT '기점정류장번호',
  `ST_STA_NM` varchar(80) CHARACTER SET utf8 COLLATE utf8_unicode_ci DEFAULT NULL,
  `ST_STA_NO` varchar(5) CHARACTER SET utf8 COLLATE utf8_unicode_ci DEFAULT NULL,
  `ED_STA_ID` int NOT NULL COMMENT '종점정류장번호',
  `ED_STA_NM` varchar(45) CHARACTER SET utf8 COLLATE utf8_unicode_ci DEFAULT NULL,
  `ED_STA_NO` varchar(5) CHARACTER SET utf8 COLLATE utf8_unicode_ci DEFAULT NULL,
  `UP_FIRST_TIME` time DEFAULT NULL COMMENT '기점첫차',
  `UP_LAST_TIME` time DEFAULT NULL COMMENT '기점막차',
  `DOWN_FIRST_TIME` time DEFAULT NULL COMMENT '종점첫차',
  `DOWN_LAST_TIME` time DEFAULT NULL COMMENT '종점막차',
  `PEEK_ALLOC` int DEFAULT NULL COMMENT '배차간격',
  `NPEEK_ALLOC` int DEFAULT NULL,
  `COMPANY_ID` int NOT NULL COMMENT '운수사번호',
  `COMPANY_NM` varchar(20) CHARACTER SET utf8 COLLATE utf8_unicode_ci DEFAULT NULL,
  `TEL_NO` varchar(20) CHARACTER SET utf8 COLLATE utf8_unicode_ci DEFAULT NULL,
  `REGION_NAME` varchar(50) CHARACTER SET utf8 COLLATE utf8_unicode_ci DEFAULT NULL,
  `DISTRICT_CD` int NOT NULL,
  `IS_ONEWAY` char(1) CHARACTER SET utf8 COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '단방향노선여부',
  `MID_STATION` varchar(20) CHARACTER SET utf8 COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '경유지정류장이름',
  PRIMARY KEY (`ROUTE_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8_unicode_ci COMMENT='노선'"""
ROUTE_STATION_DLL = """CREATE TABLE `routestation` (
  `ROUTE_ID` int DEFAULT NULL,
  `STATION_ID` int DEFAULT NULL,
  `UPDOWN` text CHARACTER SET utf8 COLLATE utf8_unicode_ci,
  `STA_ORDER` int DEFAULT NULL,
  `ROUTE_NM` text CHARACTER SET utf8 COLLATE utf8_unicode_ci,
  `STATION_NM` text CHARACTER SET utf8 COLLATE utf8_unicode_ci
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8_unicode_ci"""
STATION_DLL="""CREATE TABLE `station` (
  `STATION_ID` int NOT NULL,
  `STATION_NM` text CHARACTER SET utf8 COLLATE utf8_unicode_ci,
  `CENTER_ID` int DEFAULT NULL,
  `CENTER_YN` text CHARACTER SET utf8 COLLATE utf8_unicode_ci,
  `X` double DEFAULT NULL,
  `Y` double DEFAULT NULL,
  `REGION_NAME` text CHARACTER SET utf8 COLLATE utf8_unicode_ci,
  `MOBILE_NO` int DEFAULT NULL,
  `DISTRICT_CD` int DEFAULT NULL,
  PRIMARY KEY (`STATION_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8_unicode_ci"""

dDllSql = {'route': ROUTE_DLL, 'routeStation': ROUTE_STATION_DLL, 'station': STATION_DLL}


PRIVATE_KEY = "zRuxSFejoJKPbOZdUuxyIUWJF7R56lxvA5LbRwxQWj8IVxCG2F6aYImQvUJIdzvjM3EDvvYQfrQyIirNaYWkqA%3D%3D"
PUBLIC_KEY = "1234567890"
KEY = PRIVATE_KEY

######################## 우정읍사무소, 어은삼거리, 어은4리 , 장안여중,      조암8리, 해창1리 ,석포삼거리,석포5리마을회관,      석포1리, 마파지,          매향3리,     이화리, 장안6리
SELECTIVE_STATION_ID = ("233001070","233000402","233000931","233000992","233000372","233000927","233000397","233001381","233001516","233002863", "233001779", "233001053", "233000991")

## binary data to utf-8
def binToUtf8(data):
	# 바이너리 데이터를 utf-16으로 디코딩한다
	# 수직 탭을 삭제한다
	return data.decode("utf-8").replace(u"\u000B", u"")
