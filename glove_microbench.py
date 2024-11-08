import numpy as np
import h5py
import os
import requests
import tempfile
import time

import scann

# Download dataset
with tempfile.TemporaryDirectory() as tmp:
    response = requests.get("http://ann-benchmarks.com/glove-100-angular.hdf5")
    loc = os.path.join(tmp, "glove.hdf5")
    with open(loc, 'wb') as f:
        f.write(response.content)

    glove_h5py = h5py.File(loc, "r")

list(glove_h5py.keys())

dataset = glove_h5py['train']
queries = glove_h5py['test']
nvec = dataset.shape[0]
dim = dataset.shape[1]
nq = queries.shape[0]
print(dataset.shape)
print(queries.shape)
print(dim)

# Scann params
num_leaves = 250 # we would like leaf sizes of ~4K vectors 0> 1M/4K=250
num_leaves_to_search = 1
reorder_num = 100
ah=1
bytes_per_vec = dim / ah / 2
print("bytes per vec: ", bytes_per_vec)


# Create ScaNN searcher
normalized_dataset = dataset / np.linalg.norm(dataset, axis=1)[:, np.newaxis]
# configure ScaNN as a tree - asymmetric hash hybrid with reordering
# anisotropic quantization as described in the paper; see README

# use scann.scann_ops.build() to instead create a TensorFlow-compatible searcher
searcher = scann.scann_ops_pybind.builder(normalized_dataset, 10, "dot_product").tree(
    num_leaves=250, num_leaves_to_search=250, training_sample_size=250000).score_ah(
    ah, anisotropic_quantization_threshold=0.2).reorder(reorder_num).build()

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
print("single thread: {:.2f} GB/s".format(st_throughput))
print("multi thread: {:.2f} GB/s".format(mt_throughput))
