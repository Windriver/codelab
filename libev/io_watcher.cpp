// Copyright 2013, Not All Rights Reserved.
// Author:   Windriver
// Email:    windriver1986@gmail.com
// Created:  2013-09-27 01:00
//
// Description: A example of io watcher

#include <stdio.h>
#include <stdlib.h>

#include "thirdparty/libev/ev.h"

// 回调函数。当标准输入写操作时，被调用。
static void stdin_cb(EV_P_ ev_io* stdin_watcher, int revents) {
  puts("stdin ready");

  // 5.停止watcher
  ev_io_stop(EV_A_ stdin_watcher);

  // 6. 停止loop（这里粗暴滴停止了所有loop）
  ev_break(EV_A_ EVBREAK_ALL);
}


int main(int argc, char *argv[]) {
  // 1.初始化loop。这里使用了默认的loop。
  struct ev_loop *loop = EV_DEFAULT;

  // 2.初始化watcher（拿io_watcher为例，监视标准输入的读操作，stdin_cb是预设的回
  // 调函数）
  ev_io stdin_watcher;
  ev_io_init(&stdin_watcher, stdin_cb, 0, EV_READ);

  // 3.将watcher注册到loop上
  ev_io_start(loop, &stdin_watcher);

  // 4.启动loop
  ev_run(loop, 0);

  // 7.到这里了，说明在某回调函数中执行了ev_break。
  return EXIT_SUCCESS;
}
