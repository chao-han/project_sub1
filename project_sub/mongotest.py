#!/user/bin/env python
# -*- coding:utf-8 -*-


import requests
from packages.yottaautil import mongodb




class mongotest(object):
    def testmongo(self):
        db = mongodb()
        db.connect_mongo()

        param = [
            {"adn.domainNames.0.transparentMode": 1},
            {"adn.domainNames.1.activatable": True},
            {"adn.domainNames.1.hostName": "aaaa.yotta.com"},
            {"defaultprofile.enabled": False},
            {"searchprofile.enabled": False},
            {"tod.defaultActions.resourceActions.cache.0.threshold": 4}
        ]

        (adn_id, profile_id, tod_id, mobile_profile_id, tod_id2, searchengine_profile_id, tod_id3) = db.create_adn(
            param=param, fulladn=True)

    def testplt_1474(self):
        db = mongodb()
        db.connect_mongo()

        param = [
            {"adn.originServers.0.ipAddress": "1.1.1.1"},
            {"adn.originServers.1.ipAddress": "2.2.2.2"},
            {"adn.originServers.1.portNumber": 8080},
            {"defaultprofile.enabled": False},
            {"searchprofile.enabled": False},
            {"tod.defaultActions.resourceActions.cache.0.threshold": 4}
        ]
        db.create_adn(param=param, fulladn=False)

    def teststickysession(self):
        db = mongodb()
        db.connect_mongo()
        param = [
            {"adn.domainNames.0.stickySession": {"cookie_name": "std",
                                                 "enabled": True,
                                                 "max_age": 1}}
        ]
        db.create_adn(param=param, fulladn=False)

    def test_tod_abtesting(self):
        db=mongodb()
        db.connect_mongo()
        param1 = [{"tod.defaultActions.resourceActions.cache.0.enabled":True}]
        tod1_id = db.create_tod(param = param1)
        param2 = [{"tod.defaultActions.resourceActions.cache.0.enabled":False}]
        tod2_id = db.create_tod(param = param2)
        param3 = [{"defaultprofile.abTesting":{
                            "enabled": True,
                            "optimizationDocumentSelectionStrategy": "tod-selection-strategy",
                            "stateful": True,
                            "stateTTL": -1

                        }}
        ]
        profile_id = db.create_profile(param = param3)
        param4 = [
        {"adn.originServers.0.hostName": tod1_id},
        {"adn.originServers.0._id": "system-topology-name"},
        {"adn.originServers.1.hostName": tod2_id},
        {"adn.originServers.1._id": "current-topology-stub"},
        {"adn.loadBalancers.0.members": [
                           {
                              "idref": "system-topology-name"
                           },
                           {
                              "idref": "current-topology-stub"
                           }
                        ]}
        ]
        adn_id = db.create_tmd(param = param4)
        db.associate_adn_profile(profile_id=profile_id,adn_id=adn_id)
        print (adn_id, profile_id, tod1_id, tod2_id)

    def test_plt_95(self):
        param = [{"tod.defaultActions.resourceActions.cache.0.enabled":True},{"tod.defaultActions.resourceActions.htmlCache.0.enabled":True}]
        db=mongodb()
        db.connect_mongo()
        (tod_id, profile_id, adn_id) = db.create_adn(param=param, fulladn=False)
        cname = db.get_cname_by_id(adn_id)
        url = "http://" + cname + "/py/expired/1.html"
        for i in range(10):
            content = requests.get(url, proxies={"http":"http://ec2-54-215-210-201.us-west-1.compute.amazonaws.com:80"})
            if content.status_code == 500:
                continue
            lastbit=0
            secondbit=0
            thirdbit=0
            if len(content.headers["x-yottaa-optimizations"].split(' ')[0].split('/')[1])==1:
                lastbit = content.headers["x-yottaa-optimizations"].split(' ')[0].split('/')[1][-1]
            if len(content.headers["x-yottaa-optimizations"].split(' ')[0].split('/')[1])==2:
                secondbit = content.headers["x-yottaa-optimizations"].split(' ')[0].split('/')[1][-2]
            if len(content.headers["x-yottaa-optimizations"].split(' ')[0].split('/')[1])==3:
                thirdbit = content.headers["x-yottaa-optimizations"].split(' ')[0].split('/')[1][-3]
            if lastbit==1 or secondbit==1 or thirdbit==1:
                print "cached"
                return True

        print "not cached"

    def test_plt_239(self):
        param = [{"tod.defaultActions.documentActions.asyncJs.0.enabled":True},
                 {"tod.defaultActions.documentActions.asyncJs.0.filters":
                      {"direction" : "1",
                                 "match" : [
                                {
                                    "operator" : "CONTAIN",
                                    "type" : "0",
                                    "name" : "URI",
                                    "condition" : "/script/1.js"
                                }
                            ]}},
                 {"tod.defaultActions.documentActions.jsCombination.0.enabled":False}
                 ]
        db=mongodb()
        db.connect_mongo()
        (tod_id, profile_id, adn_id) = db.create_adn(param=param, fulladn=False)
        cname = db.get_cname_by_id(adn_id)
        url = "http://" + cname + "/py/expired/1.html"
        for i in range(10):
            content = requests.get(url, proxies={"http":"http://ec2-54-215-210-201.us-west-1.compute.amazonaws.com:80"})

        print "not cached"

    def test_plt_523(self):
        param = [
            {"adn.originServers.1.hostName": "test.dnsyottaatest1.com"},
            {"adn.originServers.1.hostName": "qa-level3-8.dnsyottaatest1.com"},
            {"adn.domainNames.0.hostName": "test.dnsyottaatest1.com"},
            {"adn.domainNames.1.hostName": "qa-level3-8.dnsyottaatest1.com"},
            {"tod.defaultActions.documentActions.clientPrefetch.0.enabled":True},
            {"tod.defaultActions.documentActions.clientPrefetch.0.policy":2},
            {"tod.defaultActions.documentActions.dataURI.0.enabled":False},
            {"tod.defaultActions.documentActions.urlRewrite.0.enabled":True},
            {"tod.defaultActions.documentActions.urlRewrite.0.filters":{
                                                      "match": [
                                                             {
                                                                 "name": "URI",
                                                                 "type": "0",
                                                                 "operator": "CONTAIN",
                                                                 "condition": "1.png"
                                                             }
                                                         ],
                                                         "direction": 0}}
        ]
        db=mongodb()
        db.connect_mongo()
        (tod_id, profile_id, adn_id) = db.create_adn(param=param, fulladn=False)
        cname = db.get_cname_by_id(adn_id)
        url = "http://" + cname + "/py/expired/1.html"


    def test_plt_1444(self):
        param = [
            {"adn.originServers.1.ipAddress": "54.85.144.243"},
            {"adn.originServers.1.portNumber": 8080},
            {"adn.domainNames.0.stickySession": {"cookie_name" : "std-1", "enabled" : True, "max_age" : 10}},
            {"tod.defaultActions.resourceActions.cache.0.enabled":False},
            {"tod.defaultActions.resourceActions.htmlCache.0.enabled":False},
            {"tod.defaultActions.documentActions.clientPrefetch.0.enabled":False}
        ]
        db=mongodb()
        db.connect_mongo()
        (tod_id, profile_id, adn_id) = db.create_adn(param=param, fulladn=False)
        cname = db.get_cname_by_id(adn_id)
        url = "http://" + cname + "/py/expired/1.html"

    def test_plt_1474(self):
        param = [
            {"adn.originServers.1.portNumber": 8080},
            {"adn.domainNames.0.stickySession": {"cookie_name" : "std-1", "enabled" : True, "max_age" : 10}},
            {"adn.domainNames.0.transparentMode":2},
            {"tod.defaultActions.resourceActions.cache.0.enabled":False},
            {"tod.defaultActions.resourceActions.htmlCache.0.enabled":False},
            {"tod.defaultActions.documentActions.clientPrefetch.0.enabled":False}
        ]
        db=mongodb()
        db.connect_mongo()
        (tod_id, profile_id, adn_id) = db.create_adn(param=param, fulladn=False)
        cname = db.get_cname_by_id(adn_id)
        url = "http://" + cname + "/py/expired/1.html"

    def test_plt_1938(self):
        '''
        should only open the interface create_adn.

        param4 =[
        {"adn.originServers.0.hostName": "$tod1"},
        ]
        :return:
        '''
        db=mongodb()
        db.connect_mongo()

        '''
        param_tod =[]
        '''

        param1 = [{"tod.defaultActions.resourceActions.cache.0.enabled":True}]
        tod1_id = db.create_tod(param = param1)
        param2 = [{"tod.defaultActions.resourceActions.cache.0.enabled":False}]
        tod2_id = db.create_tod(param = param2)
        param3 = [
        {"defaultprofile.abTesting":{
                            "enabled": True,
                            "optimizationDocumentSelectionStrategy": "tod-selection-strategy",
                            "stateful": True,
                            "stateTTL": -1

                        }}
        ]
        profile_id = db.create_profile(param = param3)

        param4 = [
        {"adn.originServers.0.hostName": tod1_id},
        {"adn.originServers.0._id": "system-topology-name"},
        {"adn.originServers.1.hostName": tod2_id},
        {"adn.originServers.1._id": "current-topology-stub"},
        {"adn.loadBalancers.0.loadBalanceStrategy": {
                            "_id": "53fe919c0b28e41e03000021",
                            "type": "percentage",
                            "qualifier": {
                                "bulksize": 2
                            },
                            "rule": [
                                {
                                    "_id": "53fe919c0b28e41e03000022",
                                    "match": [
                                        {
                                            "name": "threshold",
                                            "condition": 0.5,
                                            "operator": "LEQ"
                                        }
                                    ],
                                    "target": {
                                        "idref": "system-topology-name"
                                    }
                                },
                                {
                                    "_id": "53fe919c0b28e41e03000023",
                                    "match": [],
                                    "target": {
                                        "idref": "current-topology-stub"
                                    }
                                }
                            ]
                        }
        }
        ]

        adn_id = db.create_tmd(param = param4)
        db.associate_adn_profile(profile_id=profile_id,adn_id=adn_id)

        print (adn_id, profile_id, tod1_id, tod2_id)

    def test_muti_profile(self):
        '''
        profile1 ,profile2 => tod1, tod2

        paramtod = [{"tod1.defaultActions.resourceActions.cache.0.enabled":True},{"tod2.defaultActions.resourceActions.cache.0.enabled":False}]
        paramprofile = [{"profile1.filter=[]"},{"profile2.filter=[]"}]

        tod2_id = db.create_tod(param = param2)
        :return:
        '''

        pass

    def get_better_result(self):
        '''
        result = db.create_adn()

        result.adn._id = # adnid
        result.adn.profiles = #[$profile_list]
        result.adn.profiles[0]._id = #profile0.id
        result.adn.profiles[0].tods = #profile0.tods
        result.adn.profiles[0].tods[0]._id = #profile0.tod0.id

        :return:
        '''
        pass


if __name__ == '__main__':
    _mongotest = mongotest()
    # _mongotest.testplt_1474()
    # _mongotest.teststickysession()
    # _mongotest.test_tod_abtesting()
    # _mongotest.test_plt_523()
    # _mongotest.test_plt_1444()
    # _mongotest.test_plt_1474()
    print "aa"
    _mongotest.test_plt_1938()
