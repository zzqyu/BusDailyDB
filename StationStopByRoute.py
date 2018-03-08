from urllib.request import Request, urlopen
from urllib.parse import urlencode, quote_plus
from xml.etree.ElementTree import fromstring
from PublicValue import *
'''
<busRouteList>
<districtCd>2</districtCd>
<regionName>화성</regionName>
<routeId>233000080</routeId>
<routeName>21</routeName>
<routeTypeCd>13</routeTypeCd>
<routeTypeName>일반형시내버스</routeTypeName>
<staOrder>10</staOrder>
</busRouteList>
'''

tags=STATION_STOP_BY_ROUTR_TAG

class StopByRoute:
	##조회할 노선 아이디를 받는다.
	def __init__(self, stationId):
		## xml url
		StopByRoute.url = STATION_STOP_BY_ROUTR_URL
		## 인증키
		StopByRoute.key = KEY
		self.stationId = stationId
		self.xmlStr = "" ##xml문자열 담을 변수
		self.root = None ##최상위 항목 담을 변수
		self.isOnInternet = True ## 인터넷연결여부 
		print(stationId)
		##xml요청 주소에 넘길 인자 세팅
		queryParams = '?' + urlencode({quote_plus('serviceKey') : "KEYKEY", quote_plus('stationId') : self.stationId })
		queryParams = queryParams.replace("KEYKEY", StopByRoute.key)
		
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
	def getRouteList(self):
		if not self.isOnInternet:
			return []
		return self.root.find("msgBody").findall("busRouteList")

	def getRouteItems(self):
		aList = self.getRouteList()
		answer = []
		for routeList in aList:
			route = {}
			for i in range(len(tags)):
				#route.append(routeList.findtext(tags[i]))
				route[tags[i]] = routeList.findtext(tags[i])
			answer.append(route)
		return answer



		
##테스트코드
if __name__ == "__main__" :
	dd = StopByRoute("233000452")
	result = dd.getRouteItems()
	for route in result:
		for i  in range(len(route)):
			print(tags[i], route[tags[i]])


