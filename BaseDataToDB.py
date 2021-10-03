import urllib3
from DBControl import DBControl
from BaseInfo import BaseInfo
from Progress import *
from PublicValue import *

##테스트코드
if __name__ == "__main__" :

    dbc = DBControl("joambus")

    jodbFlag = False
    if dbc.isThisTable("route"):
        joamData = dbc.getJoamData()
        jodbFlag = True

    http = urllib3.PoolManager()
    result = BaseInfo().getBaseInfoItemFields()
    date = result[BASE_INFO_NEED_TAG[0]]
    print("version: " + date)
    for tag in list(BASE_INFO_NEED_TAG)[1:] :
        url = result[tag]       
        req = http.request('GET', url)
        txtdata = req.data.decode('utf-8')
        if(tag == BASE_INFO_NEED_TAG[2]):
            txtdata = txtdata.replace("|정|", "|Y|")
            txtdata = txtdata.replace("|역|", "|N|")
        txtdata = txtdata.split('^')
        alist = [row.split("|") for row in txtdata]
        
        if(len(alist[0]) > len(alist[1])):
            alist[0] = alist[0][:-1]

        tableNm = tag.replace("DownloadUrl", "")
        print(tableNm)

        flag = False

        if dbc.isThisTable(tableNm):
            #backup
            dbc.dumpdb(tableNm)
            count = dbc.getRowViaSql(tableNm)
            dbc.emptyTable(tableNm)
            flag = True
        else:
            dbc.createTable(dDllSql[tableNm])

        for i in range(len(alist[1:])):
            dbc.addData(tableNm, tuple(alist[0]), alist[i+1])
            printProgress(i, len(alist[1:]), 'Progress:', 'Complete', 1, 50)
            print()

        # restore
        if(flag and count/2 > dbc.getRowViaSql(tableNm)):
            dbc.restoredb(tableNm)
        
    if(jodbFlag) :
        dbc.setJoamData(joamData)

    # restore joambus route db
    dbc.restoredb("joam_restore")
