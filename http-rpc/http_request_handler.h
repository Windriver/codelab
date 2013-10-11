// Copyright 2013, Baidu Inc.
// Author: Zhong Yi <zhongyi01@baidu.com>
//
// Description:

#include <string>

namespace baidu {
namespace minos {

enum Action {
    ERROR = 0,
    INDEX,
    RPC,
    FLAGS,
    FAVICON,
};

struct HttpRequest {
    std::string method;
    Action action;
    std::string rpc_method;
    std::string rpc_request;
};

class HttpRequestHandler {
public:
    HttpRequestHandler();
    ~HttpRequestHandler();

    static bool HandleHttpRequest(const std::string& request_content,
                                   std::string* response_content);
private:
    static bool ParseHttpRequest(const std::string& request_content,
                                 HttpRequest* http_request);

    static bool GenerateHtml(const HttpRequest& http_request,
                             std::string* html_content);
    static bool GenerateIndexHtml(const HttpRequest& http_request,
                                  std::string* html_content);
    static bool GenerateRpcHtml(const HttpRequest& http_request,
                                std::string* html_content);
    static bool GenerateFlagsHtml(const HttpRequest& http_request,
                                  std::string* html_content);

    static bool AppendHttpResponseHeader(const std::string& html_content,
                                         std::string* response_content);
};

}  // namespace minos
}  // namespace baidu
