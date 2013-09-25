#!/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2013, ZhongYi Inc.
# Author: Windriver <windriver1986@gmail.com>

import hashlib
import binascii
import evernote.edam.userstore.constants as UserStoreConstants
import evernote.edam.type.ttypes as Types

from evernote.api.client import EvernoteClient
from evernote.api.client import Store
from evernote.edam.userstore import UserStore
import thrift.protocol.TBinaryProtocol as TBinaryProtocol
import thrift.transport.THttpClient as THttpClient


dev_token = "S=s9:U=f38d5:E=148a8cf4838:C=141511e1c3a:P=1cd:A=en-devtoken:V=2:H=06d5f3f2d0f723c0160290955387d55a"
store_url = "https://app.yinxiang.com/shard/s9/notestore"
#client = EvernoteClient(token=dev_token)
#userStore = client.get_user_store()
#user = userStore.getUser()
##print user.username

#client =  Store(dev_token, EvernoteClient, store_url)

# 获取印象笔记 NoteStore URL

userStoreProt = TBinaryProtocol.TBinaryProtocol(THttpClient.THttpClient(store_url));
userStore = UserStore.Client(userStoreProt, userStoreProt);
notestoreUrl = userStore.getNoteStoreUrl(dev_token);

# 建立 NoteStore client 
noteStoreTrans = THttpClient.THttpClient(notestoreUrl);
noteStoreTrans.setCustomHeader("User-Agent", myUserAgent);
noteStoreProt = TBinaryProtocol(noteStoreTrans);
noteStore = NoteStore.Client(noteStoreProt, noteStoreProt);

