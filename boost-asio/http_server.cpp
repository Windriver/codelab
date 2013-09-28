// Copyright 2013, Baidu Inc.
// Author: Zhong Yi <zhongyi01@baidu.com>
//
// Description:

#include "codelab/boost-asio/http_server.h"

#include "thirdparty/boost/bind.hpp"
#include "thirdparty/glog/logging.h"
#include "toft/base/string/number.h"

HttpServer::~HttpServer() {

    m_is_inited = false;
}

bool HttpServer::Init(const std::string& ip, int port) {
    CHECK(!m_is_inited);

    // Init acceptor
    boost::asio::ip::tcp::resolver resolver(m_io_service);
    boost::asio::ip::tcp::resolver::query query(ip, toft::IntegerToString(port));
    boost::asio::ip::tcp::endpoint endpoint = *resolver.resolve(query);
    m_acceptor.open(endpoint.protocol());
    m_acceptor.set_option(boost::asio::ip::tcp::acceptor::reuse_address(true));
    m_acceptor.bind(endpoint);
    m_acceptor.listen();

    m_is_inited = true;
    return true;
}

bool HttpServer::Run() {
    CHECK(m_is_inited);

    boost::asio::ip::tcp::socket socket(m_io_service);
    m_acceptor.async_accept(m_socket,
                            boost::bind(&HttpServer::ToString, this,
                                        boost::asio::placeholders::error));

    VLOG(10) << "Http server is running";

    m_io_service.run();

    return true;
}

void HttpServer::ToString(const boost::system::error_code& e) {
    LOG(INFO) << "Hehe";
}
