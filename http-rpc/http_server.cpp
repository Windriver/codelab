// Copyright 2013, Baidu Inc.
// Author: Zhong Yi <zhongyi01@baidu.com>
//
// Description:

#include "minos/http-rpc/http_server.h"

#include "thirdparty/boost/bind.hpp"
#include "thirdparty/glog/logging.h"

#include "toft/base/string/number.h"
#include "toft/system/net/socket_address.h"
#include "toft/system/net/socket.h"

#include "minos/common/common.h"
#include "minos/http-rpc/http_request_handler.h"

namespace baidu {
namespace minos {

using std::string;
using toft::ListenerSocket;
using toft::StreamSocket;
using toft::SocketAddressInet;

HttpServer::~HttpServer() {
    MINOS_SAFE_DELETE(m_listener);

    m_is_inited = false;
}

bool HttpServer::Init(const std::string& ip, int port) {
    CHECK(!m_is_inited);

    // Create listener
    m_listener = new ListenerSocket();
    if (!m_listener->Create(AF_INET, SOCK_STREAM)) {
        LOG(ERROR) << "Failed to create listener socket for http server";
        return false;
    }
    if (!m_listener->SetReuseAddress()) {
        LOG(ERROR) << "Failed to set reuse address for listener socket of http server";
        return false;
    }

    // Bind listener and listen
    SocketAddressInet socket_address(ip + ":" + toft::NumberToString(port));
    if (!m_listener->Bind(socket_address)) {
        LOG(ERROR) << "Failed to bind listener in address: " << socket_address.ToString();
        return false;
    }

    if (!m_listener->Listen()) {
        LOG(ERROR) << "Failed to listen, socket fd:" << m_listener->Handle();
        return false;
    }
    VLOG(10) << "Succeed to bind and listen, address: " << socket_address.ToString()
        << ", socket fd: " << m_listener->Handle();

    // Init event loop, we use default event loop provided by libev
    m_loop = EV_DEFAULT;

    // Set http request event
    m_http_request_event = new ev::io(m_loop);
    m_http_request_event->set<HttpServer, &HttpServer::HandleHttpRequest>(this);
    m_http_request_event->set(m_listener->Handle(), ev::READ);
    m_http_request_event->start();

    m_is_inited = true;
    return true;
}

bool HttpServer::Start() {
    CHECK(m_is_inited);

    ev_run(m_loop, 0);

    return true;
}

void HttpServer::HandleHttpRequest(ev::io& http_request_event, int event) {
    StreamSocket acceptor;
    if (!m_listener->Accept(&acceptor)) {
        LOG(ERROR) << "Failed to accept, ";
        return;
    }
    acceptor.SetTcpKeepAliveOption(14400, 150, 5);

    string request_content;
    if (!acceptor.ReceiveLine(&request_content, 1024)) {
        LOG(ERROR) << "Failed to receive line from client";
        return;
    }

    string response_content;
    if (!HttpRequestHandler::HandleHttpRequest(request_content,
                                               &response_content)) {
        LOG(ERROR) << "Failed to handle http request";
        return;
    }
    VLOG(30) << "Response content: " << response_content;
    VLOG(30) << "Response content length: " << response_content.length();

    timeval tv;
    tv.tv_sec = 1;
    tv.tv_usec = 0;
    size_t sent_size = 0;
    if (!acceptor.SendAll(response_content.c_str(), response_content.length(), &sent_size, &tv)) {
        LOG(ERROR) << "Failed to send response to client";
        return;
    }
    VLOG(30) << "Sent length: " << sent_size;
}

}  // namespace minos
}  // namespace baidu
