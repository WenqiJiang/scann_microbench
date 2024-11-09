import numpy as np
import h5py
import os
import requests
import tempfile
import time
import multiprocessing

import scann

# Instead of using a specific dataset, let's generate something with certain distribution

cpu_count = int(multiprocessing.cpu_count()/2) # consider hyper-threading

nvec = int(1e7) # 10M -> so we can evaluate dataset larger than cache size
dim = 768 # sbert
nq = 10000

# Scann params
ah=8
bytes_per_vec = dim / ah # regarless of lut16 or lut256, each PQ code is stored in 1 byte -> check saved index for this
reorder_num = 1
leaf_size = int(4e3)
num_leaves = int(nvec / leaf_size) # we would like leaf sizes of ~4K vectors 0> 1M/4K=250

# Check whether already trained
index_name = os.path.join("index", f"np_{nvec}vec_{dim}d_{leaf_size}_leafsize_ah{ah}")
if os.path.exists(index_name):
    print("Index exists, loading...")
    searcher = scann.scann_ops_pybind.load_searcher(index_name)
else:
    print("Index does not exist, generating...")
    # Create dataset and train
    dataset = np.zeros((nvec, dim), dtype=np.float16)
    # Each leaf is filled with a unique number for all vectors
    dataset_sample = np.zeros((num_leaves, dim), dtype=np.float16)
    # Manually shuffle by round-robin, so scann can train without full dataset
    for i in range(num_leaves):
        dataset_sample[i, :] = i

    for i in range(leaf_size):
        dataset[num_leaves * i: num_leaves * (i + 1), :] = dataset_sample

    # use scann.scann_ops.build() to instead create a TensorFlow-compatible searcher
    searcher = scann.scann_ops_pybind.builder(dataset, 10, "squared_l2").tree(
        num_leaves=num_leaves, num_leaves_to_search=num_leaves_to_search, training_sample_size=num_leaves * 100).score_ah(
        ah, anisotropic_quantization_threshold=0.2, hash_type="lut16").reorder(reorder_num).build()

    os.mkdir(index_name)
    searcher.serialize(index_name)

queries = np.zeros((nq, dim), dtype=np.float32)
for qid in range(nq):
    queries[qid, :] = qid % num_leaves
# shuffle to minimize the impact of cache locality across adjacent queries
np.random.shuffle(queries)

print("dataset: ", nvec, dim)
print("queries: ", queries.shape)
print(f"leaf_size: {leaf_size}\tnum_leaves: {num_leaves}")
print(f"ah: {ah}, bytes_per_vec: {bytes_per_vec}")

def compute_recall(neighbors, true_neighbors):
    total = 0
    for gt_row, row in zip(true_neighbors, neighbors):
        total += np.intersect1d(gt_row, row).shape[0]
    return total / true_neighbors.size

def compute_throughput(num_leaves_to_search, t_sec):
    # compute_bytes = ((num_leaves_to_search / num_leaves) * nvec) * bytes_per_vec * nq
    compute_bytes = (num_leaves + (num_leaves_to_search / num_leaves) * nvec) * bytes_per_vec * nq
    mem_bytes = ((num_leaves_to_search / num_leaves) * nvec) * bytes_per_vec * nq # assume that root is already in cache
    comp_throughput = compute_bytes / t_sec / 1e9 / 2 # normalize to actual 4-bit implementation
    mem_throughput = mem_bytes / t_sec / 1e9
    # Always assume lut16, and that the way the data is stored is in one byte per lut16 (as suggested in the index size)
    print("\t compute throughput: {:.2f} GB/s".format(comp_throughput), "\tmemory throughput {:.2f} GB/s".format(mem_throughput))
    # print("\tif int8(lut256) {:.2f} GB/s".format(comp_throughput), "\t if int4(lut16): {:.2f} GB/s".format(comp_throughput/2))

# Single thread search
print("Single thread search starts (searching all leaves)")
perc_to_search_list = [0.001, 0.005, 0.01, 0.05, 0.1]
for perc_to_search in perc_to_search_list:
    num_leaves_to_search = int(num_leaves * perc_to_search)
    print(f"perc_to_search: {perc_to_search}\tnum_leaves_to_search: {num_leaves_to_search}")
    start = time.time()
    #neighbors, distances = searcher.search_batched(queries, leaves_to_search=num_leaves_to_search, pre_reorder_num_neighbors=None, final_num_neighbors=1)
    for i in range(nq):
        searcher.search(queries[i], leaves_to_search=num_leaves_to_search, pre_reorder_num_neighbors=None, final_num_neighbors=1)
    end = time.time()
    t_st = end - start
    print("Sinlge-thread Time:", t_st)
    compute_throughput(num_leaves_to_search, t_st)

# Multi-thread search
print("Multi-thread search starts (searching all leaves)")
search_mt_batch_size_list = [24, 96, 1000, 10000] # cpu_count # 128
perc_to_search_list = [0.001, 0.002, 0.005, 0.01, 0.02, 0.05, 0.1]
for search_mt_batch_size in search_mt_batch_size_list:
    print(f"=== Thread batch size: {search_mt_batch_size} ===\n")
    nbatch = int(np.ceil(nq / search_mt_batch_size))
    for perc_to_search in perc_to_search_list:
        num_leaves_to_search = int(num_leaves * perc_to_search)
        np.random.shuffle(queries)
        print(f"perc_to_search: {perc_to_search}\tnum_leaves_to_search: {num_leaves_to_search}")
        start = time.time()
        for bid in range(nbatch):
            searcher.search_batched_parallel(queries[search_mt_batch_size * bid: search_mt_batch_size * (bid + 1)], leaves_to_search=num_leaves_to_search, pre_reorder_num_neighbors=None, final_num_neighbors=1)
        end = time.time()
        t_mt = end - start
        print("Multi-thread Time:", t_mt)
        compute_throughput(num_leaves_to_search, t_mt)

# Search bytes include root + leaf
# print("multi thread: if int8(lut256) {:.2f} GB/s".format(mt_throughput), "\t if int4(lut16): {:.2f} GB/s".format(mt_throughput/2), "\t {:.2f} x over ST".format(mt_throughput/st_throughput))

