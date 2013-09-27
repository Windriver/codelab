// Copyright 2013, Not All Rights Reserved.
// Author:   Windriver
// Email:    windriver1986@gmail.com
// Created:  2013-09-26 23:39
//
// Description: A simple http server implemented by libev

#include <stdio.h>
#include <stdlib.h>

#include "thirdparty/libev/ev.h"

static void handle_request(EV_P_ ev_io* http_watcher, int revent) {
  puts("hehe");

  ev_io_stop(EV_A_ http_watcher);

  ev_break(EV_A_ EVBREAK_ALL);
}

int main(int argc, char *argv[]) {
  struct ev_loop* loop = EV_DEFAULT;

  ev_io http_watcher;
  int fd = 0;
  ev_io_init(&http_watcher, handle_request, fd, EV_READ);

  ev_io_start(loop, &http_watcher);

  ev_run(loop, 0);

  return EXIT_SUCCESS;
}
