#!/usr/bin/env python

default_adn = {
    "isDeleted"  :  False,
    "userID"  :  "51be7dbbebe2bb0b8c001811",
    "className"  :  "com.yottaa.platform.router.backplane.adn.ApplicationDeliveryNetwork",
    "author":"qa_v3",
    "maxAge"  :  60000,
    "protocolVersion"  :  "3.0",
    "sslAdn"  :  False,
    "active"  :  True,
    "keyStore"  :  None,
    "timeStamp"  :  1388648967539,
    "os_need_https"  :  False,
    "specific_system_adn"  :  "",
    "private_test"  :  False,
    "privateAdnId"  :  None,
    "usingNewPattern"  :  True,
    "type"  :  0,
    "data_center_weight_group"  :  "Default",
    "optimization_template"  :  "default",
    "originServers"  :  [
        {
            "_id"  :  "52c507b1ebe2bb2898000e5a",
            "hostName"  :  "",
            "ipAddress" :  "54.85.144.243",
            "portNumber" :  80,
            "sslPort" :  443,
            "maxConnection" :  1000,
            "connectionTimeout" :  20,
            "readTimeout" :  100,
            "dme_id" :  "12795238",
            "datacenter" :  "",
            "region" :  ""
            }
        ],
    "loadBalancers"  :  [
        {
            "_id" :  "52bc2f6bebe2bb1abe001644",
            "sessionCookie" :  "cookie",
            "loadBalanceStrategy" :  {
                "_id" :  "52bc2f6bebe2bb1abe001643",
                "type" :  "round-robin",
                "qualifier" :  {},
                "rule" : [
                    {
                        "_id" : "53fe919c0b28e41e03000022",
                        "target" : {
                            "idref" : ""
                        },
                        "match" : [
                            {
                                "operator" : "LEQ",
                                "name" : "threshold",
                                "condition" : 0.5
                            }
                        ]
                    },
                    {
                        "_id" : "53fe919c0b28e41e03000023",
                        "target" : {
                            "idref" : ""
                        },
                        "match" : []
                    }
                ]
            },
            "members" :  [],
            "removed_members" :  [],
            "hostName" :  "",
            "ipAddress" :  "",
            "label" :  "",
            "datacenter" :  "",
            "region" :  "",
            "dme_id" :  "",
            }
        ],
    "domainNames"  :  [
        {
            "_id" :  "52bc2f6bebe2bb1abe00164b",
            "hostName" :  "",
            "yottaaCNAME" :  "",
            "domain" :  "yottaa.org",
            "refSystemAdn" :  "sys-2",
            "role" :  "domain",
            "active" :  True,
            "activatable" :  False,
            "dns_record_ids" :  [],
            "dme_id" :  "12682331",
            "target" :  {
                "idref" :  "52c507b1ebe2bb2898000e5a"
                },
            "transparentMode" :  0,
            "profileIds":[],
            "stickySession" : {}
            }
        ],
    "security"  :  {
        "_id"  :  "52bc2f6bebe2bb1abe001649",
        "block"  :  [],
        "throttle"  :  [],
        "redirect"  :  [],
        }
    }

domainNames = {
            "_id" :  "52bc2f6bebe2bb1abe00164b",
            "hostName" :  "",
            "yottaaCNAME" :  "",
            "domain" :  "yottaa.org",
            "refSystemAdn" :  "sys-2",
            "role" :  "domain",
            "active" :  True,
            "activatable" :  False,
            "dns_record_ids" :  [],
            "dme_id" :  "12682331",
            "target" :  {
                "idref" :  "52c507b1ebe2bb2898000e5a"
                },
            "transparentMode" :  0,
            "profileIds":[],
            "stickySession" : {}
}

loadBalancers = {
            "_id" :  "52bc2f6bebe2bb1abe001644",
            "sessionCookie" :  "cookie",
            "loadBalanceStrategy" :  {
                "_id" :  "52bc2f6bebe2bb1abe001643",
                "type" :  "round-robin",
                "qualifier" :  {},
                },
            "members" :  [
                {
                    "idref" :  "52c507b1ebe2bb2898000e5a",
                    }
                ],
            "removed_members" :  [],
            "hostName" :  "",
            "ipAddress" :  "",
            "label" :  "",
            "datacenter" :  "",
            "region" :  "",
            "dme_id" :  ""
}

originServers = {
            "_id"  :  "",
            "hostName"  :  "",
            "ipAddress" :  "54.85.144.243",
            "portNumber" :  80,
            "sslPort" :  443,
            "maxConnection" :  1000,
            "connectionTimeout" :  20,
            "readTimeout" :  100,
            "dme_id" :  "12795238",
            "datacenter" :  "",
            "region" :  ""
}

default_tod = {
    "isDeleted"  :  False,
    "className"  :  "com.yottaa.platform.router.backplane.adn.profile.TrafficOptimizationDocument",
    "protocolVersion"  :  "3.0",
    "maxAge"  :  60000,
    "timeStamp"  :  1388649006620,
    "version"  :  "d3",
    "optimization_template" :  "default",
    "documentRules" :  [],
    "resourceRules" :  [],
    "defaultActions" :  {
        "_id" :  "52bc2f6cebe2bb1abe001669",
        "filters" :  [],
        "resourceActions" :  {
            "_id" :  "52bc2f6cebe2bb1abe001650",
            "misc" :  [
                {"_id" :  "497c2f6cebe2bb1abe001651"
                 }
                ],
            "compression" :  [
                {
                    "_id" :  "52bc2f6cebe2bb1abe001651",
                    "enabled" :  False,
                    "filters" :  [],
                    }
                ],
            "lossyImageCompression" :  [
                {
                    "_id" :  "52bc2f6cebe2bb1abe001652",
                    "enabled" :  False,
                    "filters" :  [],
                    "threshold" :  1024,
                    "maxImageSize" :  102400,
                    "ratio" :  0.75
                    }
                ],
            "cache" :  [
                {
                    "_id" :  "52bc2f6cebe2bb1abe001653",
                    "enabled" :  True,
                    "filters" :  [],
                    "ttl" :  2592000,
                    "requestMethods" :  [],
                    "cacheIfQueryStringExists" :  0,
                    "cookieNames" :  [],
                    "setCookieNames" :  [],
                    "honorCacheControl" :  True,
                    "headerRemovals" :  [],
                    "queryStrings" :  []
                    }
                ],
            "htmlCache" :  [
                {
                    "_id" :  "52bc2f6cebe2bb1abe001654",
                    "enabled" :  False,
                    "filters" :  [],
                    "ttl" :  1800,
                    "ttl_unit" :  60,
                    "requestMethods" :  [
                        "GET"
                        ],
                    "cacheIfQueryStringExists" :  1,
                    "cacheIfCookieExists" :  0,
                    "cookieNames" :  [],
                    "cacheIfSetCookieExists" :  0,
                    "setCookieNames" :  [],
                    "honorCacheControl" :  True,
                    "headerRemovals" :  [],
                    "queryStrings" :  [],
                    }
                ],
            "cdnCache" :  [
                {
                    "_id" :  "52bc2f6cebe2bb1abe001655",
                    "enabled" :  False,
                    "filters" :  [],
                    "available" :  True,
                    "cdns" :  [],
                    #object(Target),  ##point to ContentDeliveryNetwork#_id
                    "target" :  {},
                    }
                ],
            "cssMinify" :  [
                {
                    "_id" :  "52bc2f6cebe2bb1abe001656",
                    "enabled" :  False,
                    "threshold" :  1024,
                    "filters" :  []
                     }
                ],
            "jsMinify" :  [
                {
                    "_id" :  "52bc2f6cebe2bb1abe001657",
                    "enabled" :  False,
                    "threshold" :  1024,
                    "filters" :  []
                    }
                ],
            "losslessImageCompression" :  [
                {
                    "_id" :  "52bc2f6cebe2bb1abe001658",
                    "enabled" :  False,
                    "filters" :  [],
                    "threshold" :  1024,
                    "maxImageSize" :  102400
                    }
                ],
            "imageResize" :  [
                {
                    "_id" :  "52bc2f6cebe2bb1abe001659",
                    "enabled" :  False,
                    "filters" :  [],
                    "threshold" :  1024,
                    "maxImageSize" :  102400,
                    "width" :  -1,
                    "height" :  -1
                    }
                ],
            # ImageType = "JPEG" | "PNG"
            "imageTranscode" :  [
                {
                    "_id" :  "52bc2f6cebe2bb1abe00165a",
                    "enabled" :  False,
                    "filters" :  [],
                    "threshold" :  1024,
                    "maxImageSize" :  102400,
                    "source" :  "JPEG",
                    "target" :  "PNG"
                    }
                ]
            },
        "documentActions" :  {
            "_id" :  "52bc2f6cebe2bb1abe00165b",
            "rapidTag" :  [
                {
                    "_id" :  "531d2b4f2335c60bdb000144",
                    "enabled" :  True,
                    "filters" :  [],
                    "comment" :  "",
                    "action" :  []
                    }
                ],
            "transformer" :  [
                {
                    "merger" :  False,
                    "item" :  [],
                    "enabled" :  False,
                    "comment" :  True,
                    "_id" :  "5271f8152335c6628b00108b"
                    }
                ],
            "clientPrefetch" :  [
                {
                    "_id" :  "52bc2f6cebe2bb1abe00165c",
                    "enabled" :  False,
                    "filters" :  [],
                    "locationExpression" :  "body",
                    "autoImagePrefetch" :  True,
                    "expressionType" :  "tag",
                    "maxNum" :  10,
                    "headRequests" :  [],
                    "postLoadRequests" :  [],
                    "policy" :  1
                    }
                ],
            "prefetch" :  [
                {
                    "_id" :  "52bc2f6cebe2bb1abe00165d",
                    "enabled" :  False,
                    "levels" :  2,
                    "filters" :  []
                    }
                ],
            "cssCombination" :  [
                {
                    "_id" :  "52bc2f6cebe2bb1abe00165e",
                    "enabled" :  False,
                    "filters" :  [],
                    "safeLevel" :  0,
                    "ensureInSameDir" :  False,
                    "concatInline" :  False,
                    "threshold" :  102400,
                    "groups" :  []
                    }
                ],
            "jsCombination" :  [
                {
                    "_id" :  "52bc2f6cebe2bb1abe00165f",
                    "enabled" :  False,
                    "filters" :  [],
                    "safeLevel" :  0,
                    "ensureInSameDir" :  False,
                    "concatInline" :  False,
                    "threshold" :  102400,
                    "groups" :  []
                    }
                ],
            "cssSprite" :  [
                {
                    "_id" :  "52bc2f6cebe2bb1abe001660",
                    "enabled" :  False,
                    "groups" :  [],
                    "filters" :  []
                    }
                ],
            "urlRewrite" :  [
                {
                    "_id" :  "52bc2f6cebe2bb1abe001661",
                    "enabled" :  True,
                    "filters" :  [],
                    "direction" :  2,
                    "shardingSize" :  2,
                    "sharding" :  False
                    }
                ],
            "dataURI" :  [
                {
                    "_id" :  "52bc2f6cebe2bb1abe001662",
                    "enabled" :  False,
                    "filters" :  [],
                    "threshold" :  5120
                    }
                ],
            "badAssetRemoval" :  [
                {
                    "_id" :  "52bc2f6cebe2bb1abe001663",
                    "enabled" :  False,
                    "filters" :  []
                    }
                ],
            "asyncJs" :  [
                {
                    "_id" :  "52bc2f6cebe2bb1abe001664",
                    "enabled" :  False,
                    "filters" :  []
                    }
                ],
            "htmlInsert" :  [
                {
                    "_id" :  "52bc2f6cebe2bb1abe001665",
                    "enabled" :  False,
                    "filters" :  []
                    }
                ],
            "responsiveImage" :  [
                {
                    "_id" :  "52bc2f6cebe2bb1abe001666",
                    "enabled" :  False,
                    "filters" :  [],
                    "type" :  0
                    }
                ],
            "cssInline" :  [
                {
                    "_id" :  "52bc2f6cebe2bb1abe001667",
                    "enabled" :  False,
                    "filters" :  [],
                    "maxSize" :  1024,
                    "policy" :  1
                    }
                ],
            "jsInline" :  [
                {
                    "_id" :  "52bc2f6cebe2bb1abe001668",
                    "enabled" :  False,
                    "filters" :  [],
                    "maxSize" :  5120,
                    "policy" :  1
                    }
                ]
            }
        },
    "keyStore" :  None
    }

# default profiles
default_profile = {
    "isDeleted"  :  False,
    "name" :  "Default Profile",
    "type" :  0,
    "enabled" :  True,
    "className" :  "com.yottaa.platform.router.backplane.adn.profile.Profile",
    "protocolVersion" :  "3.0",
    "target" :  {
        "idref" :  "52bc2f6cebe2bb1abe00166b"
        },
    "timeStamp" :  1388649006604,
    "version" :  "d5",
    "conditions" :  [],
    "keyStore" :  None,
    "abTesting" : {
        "stateful" : True,
        "optimizationDocumentSelectionStrategy" : "",
        "enabled" : False,
        "stateTTL" : -1
        }
    }

default_mobile_profile = {
    "isDeleted" :  False,
    "name" :  "Mobile",
    "type" :  1,
    "enabled" :  False,
    "className" :  "com.yottaa.platform.router.backplane.adn.profile.Profile",
    "protocolVersion" :  "3.0",
    # tod id string
    "target" :  {
        "idref" :  "52bc2f6cebe2bb1abe00168c"
        },
    "timeStamp" :  1388649006662,
    "version" :  "d5",
    "conditions" :  [
        {
            "direction" :  1,
            "match" :  [
                {
                    "name" :  "User-Agent",
                    "type" :  0,
                    "operator" :  "CONTAIN",
                    "condition" :  "Mobile"
                    }
                ]
            }
        ],
    "keyStore" :  None
    }

default_search_profile = {
    "isDeleted" :  False,
    "name" :  "Search Engine",
    "type" :  1,
    "enabled" :  False,
    "className" :  "com.yottaa.platform.router.backplane.adn.profile.Profile",
    "protocolVersion" :  "3.0",
    "target" :  {
        "idref" :  "52bc2f6cebe2bb1abe0016d0"
        },
    "timeStamp" :  1388649006880,
    "version" :  "d5",
    "conditions" :  [
        {
            "direction" :  1,
            "match" :  [
                {
                    "name" :  "User-Agent",
                    "type" :  0,
                    "operator" :  "REGEX",
                    "condition" :  ".*crawl(er|ing).*"
                    }
                ]
            }
        ],
    "keyStore" : None
    }



