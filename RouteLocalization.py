from PublicValue import *
from StationStopByRoute import StopByRoute
def routeLocalization():
    stationList = SELECTIVE_STATION_ID
    answer = []
    addedRoute = []


    for stationId in stationList:
        sbr = StopByRoute(stationId)
        routeList = sbr.getRouteItems()
        for route in routeList:
            if not route["routeId"] in addedRoute:
                answer.append(route)
                addedRoute.append(route["routeId"])

    return addedRoute


		
##테스트코드
if __name__ == "__main__" :
    print(routeLocalization())