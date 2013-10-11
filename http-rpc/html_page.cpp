// Copyright 2013, Baidu Inc.
// Author: Zhong Yi <zhongyi01@baidu.com>
//
// Description:

namespace baidu {
namespace minos {

HtmlPage::~HtmlPage();

HtmlPage::bool AddForm(std::string& form_in_pb_textformat) {

    return true;
}

HtmlPage::bool AddTable(std::string& table_in_pb_textformat) {

    return true;
}

HtmlPage::const std::string& Export() {

    return m_html_content;
}

}  // namespace minos
}  // namespace baidu
