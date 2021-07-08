from urllib.request import Request, urlopen
from urllib.parse import urlencode, quote_plus
from xml.etree.ElementTree import fromstring
from PublicValue import *
'''
<baseInfoItem>
<areaDownloadUrl>http://openapi.gbis.go.kr/ws/download?area20210627.txt</areaDownloadUrl>
<areaVersion>20210627</areaVersion>
<routeDownloadUrl>http://openapi.gbis.go.kr/ws/download?route20210627.txt</routeDownloadUrl>
<routeLineDownloadUrl>http://openapi.gbis.go.kr/ws/download?routeline20210627.txt</routeLineDownloadUrl>
<routeLineVersion>20210627</routeLineVersion>
<routeStationDownloadUrl>http://openapi.gbis.go.kr/ws/download?routestation20210627.txt</routeStationDownloadUrl>
<routeStationVersion>20210627</routeStationVersion>
<routeVersion>20210627</routeVersion>
<stationDownloadUrl>http://openapi.gbis.go.kr/ws/download?station20210627.txt</stationDownloadUrl>
<stationVersion>20210627</stationVersion>
<vehicleDownloadUrl>http://openapi.gbis.go.kr/ws/download?vehicle20210627.txt</vehicleDownloadUrl>
<vehicleVersion>20210627</vehicleVersion>
</baseInfoItem>
'''

#tags = BASE_INFO_TAG
tags = BASE_INFO_NEED_TAG

class BaseInfo:
	##조회할 노선 아이디를 받는다.
	def __init__(self):
		## xml url
		BaseInfo.url = BASE_INFO_URL
		## 인증키
		BaseInfo.key = KEY
		self.xmlStr = "" ##xml문자열 담을 변수
		self.root = None ##최상위 항목 담을 변수
		self.isOnInternet = True ## 인터넷연결여부 
		##xml요청 주소에 넘길 인자 세팅
		queryParams = '?' + urlencode({quote_plus('serviceKey') : "KEYKEY" })
		queryParams = queryParams.replace("KEYKEY", BaseInfo.key)
		
		##xml문서 받아와 str으로 xmlStr에 담는다.
		print(self.url + queryParams)
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
	def getBaseInfoItem(self):
		if not self.isOnInternet:
			return []
		return self.root.find("msgBody").findall("baseInfoItem")

	def getBaseInfoItemFields(self):
		aList = self.getBaseInfoItem()
		answer = {}
		for routeList in aList:
			for i in range(len(tags)):
				answer[tags[i]] = routeList.findtext(tags[i])
		return answer



		
##테스트코드
if __name__ == "__main__" :
	dd = BaseInfo()
	result = dd.getBaseInfoItemFields()
	for i  in range(len(result)):
		print(tags[i], result[tags[i]])


