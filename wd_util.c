/*
 * Copyright (C) 2019. Huawei Technologies Co.,Ltd.All rights reserved.
 * 
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 * 
 *     http://www.apache.org/licenses/LICENSE-2.0
 * 
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

#include <stdio.h>
#include <string.h>
#include <dirent.h>

#include "wd_util.h"

void wd_spinlock(struct wd_lock *lock)
{
	while (__atomic_test_and_set(&lock->lock, __ATOMIC_ACQUIRE))
		while (__atomic_load_n(&lock->lock, __ATOMIC_RELAXED))
			;
}

void wd_unspinlock(struct wd_lock *lock)
{
	__atomic_clear(&lock->lock, __ATOMIC_RELEASE);
}

void *drv_dma_map(struct wd_queue *q, void *va, size_t sz)
{
	struct q_info *qinfo = q->info;

	if (qinfo->ops.dma_map)
		return (void *)qinfo->ops.dma_map(qinfo->ops.usr, va, sz);
	else
		return wd_dma_map(q, va, sz);
}

void drv_dma_unmap(struct wd_queue *q, void *va, void *dma, size_t sz)
{
	struct q_info *qinfo = q->info;

	if (qinfo->ops.dma_unmap)
		qinfo->ops.dma_unmap(qinfo->ops.usr, va, dma, sz);
	else
		wd_dma_unmap(q, va, dma, sz);
}
