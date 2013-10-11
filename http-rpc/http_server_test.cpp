// Copyright 2013, Baidu Inc.
// Author: Zhong Yi <zhongyi01@baidu.com>
//
// Description:

#include "minos/http-rpc/http_server.h"

#include "thirdparty/glog/logging.h"
#include "thirdparty/gtest/gtest.h"

namespace baidu {
namespace minos {

class HttpServerTest : public ::testing::Test {
protected:
    virtual void SetUp() {
    }
    virtual void TearDown() {
    }
};

TEST_F(HttpServerTest, SimpleCase) {
    HttpServer server;
    ASSERT_TRUE(server.Init("0.0.0.0", 8712));

    ASSERT_TRUE(server.Start());

}

}  // namespace minos
}  // namespace baidu

int main(int argc, char *argv[]) {
    testing::InitGoogleTest(&argc, argv);
    FLAGS_v = 31;

    return RUN_ALL_TESTS();
}
