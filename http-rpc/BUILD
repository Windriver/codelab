cc_library (
    name = 'http_server',
    srcs = [
        'http_server.cpp',
        'http_request_handler.cpp',
    ],
    deps = [
        '//toft/base/string:string', 
        '//toft/system/net:socket',
        '//thirdparty/glog:glog',
        '//thirdparty/libev:ev',
        '//thirdparty/libev:event',
        '//thirdparty/sofa-pbrpc:sofa-pbrpc',
    ],
)

cc_test (
    name = 'http_server_test',
    srcs = [
        'http_server_test.cpp',
    ],
    deps = [
        ':http_server',
    ],
)
