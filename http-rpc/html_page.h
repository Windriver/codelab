// Copyright 2013, Baidu Inc.
// Author: Zhong Yi <zhongyi01@baidu.com>
//
// Description:

#ifndef MINOS_HTTP-RPC_HTML_PAGE_H_
#define MINOS_HTTP-RPC_HTML_PAGE_H_
#pragma once

namespace baidu {
namespace minos {

class HtmlPage {
public:
    HtmlPage();
    ~HtmlPage();

    bool AddForm(std::string& form_in_pb_textformat);
    bool AddTable(std::string& table_in_pb_textformat);

    const std::string& Export();

private:
    std::string m_html_content;

};

}  // namespace minos
}  // namespace baidu

#endif  // MINOS_HTTP-RPC_HTML_PAGE_H_
