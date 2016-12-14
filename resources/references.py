# List of IoTdm references

child_resources = {
    'ae':['cnt','sub'],
    'cnt':['sub','cin']
}

child_parents ={
    'ae':['cb'],
    'cnt':['cb', 'ae', 'cnt'],
    'cin':['cnt'],
    'sub':['cb','ae','cnt']
}

longToShortDict = {
    "operation": "op",
    "to": "to",
    "from": "fr",
    "requestIdentifier": "rqi",
    "resourceType": "ty",
    "primitiveContent": "pc",
    "role": "rol",
    "originatingTimestamp": "ot",
    "requestExpirationTimestamp": "rqet",
    "resultExpirationTimestamp": "rset",
    "operationExecutionTime": "oet",
    "responseType": "rt",
    "resultPersistence": "rp",
    "resultContent": "rcn",
    "eventCategory": "ec",
    "deliveryAggregation": "da",
    "groupRequestIdentifier": "gid",
    "filterCriteria": "fc",
    "discoveryResultType": "drt",
    "responseStatusCode": "rsc",
    "requestPrimitive": "rqp",
    "responsePrimitive": "rsp",
    "accessControlPolicyIDs": "acpi",
    "announcedAttribute": "aa",
    "announceTo": "at",
    "creationTime": "ct",
    "expirationTime": "et",
    "labels": "lbl",
    "link": "lnk",
    "lastModifiedTime": "lt",
    "parentID": "pi",
    "resourceID": "ri",
    "stateTag": "st",
    "resourceName": "rn",
    "privileges": "pv",
    "selfPrivileges": "pvs",
    "App-ID": "api",
    "AE-ID": "aei",
    "appName": "apn",
    "pointOfAccess": "poa",
    "ontologyRef": "or",
    "nodeLink": "nl",
    "creator": "cr",
    "maxNrOfInstances": "mni",
    "maxByteSize": "mbs",
    "maxInstanceAge": "mia",
    "currentNrOfInstances": "cni",
    "currentByteSize": "cbs",
    "locationID": "li",
    "contentInfo": "cnf",
    "contentSize": "cs",
    "content": "con",
    "cseType": "cst",
    "CSE-ID": "csi",
    "supportedResourceType": "srt",
    "notificationCongestionPolicy": "ncp",
    "source": "sr",
    "target": "tg",
    "lifespan": "ls",
    "eventCat": "eca",
    "deliveryMetaData": "dmd",
    "aggregatedRequest": "arq",
    "eventID": "evi",
    "eventType": "evt",
    "eventStart": "evs",
    "eventEnd": "eve",
    "operationType": "opt",
    "dataSize": "ds",
    "execStatus": "exs",
    "execResult": "exr",
    "execDisable": "exd",
    "execTarget": "ext",
    "execMode": "exm",
    "execFrequency": "exf",
    "execDelay": "exy",
    "execNumber": "exn",
    "execReqArgs": "exra",
    "execEnable": "exe",
    "memberType": "mt",
    "currentNrOfMembers": "cnm",
    "maxNrOfMembers": "mnm",
    "memberIDs": "mid",
    "membersAccessControlPolicyIDs": "macp",
    "memberTypeValidated": "mtv",
    "consistencyStrategy": "csy",
    "groupName": "gn",
    "locationSource": "los",
    "locationUpdatePeriod": "lou",
    "locationTargetID": "lot",
    "locationServer": "lor",
    "locationContainerID": "loi",
    "locationContainerName": "lon",
    "locationStatus": "lost",
    "serviceRoles": "svr",
    "description": "dc",
    "cmdType": "cmt",
    "mgmtDefinition": "mgd",
    "objectIDs": "obis",
    "objectPaths": "obps",
    "nodeID": "ni",
    "hostedCSELink": "hcl",
    "CSEBase": "cb",
    "M2M-Ext-ID": "mei",
    "Trigger-Recipient-ID": "tri",
    "requestReachability": "rr",
    "originator": "org",
    "metaInformation": "mi",
    "requestStatus": "rs",
    "operationResult": "ors",
    "requestID": "rid",
    "scheduleElement": "se",
    "deviceIdentifier": "di",
    "ruleLinks": "rlk",
    "statsCollectID": "sci",
    "collectingEntityID": "cei",
    "collectedEntityID": "cdi",
    "devStatus": "ss",
    "statsRuleStatus": "srs",
    "statModel": "sm",
    "collectPeriod": "cp",
    "eventNotificationCriteria": "enc",
    "expirationCounter": "exc",
    "notificationURI": "nu",
    "groupID": "gpi",
    "notificationForwardingURI": "nfu",
    "batchNotify": "bn",
    "rateLimit": "rl",
    "preSubscriptionNotify": "psn",
    "pendingNotification": "pn",
    "notificationStoragePriority": "nsp",
    "latestNotify": "ln",
    "notificationContentType": "nct",
    "notificationEventCat": "nec",
    "subscriberURI": "su",
    "version": "vr",
    "URL": "url",
    "URI": "uri",
    "update": "ud",
    "updateStatus": "uds",
    "install": "in",
    "uninstall": "un",
    "installStatus": "ins",
    "activate": "act",
    "deactivate": "dea",
    "activeStatus": "acts",
    "memAvailable": "mma",
    "memTotal": "mmt",
    "areaNwkType": "ant",
    "listOfDevices": "ldv",
    "devID": "dvd",
    "devType": "dvt",
    "areaNwkId": "awi",
    "sleepInterval": "sli",
    "sleepDuration": "sld",
    "listOfNeighbors": "lnh",
    "batteryLevel": "btl",
    "batteryStatus": "bts",
    "deviceLabel": "dlb",
    "manufacturer": "man",
    "model": "mod",
    "deviceType": "dty",
    "fwVersion": "fwv",
    "swVersion": "swv",
    "hwVersion": "hwv",
    "capabilityName": "can",
    "attached": "att",
    "capabilityActionStatus": "cas",
    "enable": "ena",
    "disable": "dis",
    "currentState": "cus",
    "reboot": "rbo",
    "factoryReset": "far",
    "logTypeId": "lgt",
    "logData": "lgd",
    "logActionStatus": "lgs",
    "logStatus": "lgst",
    "logStart": "lga",
    "logStop": "lgo",
    "firmwareName": "fwn",
    "softwareName": "swn",
    "cmdhPolicyName": "cpn",
    "mgmtLink": "cmlk",
    "activeCmdhPolicyLink": "acmlk",
    "order": "od",
    "defEcValue": "dev",
    "requestOrigin": "ror",
    "requestContext": "rct",
    "requestContextNotification": "rctn",
    "requestCharacteristics": "rch",
    "applicableEventCategories": "aecs",
    "applicableEventCategory": "aec",
    "defaultRequestExpTime": "dqet",
    "defaultResultExpTime": "dset",
    "defaultOpExecTime": "doet",
    "defaultRespPersistence": "drp",
    "defaultDelAggregation": "dda",
    "limitsEventCategory": "lec",
    "limitsRequestExpTime": "lqet",
    "limitsResultExpTime": "lset",
    "limitsOpExecTime": "loet",
    "limitsRespPersistence": "lrp",
    "limitsDelAggregation": "lda",
    "targetNetwork": "ttn",
    "minReqVolume": "mrv",
    "backOffParameters": "bop",
    "otherConditions": "ohc",
    "maxBufferSize": "mbfs",
    "storagePriority": "sgp",
    "applicableCredIDs": "apci",
    "allowedApp-IDs": "aai",
    "allowedAEs": "aae",
    "accessControlPolicy": "acp",
    "accessControlPolicyAnnc": "acpA",
    "AE": "ae",
    "AEAnnc": "aeA",
    "container": "cnt",
    "containerAnnc": "cntA",
    "latest": "la",
    "oldest": "ol",
    "contentInstance": "cin",
    "contentInstanceAnnc": "cinA",
    "delivery": "dlv",
    "eventConfig": "evcg",
    "execInstance": "exin",
    "fanOutPoint": "fopt",
    "group": "grp",
    "groupAnnc": "grpA",
    "locationPolicy": "lcp",
    "locationPolicyAnnc": "lcpA",
    "m2mServiceSubscriptionProfile": "mssp",
    "mgmtCmd": "mgc",
    "mgmtObj": "mgo",
    "mgmtObjAnnc": "mgoA",
    "node": "nod",
    "nodeAnnc": "nodA",
    "pollingChannel": "pch",
    "pollingChannelURI": "pcu",
    "remoteCSE": "csr",
    "remoteCSEAnnc": "csrA",
    "request": "req",
    "schedule": "sch",
    "scheduleAnnc": "schA",
    "serviceSubscribedAppRule": "asar",
    "serviceSubscribedNode": "svsn",
    "statsCollect": "stcl",
    "statsConfig": "stcg",
    "subscription": "sub",
    "firmware": "fwr",
    "firmwareAnnc": "fwrA",
    "software": "swr",
    "softwareAnnc": "swrA",
    "memory": "mem",
    "memoryAnnc": "memA",
    "areaNwkInfo": "ani",
    "areaNwkInfoAnnc": "aniA",
    "areaNwkDeviceInfo": "andi",
    "areaNwkDeviceInfoAnnc": "andiA",
    "battery": "bat",
    "batteryAnnc": "batA",
    "deviceInfo": "dvi",
    "deviceInfoAnnc": "dviA",
    "deviceCapability": "dvc",
    "deviceCapabilityAnnc": "dvcA",
    "rebootAnnc": "rboA",
    "eventLog": "evl",
    "eventLogAnnc": "evlA",
    "cmdhPolicy": "cmp",
    "activeCmdhPolicy": "acmp",
    "cmdhDefaults": "cmdf",
    "cmdhDefEcValue": "cmdv",
    "cmdhEcDefParamValues": "cmpv",
    "cmdhLimits": "cml",
    "cmdhNetworkAccessRules": "cmnr",
    "cmdhNwAccessRule": "cmwr",
    "cmdhBuffer": "cmbf",
    "createdBefore": "crb",
    "createdAfter": "cra",
    "modifiedSince": "ms",
    "unmodifiedSince": "us",
    "stateTagSmaller": "sts",
    "stateTagBigger": "stb",
    "expireBefore": "exb",
    "expireAfter": "exa",
    "sizeAbove": "sza",
    "sizeBelow": "szb",
    "contentType": "cty",
    "limit": "lim",
    "attribute": "atr",
    "resourceStatus": "rss",
    "notificationEventType": "net",
    "operationMonitor": "om",
    "representation": "rep",
    "filterUsage": "fu",
    "eventCatType": "ect",
    "eventCatNo": "ecn",
    "number": "num",
    "duration": "dur",
    "notification": "sgn",
    "notificationEvent": "nev",
    "verificationRequest": "vrq",
    "subscriptionDeletion": "sud",
    "subscriptionReference": "sur",
    "accessId": "aci",
    "MSISDN": "msd",
    "action": "acn",
    "status": "sus",
    "childResource": "ch",
    "accessControlRule": "acr",
    "accessControlOriginators": "acor",
    "accessControlOperations": "acop",
    "accessControlContexts": "acco",
    "accessControlWindow": "a",
    "accessControlIpAddresses": "acip",
    "ipv4Addresses": "ipv4",
    "ipv6Addresses": "ipv6",
    "accessControlLocationRegion": "aclr",
    "countryCode": "accc",
    "circRegion": "accr",
    "value": "val",
    "type": "typ",
    "maxNrOfNotify": "mnn",
    "timeWindow": "tww",
    "scheduleEntry": "sce",
    "aggregatedNotification": "agn",
    "attributeList": "atrl",
    "aggregatedResponse": "agr",
    "resource": "rce",
    "URIList": "uril",
    "anyArg": "any",
    "fileType": "ftyp",
    "username": "unm",
    "password": "pwd",
    "filesize": "fsi",
    "targetFile": "tgf",
    "delaySeconds": "dss",
    "successURL": "surl",
    "startTime": "stt",
    "completeTime": "cpt",
    "UUID": "uuid",
    "executionEnvRef": "eer",
    "reset": "rst",
    "upload": "uld",
    "download": "dld",
    "softwareInstall": "swin",
    "softwareUpdate": "swup",
    "softwareUninstall": "swun",
    "tracingOption": "tcop",
    "tracingInfo": "tcin",
    "responseTypeValue": "rtv",
    "contentSerialization": "csz"
}