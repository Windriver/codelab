// Copyright 2013, Not All Rights Reserved.
// Author:   Windriver
// Email:    windriver1986@gmail.com
// Created:  2013-09-28 18:10
//
// Description:

#ifndef CODELAB_BOOST-ASIO_HTTP_SERVER_H_
#define CODELAB_BOOST-ASIO_HTTP_SERVER_H_
#pragma once

#include <string>

#include "thirdparty/boost/asio.hpp"

class HttpServer {
public:
    HttpServer() :
        m_is_inited(false),
        m_acceptor(m_io_service)
    {}
    ~HttpServer();

    bool Init(const std::string& ip, int port);
    bool Run();

    void ToString(const boost::system::error_code& e);

private:
    bool m_is_inited;

    boost::asio::io_service m_io_service;
    boost::asio::ip::tcp::acceptor m_acceptor;
};

#endif  // CODELAB_BOOST-ASIO_HTTP_SERVER_H_
