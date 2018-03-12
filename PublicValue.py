##경유정류소목록조회
ROUTE_STATION_URL = 'http://openapi.gbis.go.kr/ws/rest/busrouteservice/station'
##노선정보
ROUTE_INFO_URL = 'http://openapi.gbis.go.kr/ws/rest/busrouteservice/info'
##정류소 경유하는 노선목록 조회
STATION_STOP_BY_ROUTR_URL = 'http://openapi.gbis.go.kr/ws/rest/busstationservice/route'

##경유정류소목록조회 항목태그
ROUTE_STATION_TAG = ("stationSeq", "centerYn", "districtCd", "mobileNo", "regionName", "stationId", "stationName", "x", "y", "turnYn")
##경유정류소목록조회DB 항목태그
ROUTE_STATION_DB_TAG = ("routeId", "stationSeq", "centerYn", "districtCd", "mobileNo", "regionName", "stationId", "stationName", "x", "y", "turnYn")
##노선정보 항목태그
ROUTE_INFO_TAG = ("companyName", "companyTel", "districtCd", "downFirstTime", "downLastTime", "endMobileNo", "endStationId", "endStationName", "peekAlloc", "regionName", "routeId", "routeName", "routeTypeCd", "routeTypeName", "startMobileNo", "startStationId", "startStationName", "upFirstTime", "upLastTime", "nPeekAlloc")
##노선정보DB 항목태그
ROUTE_INFO_DB_TAG = ("companyName", "companyTel", "districtCd", "downFirstTime", "downLastTime", "endMobileNo", "endStationId", "endStationName", "peekAlloc", "regionName", "routeId", "routeName", "routeTypeCd", "routeTypeName", "startMobileNo", "startStationId", "startStationName", "upFirstTime", "upLastTime", "nPeekAlloc", "middleSationName")
##정류소 경유하는 노선목록 조회 항목태그
STATION_STOP_BY_ROUTR_TAG = ("districtCd", "regionName", "routeId", "routeName", "routeTypeCd", "routeTypeName")
##조암지역 노선 저장DB 태그
ROUTE_LIST_IN_JOAM_TAG = "routeId"


##경유정류소목록조회 항목태그 byte
ROUTE_STATION_DB_TAG_BYTE = (11, 4, 2, 3, 6, 7, 11, 40, 11, 11, 2)
##노선정보 항목태그 byte
ROUTE_INFO_TAG_BYTE = (30, 13, 3, 6, 6, 6, 11, 40, 6, 30, 11, 10, 3, 30, 6, 11, 40, 6, 6, 6)
##노선정보DB 항목태그 byte
ROUTE_INFO_DB_TAG_BYTE = (30, 13, 3, 6, 6, 6, 11, 40, 6, 30, 11, 10, 3, 30, 6, 11, 40, 6, 6, 6, 40)
##정류소 경유하는 노선목록 조회 항목태그 byte
STATION_STOP_BY_ROUTR_TAG_BYTE = (3, 13, 11, 6, 3, 30)
##조암지역 노선 저장DB 태그 byte
ROUTE_LIST_IN_JOAM_TAG_BYTE = 11


PRIVATE_KEY = "zRuxSFejoJKPbOZdUuxyIUWJF7R56lxvA5LbRwxQWj8IVxCG2F6aYImQvUJIdzvjM3EDvvYQfrQyIirNaYWkqA%3D%3D"
PUBLIC_KEY = "1234567890"
KEY = PUBLIC_KEY

######################## 우정읍사무소, 어은삼거리, 어은4리 , 장안여중,      조암8리, 해창1리 ,석포삼거리,석포5리마을회관,      석포1리, 마파지,          매향3리,     이화리, 장안6리
SELECTIVE_STATION_ID = ("233001070","233000402","233000931","233000992","233000372","233000927","233000397","233001381","233001516","233002863", "233001779", "233001053", "233000991")

## binary data to utf-8
def binToUtf8(data):
	# 바이너리 데이터를 utf-16으로 디코딩한다
	# 수직 탭을 삭제한다
	return data.decode("utf-8").replace(u"\u000B", u"")
