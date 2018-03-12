from urllib.request import Request, urlopen
from urllib.parse import urlencode, quote_plus
from xml.etree.ElementTree import fromstring
from PublicValue import *
'''
운수업체명	companyName
운수업체 전화번호	companyTel
관할지역	districtCd
하행첫차	downFirstTime
하행막차	downLastTime
종점정류소번호	endMobileNo
종점정류소아이디	endStationId
종점정류소명	endStationName
최소(첨두)배차간격	peekAlloc
운행지역	regionName
노선 아이디	routeId
노선번호	routeName
노선유형	routeTypeCd
노선유형명	routeTypeName
기점정류소번호	startMobileNo
기점정류소아이디	startStationId
기점정류소명	startStationName
상행첫차	upFirstTime
상행막차	upLastTime
최대(비첨두)배차간격	nPeekAlloc
'''
		

tags=ROUTE_INFO_TAG
class RouteInfo:
	##조회할 노선 아이디를 받는다.
	def __init__(self, routeId):
		## xml url
		RouteInfo.url = ROUTE_INFO_URL
		## 인증키
		RouteInfo.key = KEY
		self.routeId = routeId
		self.xmlStr = "" ##xml문자열 담을 변수
		self.root = None ##최상위 항목 담을 변수
		self.isOnInternet = True ## 인터넷연결여부 
		
		##xml요청 주소에 넘길 인자 세팅
		queryParams = '?' + urlencode({quote_plus('serviceKey') : "KEYKEY", quote_plus('routeId') : self.routeId })
		queryParams = queryParams.replace("KEYKEY", RouteInfo.key)

		if routeId=='241483004' or routeId=='241483010' :
			self.url = "https://joambusapp.azurewebsites.net/appfile/rinfo_"
			queryParams = routeId + '.xml'
		
		##xml문서 받아와 str으로 xmlStr에 담는다.
		request = Request(self.url + queryParams)
		request.get_method = lambda: 'GET'
		try:
			self.xmlStr = binToUtf8(urlopen(request).read())
			self.root = fromstring(self.xmlStr)
		except:
			self.isOnInternet = False
		
	## 본 정보의 루트태그 msgBody의 유무 체크
	def isSuccess(self):
		if not self.isOnInternet:
			return False
		return self.root.find("msgBody")!=None
		
	## xml문서의 루트태그 리턴
	def getRoot(self):
		if not self.isOnInternet:
			return None
		return self.root
		
	## xml문서에서 본 정보리스트 리턴
	def getRouteInfo(self):
		if not self.isSuccess():
			return []
		return self.root.find("msgBody").find("busRouteInfoItem")

	def getInfoItems(self):
		aList = self.getRouteInfo()
		if aList == []:
			return []
		answer = []
		for i in range(len(tags)):
			answer.append(aList.findtext(tags[i]))
		return answer



		
##테스트코드
if __name__ == "__main__" :
	dd = RouteInfo("241483004")
	result = dd.getInfoItems()
	for i  in range(len(result)):
		print(tags[i], result[i])


