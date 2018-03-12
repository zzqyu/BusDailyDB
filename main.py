from RouteLocalization import *
from PublicValue import *
from DBControl import DBControl
from RouteInfo import RouteInfo
from RouteStation import RouteStation

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
for i in range(len(routeList)):
    print(routeList[i]+"정류장")
    routeStation = RouteStation(routeList[i]).getStationInfos()
    seqIndexs = list(routeStation.keys())
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
    routeMidStations[routeList[i]]=midStaiontionName
    
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
    routeInfo = RouteInfo(routeList[i]).getInfoItems()+[routeMidStations[routeList[i]]]
    dbc.addData("routeInfo", ROUTE_INFO_DB_TAG, tuple(routeInfo), i)
