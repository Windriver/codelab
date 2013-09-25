#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2013, ZhongYi Inc.
# Author: Windriver <windriver1986@gmail.com>

from evernote.edam.userstore import UserStore
from evernote.edam.notestore import NoteStore

import thrift.protocol.TBinaryProtocol as TBinaryProtocol
import thrift.transport.THttpClient as THttpClient


print "代码演示了如何调用中文Evernote（印象笔记）的API来访问开发者自己的笔记。主要难点是理解Thrift RPC的使用，以及UserStore和NoteStore这两个核心概念"

# 开发者Token和note_store_url使用你从官方获得的（链接：http://dev.yinxiang.com/documentation/cloud/chapters/Authentication.php#devtoken）
# user_store_url是通用的
dev_token = "Fill it with your own token"
user_store_url = "https://app.yinxiang.com/edam/user"
note_store_url = "https://app.yinxiang.com/shard/s9/notestore"

# 建立 UserStore 的 Client
user_store_client = THttpClient.THttpClient(user_store_url)
user_store_proto = TBinaryProtocol.TBinaryProtocol(user_store_client)
user_store = UserStore.Client(user_store_proto, user_store_proto)

print "\n输出用户的信息:"
user = user_store.getUser(dev_token)
print user.username, user.id

# 建立 NoteStore 的 Client 
note_store_client = THttpClient.THttpClient(note_store_url)
note_store_proto = TBinaryProtocol.TBinaryProtocol(note_store_client)
note_store = NoteStore.Client(note_store_proto, note_store_proto)

print "\n输出各个笔记本的信息:"
notebooks = note_store.listNotebooks(dev_token)
for notebook in notebooks:
  print notebook.name, notebook.serviceCreated
