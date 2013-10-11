// Copyright 2013, Baidu Inc.
// Author: Zhong Yi <zhongyi01@baidu.com>
//
// Description:

#ifndef MINOS_HTTP-RPC_HTTP_SERVER_H_
#define MINOS_HTTP-RPC_HTTP_SERVER_H_
#pragma once

#include <string>

#include "thirdparty/libev/ev.h"
#include "thirdparty/libev/ev++.h"

namespace toft {
class ListenerSocket;
}  // namespace toft

namespace baidu {
namespace minos {

class HttpServer {
public:
    HttpServer() :
        m_is_inited(false),
        m_loop(NULL)
    {}
    ~HttpServer();

    bool Init(const std::string& ip, int port);
    bool Start();
    bool Stop();

private:
    void HandleHttpRequest(ev::io& http_request_event, int event);

private:
    bool m_is_inited;

    toft::ListenerSocket* m_listener;

    struct ev_loop* m_loop;
    ev::io* m_http_request_event;
};

}  // namespace minos
}  // namespace baidu

#endif  // MINOS_HTTP-RPC_HTTP_SERVER_H_
