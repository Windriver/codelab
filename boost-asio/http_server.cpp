// Copyright 2013, Not All Rights Reserved.
// Author:   Windriver
// Email:    windriver1986@gmail.com
// Created:  2013-09-28 18:10
//
// Description:

#include "codelab/boost-asio/http_server.h"

#include "thirdparty/boost/bind.hpp"
#include "thirdparty/glog/logging.h"

HttpServer::~HttpServer() {

  m_is_inited = false;
}

bool HttpServer::Init(const std::string& ip, const std::string& port) {
  CHECK(!m_is_inited);

  // Init acceptor
  boost::asio::ip::tcp::resolver resolver(m_io_service);
  boost::asio::ip::tcp::resolver::query query(ip, port);
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
  m_acceptor.async_accept(socket,
                          boost::bind(&HttpServer::HandleRequest, this,
                                      boost::asio::placeholders::error));

  VLOG(10) << "Http server is running";

  m_io_service.run();

  return true;
}

void HttpServer::HandleRequest(const boost::system::error_code& e) {
  LOG(INFO) << "Hehe";
}
