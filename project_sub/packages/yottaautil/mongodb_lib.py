import sys

sys.path.append("../../")

import adn_template
import copy
from pymongo import MongoClient
from bson import ObjectId
import logging
import uuid
import time


class mongodb(object):
    default_adn = adn_template.default_adn
    default_profile = adn_template.default_profile
    default_tod = adn_template.default_tod
    default_mobile_profile = adn_template.default_mobile_profile
    default_search_profile = adn_template.default_search_profile
    domainNames = adn_template.domainNames
    loadBalancers = adn_template.loadBalancers
    originServers = adn_template.originServers

    def connect_mongo(self):
        uri = "mongodb://yoadmindev:Yie7zaiz@ec2-54-165-63-201.compute-1.amazonaws.com:17018/customer-staging"
        client = MongoClient(uri)
        self.db = client["customer-staging"]


    def get_profile_by_id(self, id):
        coll = self.db["profiles"]
        result = coll.find({"_id": ObjectId(id)})
        return list(result)[0]

    def get_adn_by_id(self, id):
        coll = self.db["adns"]
        result = coll.find({"_id": ObjectId(id)})
        return list(result)[0]

    def get_cname_by_id(self, id):
        coll = self.db["adns"]
        result = coll.find({"_id": ObjectId(id)})
        adn = list(result)[0]
        return adn["domainNames"][0]["yottaaCNAME"]

    # ====================mongo basic operations====================

    def insert_tod(self, param):
        coll = self.db["tods"]
        if "_id" in param.keys():
            del param["_id"]
        tod_id = coll.insert(param)
        return tod_id

    def insert_profile(self, param):
        coll = self.db["profiles"]
        profile_id = coll.insert(param)
        return profile_id

    def insert_mobile_profile(self, param):
        coll = self.db["profiles"]
        profile_id = coll.insert(param)
        return profile_id

    def insert_searchengine_profile(self, param):
        coll = self.db["profiles"]
        profile_id = coll.insert(param)
        return profile_id

    def insert_adn(self, param):
        coll = self.db["adns"]
        adn_id = coll.insert(param)
        return adn_id

    #======================merge custom setting==========================
    def make_cname(self):
        # cname = uuid.uuid4().hex[0:32] + "." + ENV.get_all_values()["suffix"]
        cname = uuid.uuid4().hex[0:32] + "." + "yottaa.org"
        return cname

    def make_hostName(self):
        hostName = "test-%s.com" % (uuid.uuid4().hex[0:6])
        return hostName

    def make_random_id(self):
        id = uuid.uuid4().hex[0:24]
        return id

    #param was custom setting, like this:
    #param={"adn.domainNames.0.transparentMode":0}
    #then we will according to the path to update the adn doc
    #model is from template, like adn_template.domainNames
    def merge_adn(self, param={}):
        default_adn = self.default_adn
        if len(param) == 0:
            self.default_adn["domainNames"][0]["yottaaCNAME"] = self.make_cname()
            self.default_adn["domainNames"][0]["hostName"] = self.make_hostName()
            return self.default_adn
        else:
            adn = default_adn
            keys = param.keys()
            for k in keys:
                if k.startswith("adn"):
                    if "domainNames" in k:
                        self.domainNames["yottaaCNAME"] = self.make_cname()
                        self.domainNames["hostName"] = self.make_hostName()
                        adn = self.merge_data(adn, param, model=self.domainNames)
                    if "loadBalancers" in k:
                        adn = self.merge_data(adn, param, model=self.loadBalancers)
                    if "originServers" in k:
                        self.originServers["_id"] = self.make_random_id()
                        adn = self.merge_data(adn, param, model=self.originServers)
                    else:
                        self.default_adn["domainNames"][0]["yottaaCNAME"] = self.make_cname()
                        self.default_adn["domainNames"][0]["hostName"] = self.make_hostName()
                        adn = self.merge_data(adn, param, model={})

            #check if there is multiple originServers, if there is, need to update loadBalancers and DomainNames
            # if len(adn["originServers"])>1 and adn["originServers"][0]["hostName"]==adn["originServers"][1]["hostName"]:
            #     for i in range(len(adn["originServers"])-1):
            #         osid = adn["originServers"][i+1]["_id"]
            #         adn["loadBalancers"][0]["members"].append({"idref" : osid})
            #     lbid = adn["loadBalancers"][0]["_id"]
            #     adn["domainNames"][0]["target"]["idref"] = lbid
            # elif len(adn["originServers"])>1:
            #     for i in range(len(adn["originServers"])-1):
            #         osid = adn["originServers"][i]["_id"]
            #         adn["domainNames"][i]["target"]["idref"] = osid
            # else:
            #     osid = adn["originServers"][0]["_id"]
            #     adn["domainNames"][0]["target"]["idref"] = osid

            return adn

    def merge_default_profile(self, param={}):
        default_profile = self.default_profile
        if len(param) <= 0:
            return default_profile
        else:
            profile = default_profile
            keys = param.keys()
            for k in keys:
                if k.startswith("defaultprofile"):
                    profile = self.merge_data(profile, param=param, model={})
            return profile

    def merge_mobile_profile(self, param={}):
        mobile_profile = self.default_mobile_profile
        if len(param) <= 0:
            return mobile_profile
        else:
            _mobile_profile = mobile_profile
            keys = param.keys()
            for k in keys:
                if k.startswith("mobileprofile"):
                    _mobile_profile = self.merge_data(_mobile_profile, param=param, model={})
            return _mobile_profile

    def merge_search_profile(self, param={}):
        search_profile = self.default_search_profile
        if len(param) <= 0:
            return search_profile
        else:
            _search_profile = search_profile
            keys = param.keys()
            for k in keys:
                if k.startswith("searchprofile"):
                    _search_profile = self.merge_data(_search_profile, param=param, model={})
            return _search_profile

    def merge_tod(self, param={}):
        tod = self.default_tod
        if len(param) <= 0:
            return tod
        else:
            _tod = tod
            keys = param.keys()
            for k in keys:
                if k.startswith("tod"):
                    _tod = self.merge_data(tod, param, model={})
            return _tod


    def merge_data(self, data={}, param={}, model={}):
        ks = param.keys()[0].split(".")
        value = param[param.keys()[0]]
        _data = data
        for i in range(len(ks) - 1):
            if (i + 1) == len(ks) - 1:
                k = ks[i + 1]
                _data[k] = value
            else:
                k = ks[i + 1]
                if k in ['0', '1', '2', '3', '4', '5']:
                    k = int(k)
                    if len(_data) > k:
                        _data = _data[k]
                    else:
                        _data.append(model)
                        _data = _data[k]
                else:
                    _data = _data[k]

        return data

    #======================mehtod==============================
    def save_normal_adn(self):
        #insert tod collection
        self.default_tod["timeStamp"] = long(time.time() * 1000)
        tod_id = self.insert_tod(self.default_tod)
        print "tod id: %s" % tod_id

        self.default_profile["timeStamp"] = long(time.time() * 1000)
        profile_id = self.insert_profile(self.default_profile)
        print "profile id: %s" % profile_id

        self.db["profiles"].update({"_id": ObjectId(profile_id)}, {'$set': {"tod_id": ObjectId(tod_id)}})
        self.db["profiles"].update({"_id": ObjectId(profile_id)}, {'$set': {"target.idref": tod_id}})

        self.default_adn["timeStamp"] = long(time.time() * 1000)

        adn_id = self.insert_adn(self.default_adn)

        if len(self.default_adn["domainNames"]) > 1:
            for i in range(len(self.default_adn["domainNames"])):
                self.db["adns"].update({"_id": ObjectId(adn_id)},
                                       {'$push': {"domainNames." + str(i) + ".profileIds": ObjectId(profile_id)}})
        else:
            self.db["adns"].update({"_id": ObjectId(adn_id)},
                                   {'$push': {"domainNames.0.profileIds": ObjectId(profile_id)}})
        # self.db["adns"].update({"_id":ObjectId(adn_id)},{'$set':{"domainNames.0.target.idref":ObjectId(self.default_adn["originServers"][0]["_id"])}})
        # self.db["adns"].update({"_id":ObjectId(adn_id)},{'$set':{"loadBalancers.0.members.0.idref":ObjectId(self.default_adn["originServers"][0]["_id"])}})

        print "adn id: %s" % adn_id
        return (tod_id, profile_id, adn_id)

    #one adn, three profiles and three tods
    def save_full_adn(self):
        tod_id = self.insert_tod(self.default_tod)
        print "tod id: %s" % tod_id

        profile_id = self.insert_profile(self.default_profile)
        print "profile id: %s" % profile_id

        self.db["profiles"].update({"_id": ObjectId(profile_id)}, {'$set': {"tod_id": ObjectId(tod_id)}})
        self.db["profiles"].update({"_id": ObjectId(profile_id)}, {'$set': {"target.idref": tod_id}})

        tod_id2 = self.insert_tod(self.default_tod)
        print "tod id: %s" % tod_id2

        mobile_profile_id = self.insert_mobile_profile(self.default_mobile_profile)
        print "mobile profile id: %s" % mobile_profile_id

        self.db["profiles"].update({"_id": ObjectId(mobile_profile_id)}, {'$set': {"tod_id": ObjectId(tod_id2)}})
        self.db["profiles"].update({"_id": ObjectId(profile_id)}, {'$set': {"target.idref": tod_id2}})

        tod_id3 = self.insert_tod(self.default_tod)
        print "tod id: %s" % tod_id3

        searchengine_profile_id = self.insert_searchengine_profile(self.default_search_profile)
        print "search engine profile id : %s " % searchengine_profile_id

        self.db["profiles"].update({"_id": ObjectId(searchengine_profile_id)}, {'$set': {"tod_id": ObjectId(tod_id3)}})
        self.db["profiles"].update({"_id": ObjectId(profile_id)}, {'$set': {"target.idref": tod_id3}})

        adn_id = self.insert_adn(self.default_adn)
        self.db["adns"].update({"_id": ObjectId(adn_id)},
                               {'$push': {"domainNames.0.profileIds": ObjectId(mobile_profile_id)}})
        # self.db["adns"].update({"_id":ObjectId(adn_id)},{'$set':{"domainNames.0.target.idref":ObjectId(self.default_adn["originServers"][0]["_id"])}})
        # self.db["adns"].update({"_id":ObjectId(adn_id)},{'$set':{"loadBalancers.0.members.0.idref":ObjectId(self.default_adn["originServers"][0]["_id"])}})

        self.log = logging.getLogger("create adn, id is %s" % adn_id)
        print "adn id: %s" % adn_id

        return (adn_id, profile_id, tod_id, mobile_profile_id, tod_id2, searchengine_profile_id, tod_id3)

    #fulladn means, 1 adn with 3 profiles, every profile has 1 tod
    #when fulladn=False, 1 adn with 1 profile, 1 profile with 1 tod
    def create_adn(self, param, fulladn=False):
        n = len(param)
        self.default_adn["domainNames"][0]["yottaaCNAME"] = self.make_cname()
        self.default_adn["domainNames"][0]["hostName"] = self.make_hostName()
        if n > 0:
            for i in range(n):
                dic = param[i]
                key = dic.keys()[0]
                if key.startswith("adn"):
                    self.default_adn = self.merge_adn(param=dic)
                if key.startswith("defaultprofile"):
                    self.default_profile = self.merge_default_profile(param=dic)
                if key.startswith("mobileprofile"):
                    self.default_mobile_profile = self.merge_mobile_profile(param=dic)
                if key.startswith("searchprofile"):
                    self.default_search_profile = self.merge_search_profile(param=dic)
                if key.startswith("tod"):
                    self.default_tod = self.merge_tod(param=dic)

            # logic for adn, mainly about originservers, loadbalancers and domainnames
            adn = self.default_adn
            if len(adn["originServers"]) > 1 and adn["originServers"][0]["hostName"] == adn["originServers"][1][
                "hostName"]:
                for i in range(len(adn["originServers"])):
                    osid = adn["originServers"][i]["_id"]
                    adn["loadBalancers"][0]["members"].append({"idref": osid})
                lbid = adn["loadBalancers"][0]["_id"]
                adn["domainNames"][0]["target"]["idref"] = lbid
            elif len(adn["originServers"]) > 1:
                for i in range(len(adn["originServers"])):
                    osid = adn["originServers"][i]["_id"]
                    adn["domainNames"][i]["target"]["idref"] = osid
            else:
                osid = adn["originServers"][0]["_id"]
                adn["domainNames"][0]["target"]["idref"] = osid

        if fulladn:
            return self.save_full_adn()
        else:
            return self.save_normal_adn()


    def create_tod(self, param):
        n = len(param)
        if n > 0:
            for i in range(n):
                dic = param[i]
                key = dic.keys()[0]
                if key.startswith("tod"):
                    self.default_tod = self.merge_tod(param=dic)
        tod_id = self.insert_tod(self.default_tod)
        return tod_id

    def create_profile(self, param):
        n = len(param)
        if n > 0:
            for i in range(n):
                dic = param[i]
                key = dic.keys()[0]
                if key.startswith("defaultprofile"):
                    self.default_profile = self.merge_default_profile(param=dic)
        profile_id = self.insert_profile(self.default_profile)
        return profile_id

    def create_tmd(self, param):
        n = len(param)
        if n > 0:
            for i in range(n):
                dic = param[i]
                key = dic.keys()[0]
                if key.startswith("adn"):
                    self.default_adn = self.merge_adn(param=dic)
        tmd_id = self.insert_adn(self.default_adn)
        return tmd_id

    def associate_adn_profile(self, profile_id, adn_id):
        self.db["adns"].update({"_id": ObjectId(adn_id)}, {'$push': {"domainNames.0.profileIds": ObjectId(profile_id)}})


if __name__ == '__main__':
    db = mongodb()
    db.connect_mongo()

    # param = [
    # {"adn.domainNames.0.transparentMode":1},
    #     {"adn.domainNames.1.activatable":True},
    #     {"defaultprofile.version":"12"}
    # ]

    # param = [
    #     {"adn.domainNames.0.transparentMode":1},
    #     {"adn.domainNames.1.activatable":True},
    #     {"defaultprofile.enabled":False},
    #     {"searchprofile.enabled":False},
    #     {"tod.defaultActions.resourceActions.cache.0.threshold":4}
    # ]

    param1 = [{"tod.defaultActions.resourceActions.cache.0.enabled": True}]
    tod1_id = db.create_tod(param=param1)
    param2 = [{"tod.defaultActions.resourceActions.cache.0.enabled": False}]
    tod2_id = db.create_tod(param=param2)
    param3 = [
        {"defaultprofile.abTesting": {
            "enabled": True,
            "optimizationDocumentSelectionStrategy": "tod-selection-strategy",
            "stateful": True,
            "stateTTL": -1

        }}
    ]
    profile_id = db.create_profile(param=param3)

    #don't write _id first
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
    adn_id = db.create_tmd(param=param4)
    db.associate_adn_profile(profile_id=profile_id, adn_id=adn_id)

    print (adn_id, profile_id, tod1_id, tod2_id)



    # param = [
    #     {"defaultprofile.enabled":False}
    # ]
    # db.create_adn(param=param,fulladn=True)

    # param = [{"tod.defaultActions.resourceActions.cache.0.threshold":4}]
    # db.create_adn(param=param,fulladn=False)




