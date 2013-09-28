cc_library (
    name = 'http_server',
    srcs = [
        'http_server.cpp',
    ],
    deps = [
        '//thirdparty/boost:boost',
        '//thirdparty/glog:glog',
        '//toft/base/string:_number',
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
