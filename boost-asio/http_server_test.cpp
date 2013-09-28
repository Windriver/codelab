// Copyright 2013, Not All Rights Reserved.
// Author:   Windriver
// Email:    windriver1986@gmail.com
// Created:  2013-09-28 18:10
//
// Description:

#include "codelab/boost-asio/http_server.h"

#include "thirdparty/glog/logging.h"
#include "thirdparty/gtest/gtest.h"

class HttpServerTest : public ::testing::Test {
protected:
  virtual void SetUp() {
  }
  virtual void TearDown() {
  }
};

TEST_F(HttpServerTest, SimpleCase) {
  HttpServer server;
  ASSERT_TRUE(server.Init("0.0.0.0", 12333));

  ASSERT_TRUE(server.Run());

}

int main(int argc, char *argv[]) {
  testing::InitGoogleTest(&argc, argv);
  FLAGS_v = 31;

  return RUN_ALL_TESTS();
}
