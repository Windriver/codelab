// Copyright 2013, Not All Rights Reserved.
// Author:   Windriver
// Email:    windriver1986@gmail.com
// Created:  2013-09-24 02:32
//
// Description:

#include <stdlib.h>

#include "thirdparty/gflags/gflags.h"
#include "thirdparty/glog/logging.h"

DEFINE_string(test_str, "initial", "");
DEFINE_int32(test_int32, -1, "");

int main(int argc, char *argv[]) {
  LOG(INFO) << "Dynamic set string gflag...";
  LOG(INFO) << "Before set: " << FLAGS_test_str;
  LOG(INFO) << google::SetCommandLineOption("test_str", "zhongyi");
  LOG(INFO) << "After set: " << FLAGS_test_str;

  LOG(INFO) << "Dynamic set int32 gflag...";
  LOG(INFO) << "Before set: " << FLAGS_test_int32;
  LOG(INFO) << google::SetCommandLineOption("test_int32", "15191430");
  LOG(INFO) << "After set: " << FLAGS_test_int32;

  return EXIT_SUCCESS;
}
