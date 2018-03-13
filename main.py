from RouteLocalization import *
from PublicValue import *
from DBControl import DBControl
from RouteInfo import RouteInfo
from RouteStation import RouteStation
import operator

##적절한 중간 경유지 선정 함수
def selectMidStation(stationDict):
    priorityKeyword={"(경유)":-100,  "리": 1, "동": 1, "통": 1, "학교": 2, "사령부":2, "경찰서":2, "사무":3, "주민":3}
    seqIndexs = list(stationDict.keys())#키 값 리스트
    midIndex = int((int(seqIndexs[-1]) + int(seqIndexs[0]))/2) #키 값 양 끝의 중간 값
    endIndex = midIndex*2

    if stationDict[seqIndexs[-1]][-1]=='N': # 마지막 항목 정류장이 반환점이 아니면 1/4지점으로
        midIndex /= 2
        endIndex /= 2
        midIndex = round(midIndex)
        endIndex = round(endIndex)

    fivePerIndex = round(endIndex * 0.05)
    '''
    five > 0.5
    end * 0.05 > 0.5
    end * 
    '''

    if endIndex<=10:
        fivePerIndex = int(midIndex/2)

    print("[fivePerIndex]"+str(fivePerIndex), "[midIndex]"+str(midIndex), "[endIndex]"+str(endIndex))
    propertyIndex = {}
    for i in range(midIndex-fivePerIndex, midIndex+fivePerIndex+1):
        propertyIndex[i]=0
        for keyword in priorityKeyword.keys():
            if keyword in stationDict[str(i)][5]:
                propertyIndex[i]+=priorityKeyword[keyword]

    propertyIndex = sorted(propertyIndex.items(), key=operator.itemgetter(1))
    answerIndex = len(propertyIndex)-1 #    ((a, b), (c, d))
    for i in range(answerIndex-1, -1, -1):
        if propertyIndex[i][1] < propertyIndex[answerIndex][1] :
            answerIndex = i+1
            break

    for i in propertyIndex:
        print("%s ,seq: %d,  property: %d" % (stationDict[str(i[0])][5], i[0], i[1]))

    return (stationDict[str(propertyIndex[answerIndex][0])][5], stationDict[seqIndexs[-1]][-1])


    '''
    inc=1
    while True:
        print(midStaiontionName)
       # if "(경유)" in midStaiontionName:
            
        if (not "(경유)" in midStaiontionName) and ( "리" in midStaiontionName or  "동" in midStaiontionName or  "통" in midStaiontionName or  "학교" in midStaiontionName or  "마을" in midStaiontionName or  "읍" in midStaiontionName)   :
            break
        else:
            incdec = int(round(inc/2)*pow(-1, inc))
            midStaiontionName = stationDict[str(int(midIndex)+incdec)][5]
            inc+=1
            '''
    return midStaiontionName


errorCount = 0

#서버연결
##DB
server = "13.125.133.124"
serverPort = 3306 
dbc = DBControl(server, "root", "005410", "joambusdb", serverPort)
#dbc = DBControl("localhost", "root", "비번", "busarrivaldb")

#노선목록
print("노선목록")
routeList = routeLocalization()
if dbc.isThisTable("routelist"):
    dbc.emptyTable("routelist")
else:
    dbc.createTable("routelist", ROUTE_LIST_IN_JOAM_TAG, ROUTE_LIST_IN_JOAM_TAG_BYTE)
for i in range(len(routeList)):
    dbc.addData("routelist", ROUTE_LIST_IN_JOAM_TAG, routeList[i], i)


#노선정류장
print("노선정류장")
if dbc.isThisTable("routestation"):
    dbc.emptyTable("routestation")
else:
    dbc.createTable("routestation", ROUTE_STATION_DB_TAG, ROUTE_STATION_DB_TAG_BYTE)
id = 0
routeMidStations = {}
isOneWays = {}
for i in range(len(routeList)):
    print(routeList[i]+"정류장")
    routeStation = RouteStation(routeList[i]).getStationInfos()
    
    seqIndexs = list(routeStation.keys())
    '''
    midIndex = str(int((int(seqIndexs[-1]) + int(seqIndexs[0]))/2))
    if routeStation[seqIndexs[-1]][-1]=='N':
        midIndex = str(int(int(midIndex)/2))

    midStaiontionName=routeStation[midIndex][5]
    inc=1
    while True:
        print(midStaiontionName)
       # if "(경유)" in midStaiontionName:
            
        if (not "(경유)" in midStaiontionName) and ( "리" in midStaiontionName or  "동" in midStaiontionName or  "통" in midStaiontionName or  "학교" in midStaiontionName or  "마을" in midStaiontionName or  "읍" in midStaiontionName)   :
            break
        else:
            incdec = int(round(inc/2)*pow(-1, inc))
            midStaiontionName = routeStation[str(int(midIndex)+incdec)][5]
            inc+=1
            '''
    routeMidStations[routeList[i]]=selectMidStation(routeStation)
    isOneWays[routeList[i]]=routeMidStations[routeList[i]][1]
    routeMidStations[routeList[i]]=routeMidStations[routeList[i]][0]
    
    
    for seq in seqIndexs:
        stationInfo = [routeList[i], seq]
        stationInfo+=list(routeStation[seq])
    #routeStation.insert(0, routeList[i])
        dbc.addData("routestation", ROUTE_STATION_DB_TAG, tuple(stationInfo), id)
        id+=1

#노선정보
print("노선정보")
if dbc.isThisTable("routeInfo"):
    dbc.emptyTable("routeInfo")
else:
    dbc.createTable("routeInfo", ROUTE_INFO_DB_TAG, ROUTE_INFO_DB_TAG_BYTE)
for i in range(len(routeList)):
    routeInfo = RouteInfo(routeList[i]).getInfoItems()+[routeMidStations[routeList[i]], isOneWays[routeList[i]]]
    print(routeInfo)
    dbc.addData("routeInfo", ROUTE_INFO_DB_TAG, tuple(routeInfo), i)
print("끝")
