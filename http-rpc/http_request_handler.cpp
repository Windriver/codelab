// Copyright 2013, Baidu Inc.
// Author: Zhong Yi <zhongyi01@baidu.com>
//
// Description:

#include "minos/http-rpc/http_request_handler.h"

#include <map>
#include <vector>

#include "thirdparty/glog/logging.h"
#include "thirdparty/sofa/pbrpc/http_agent.h"
#include "thirdparty/sofa/pbrpc/pbrpc.h"

#include "toft/base/string/number.h"
#include "toft/base/string/algorithm.h"

namespace baidu {
namespace minos {

using std::string;
using std::map;
using std::vector;

bool HttpRequestHandler::HandleHttpRequest(const std::string& request_content,
                                            std::string* response_content) {
    CHECK_NOTNULL(response_content);

    VLOG(30) << "Http request content: " << request_content;

    // Parse http request content
    HttpRequest http_request;
    if (!ParseHttpRequest(request_content, &http_request)) {
        LOG(ERROR) << "Failed to parse http request content";
        return false;
    }

    // Generate html content
    string html_content;
    if (!GenerateHtml(http_request, &html_content)) {
        LOG(ERROR) << "Failed to generate html content";
        return false;
    }

    // Append http response header
    if (!AppendHttpResponseHeader(html_content, response_content)) {
        LOG(ERROR) << "Failed to append http response header";
        return false;
    }

    return true;
}

bool HttpRequestHandler::ParseHttpRequest(const std::string& request_content,
                                          HttpRequest* http_request) {
    CHECK_NOTNULL(http_request);

    vector<string> request_header_fields;
    toft::SplitString(request_content, " ", &request_header_fields);

    if (request_header_fields.size() < 2) {
        LOG(ERROR) << "Invalid http request content: " << request_content;
        return false;
    }

    http_request->method = request_header_fields.at(0);

    string url = request_header_fields.at(1);
    if ("/" == url) {
        http_request->action = INDEX;
        VLOG(30) << "Visit index";
    } else {
        // Split url with '?'
        vector<string> url_fields;
        toft::SplitString(url, "?", &url_fields);
        if (url_fields.size() < 1) {
            LOG(ERROR) << "Invalid url:" << url;
            return false;
        }

        // Split url_path with '/'
        string url_path = url_fields.at(0);
        vector<string> path_fields;
        toft::SplitString(url_path, "/", &path_fields);
        if (path_fields.size() < 1) {
            LOG(ERROR) << "Invalud url_path: " << url_path;
            return false;
        }

        // Parse from url_path
        string action = path_fields.at(0);
        if ("favicon.ico" == action) {
            VLOG(30) << "It is favicon.ico";
            http_request->action = FAVICON;
        } else if ("rpc" == action) {
            http_request->action = RPC;
            if (2 != path_fields.size()) {
                LOG(ERROR) << "Invalud url_path: " << url_path;
                return false;
            }
            http_request->rpc_method = path_fields.at(1);

            // Parse rpc request
            http_request->rpc_request =
                "config:{log_module_id:1 name:\"zhongyi\" bns_name:\"hehe\" "
                "collector_nodes_num:3 target{type:\"1\" config:\"2\"} "
                "target{type:\"1\" config:\"2\"}}";
        } else if ("flags" == action) {
            http_request->action = FLAGS;
        } else {
            http_request->action = ERROR;
        }
    }

    return true;
}

bool HttpRequestHandler::GenerateHtml(const HttpRequest& http_request,
                                      string* html_content) {
    CHECK_NOTNULL(html_content);

    if (INDEX == http_request.action) {
        return GenerateIndexHtml(http_request, html_content);
    } else if (FAVICON== http_request.action) {
        return GenerateIndexHtml(http_request, html_content);
    } else if (RPC == http_request.action) {
        return GenerateRpcHtml(http_request, html_content);
    } else if (FLAGS == http_request.action) {
        return GenerateFlagsHtml(http_request, html_content);
    } else {
        LOG(ERROR) << "Invalid action";
        return false;
    }
}

bool HttpRequestHandler::GenerateIndexHtml(const HttpRequest& http_request,
                                           string* html_content) {
    CHECK_NOTNULL(html_content);

    *html_content = "<html><head><title>Minos</title></head><body>"
                    "<h1>Minos HTTP RPC</h1>"
                    "<a href=\"rpc/ListServices\">rpc</a></br>"
                    "<a href=\"flags\">flags</a></br>"
                    "</body></html>";

    return true;
}

bool HttpRequestHandler::GenerateRpcHtml(const HttpRequest& http_request,
                                         string* html_content) {
    CHECK_NOTNULL(html_content);

    sofa::pbrpc::RpcClient rpc_client;
    sofa::pbrpc::http_agent::HttpAgent http_agent(&rpc_client);
    if (!http_agent.Init("0.0.0.0:8010")) {
        LOG(ERROR) << "Failed to init http agent";
        return false;
    }

    *html_content += "<html><head><title>Minos</title></head><body><p>";

    if ("ListServices" == http_request.rpc_method) {
        std::map<std::string, std::string> desc_map;
        if (!http_agent.ListService(&desc_map)) {
            LOG(INFO) << "Failed to list service";
            return false;
        }
        for (std::map<std::string, std::string>::iterator it = desc_map.begin();
             it != desc_map.end(); ++it) {
            if (it != desc_map.begin()) fprintf(stderr, "\n");
            fprintf(stderr,
                    "Service [%s]:\n"
                    "------------------------------\n"
                    "%s"
                    "------------------------------\n",
                    it->first.c_str(), it->second.c_str());
            *html_content += it->first;
            *html_content += "</br>";
            *html_content += it->second;
            *html_content += "</br>";
        }
    } else {
        string rpc_response;
        sofa::pbrpc::RpcController controller;
        controller.SetTimeout(1);
        http_agent.CallMethod(http_request.rpc_method, &controller,
                              &http_request.rpc_request, &rpc_response, NULL);
        if (controller.Failed()) {
            *html_content += controller.ErrorText();
        } else {
            *html_content += "RPC success! Method: " + http_request.rpc_method
                + " request: " + http_request.rpc_request;
        }
    }

    html_content->append("</p><a href=\"rpc\">rpc</a></br>"
        "<a href=\"flags\">flags</a></br>"
        "</body></html>");

    VLOG(30) << "Html content: " << *html_content;
    VLOG(30) << "Html content length: " << html_content->length();
    return true;
}

bool HttpRequestHandler::GenerateFlagsHtml(const HttpRequest& http_request,
                                           string* html_content) {
    CHECK_NOTNULL(html_content);

    *html_content = "Hehe flags";

    return true;
}

bool HttpRequestHandler::AppendHttpResponseHeader(const string& html_content,
                                                  string* response_content) {
    CHECK_NOTNULL(response_content);

    string request_header = "HTTP/1.1 200 OK\r\n"
        "Content-Type: text/html\r\n"
        "Content-Length: "
        + toft::NumberToString(html_content.length()) + "\r\n"
        "\r\n";

    response_content->append(request_header);
    response_content->append(html_content);

    return true;
}

}  // namespace minos
}  // namespace baidu
