from urllib.request import Request, urlopen
from urllib.parse import urlencode, quote_plus
from xml.etree.ElementTree import fromstring
from PublicValue import *
'''
중앙차로여부	centerYn
관할지역	districtCd
정류소 번호	mobileNo
지역 명	regionName
정류소아이디	stationId
정류소명	stationName
X좌표	x
Y좌표	y
정류소순서	stationSeq
회차여부	turnYn
'''
tags=ROUTE_STATION_TAG
class RouteStation:
	##조회할 노선 아이디를 받는다.
	def __init__(self, routeId):
		## xml url
		RouteStation.url = ROUTE_STATION_URL
		## 인증키
		RouteStation.key = KEY
		self.routeId = routeId
		self.xmlStr = "" ##xml문자열 담을 변수
		self.root = None ##최상위 항목 담을 변수
		self.isOnInternet = True ## 인터넷연결여부 
		
		##xml요청 주소에 넘길 인자 세팅
		queryParams = '?' + urlencode({quote_plus('serviceKey') : "KEYKEY", quote_plus('routeId') : self.routeId })
		queryParams = queryParams.replace("KEYKEY", RouteStation.key)
		
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
	def getStations(self):
		if not self.isOnInternet:
			return []
		return list(self.root.find("msgBody"))
	
	##정류장목록 리턴	
	def getStationNames(self):
		aList = self.getStations()
		##정류장 순서 기준을 정렬
		sorted(aList, key = lambda x: int(x.findtext("stationSeq")))
		names = []
		names.append("")
		for i in aList:
			names.append(i.findtext("stationName"))
		return names

	def getStationInfos(self):
		aList = self.getStations()
		answer = {}
		for i in aList:
			key = i.findtext(tags[0])
			valueList = []
			for j in range(1,len(tags)):
				valueList.append(i.findtext(tags[j]))
			answer[key]=valueList
		return answer



		
##테스트코드
if __name__ == "__main__" :
	dd = RouteStation("233000010")
	a=dd.getStationInfos()
	for i  in a.keys():
		print(a[i])


