import numpy as np
import h5py
import os
import requests
import tempfile
import time

import scann

# Instead of using a specific dataset, let's generate something with certain distribution

nvec = int(1e6) # 10M -> so we can evaluate dataset larger than cache size
dim = 768 # sbert
nq = 10000

# Scann params
ah=1
bytes_per_vec = dim / ah # regarless of lut16 or lut256, each PQ code is stored in 1 byte -> check saved index for this
reorder_num = 1
leaf_size = int(4e3)
num_leaves = int(nvec / leaf_size) # we would like leaf sizes of ~4K vectors 0> 1M/4K=250
perc_to_search = 0.1
num_leaves_to_search = int(num_leaves * perc_to_search)

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

print("dataset: ", nvec, dim)
print("queries: ", queries.shape)
print(f"leaf_size: {leaf_size}\tnum_leaves: {num_leaves}")
print(f"perc_to_search: {perc_to_search}\tnum_leaves_to_search: {num_leaves_to_search}")
print(f"ah: {ah}, bytes_per_vec: {bytes_per_vec}")

def compute_recall(neighbors, true_neighbors):
    total = 0
    for gt_row, row in zip(true_neighbors, neighbors):
        total += np.intersect1d(gt_row, row).shape[0]
    return total / true_neighbors.size

# Single thread search
print("Single thread search starts (searching all leaves)")
start = time.time()
neighbors, distances = searcher.search_batched(queries, leaves_to_search=num_leaves_to_search, pre_reorder_num_neighbors=None, final_num_neighbors=1)
end = time.time()
t_st = end - start
print("Sinlge-thread Time:", t_st)

print("Multi-thread search starts (searching all leaves)")
start = time.time()
neighbors, distances = searcher.search_batched_parallel(queries, leaves_to_search=num_leaves_to_search, pre_reorder_num_neighbors=None, final_num_neighbors=1)
end = time.time()
t_mt = end - start
print("Multi-thread Time:", t_mt)

# Search bytes include root + leaf
search_bytes = (num_leaves + (num_leaves_to_search / num_leaves) * nvec) * bytes_per_vec * nq
st_throughput = search_bytes / t_st / 1e9 
mt_throughput = search_bytes / t_mt / 1e9 
print("single thread: {:.2f} GB/s".format(st_throughput), "\t if int4: {:.2f} GB/s".format(st_throughput/2))
print("multi thread: {:.2f} GB/s".format(mt_throughput), "\t if int4: {:.2f} GB/s".format(mt_throughput/2), "\t {:.2f} x over ST".format(mt_throughput/st_throughput))

