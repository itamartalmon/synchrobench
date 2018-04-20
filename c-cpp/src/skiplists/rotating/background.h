/*
 * This is the interface for the background thread functions.
 *
 * Author: Ian Dick, 2013.
 */
#ifndef BACKGROUND_H_
#define BACKGROUND_H_

#include "skiplist.h"
#include "ptst.h"

void bg_init(set_t *s, int setIndex);
void bg_init_helper(int half_nb_threads);
void bg_start(int sleep_time);
void bg_stop(void);
void bg_print_stats(void);
void bg_remove(node_t *prev, node_t *node, ptst_t *ptst);
void bg_help_remove(node_t *prev, node_t *node, ptst_t *ptst);
int floor_log_2(unsigned int n);

#endif /* BACKGROUND_H_ */
