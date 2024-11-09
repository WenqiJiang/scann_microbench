# scann_microbench

## Docs

### Hardware

AMD milan instances on AWS: m6a: https://aws.amazon.com/ec2/instance-types/m6a/ 

AMD Milan intro: https://www.amd.com/en/products/processors/server/epyc/7003-series.html 

m6a.metal: 48 core x 2 sockets, each socket with 2 NUMA nodes (24 core x 4, each NUMA node with 96MB memory); 768 GB memory (32 x 24 channels DDR4 3200MT/s -> 24 x 25.6 GB/s = 614.4 GB/s)

CPU: 

```
cat /proc/cpuinfo 

processor	: 191
vendor_id	: AuthenticAMD
cpu family	: 25
model		: 1
model name	: AMD EPYC 7R13 48-Core Processor
stepping	: 1
microcode	: 0xa0011d5
cpu MHz		: 2650.000
cache size	: 512 KB
physical id	: 1
siblings	: 96
core id		: 47
cpu cores	: 48
apicid		: 223
initial apicid	: 223
fpu		: yes
fpu_exception	: yes
cpuid level	: 16
wp		: yes

~$ lstopo-no-graphics

Machine (753GB total)
  Package L#0
    Group0 L#0
      NUMANode L#0 (P#0 189GB)
      L3 L#0 (32MB)
        L2 L#0 (512KB) + L1d L#0 (32KB) + L1i L#0 (32KB) + Core L#0
          PU L#0 (P#0)
          PU L#1 (P#96)
        L2 L#1 (512KB) + L1d L#1 (32KB) + L1i L#1 (32KB) + Core L#1
          PU L#2 (P#1)
          PU L#3 (P#97)
        L2 L#2 (512KB) + L1d L#2 (32KB) + L1i L#2 (32KB) + Core L#2
          PU L#4 (P#2)
          PU L#5 (P#98)
        L2 L#3 (512KB) + L1d L#3 (32KB) + L1i L#3 (32KB) + Core L#3
          PU L#6 (P#3)
          PU L#7 (P#99)
        L2 L#4 (512KB) + L1d L#4 (32KB) + L1i L#4 (32KB) + Core L#4
          PU L#8 (P#4)
          PU L#9 (P#100)
        L2 L#5 (512KB) + L1d L#5 (32KB) + L1i L#5 (32KB) + Core L#5
          PU L#10 (P#5)
          PU L#11 (P#101)
        L2 L#6 (512KB) + L1d L#6 (32KB) + L1i L#6 (32KB) + Core L#6
          PU L#12 (P#6)
          PU L#13 (P#102)
        L2 L#7 (512KB) + L1d L#7 (32KB) + L1i L#7 (32KB) + Core L#7
          PU L#14 (P#7)
          PU L#15 (P#103)
      L3 L#1 (32MB)
        L2 L#8 (512KB) + L1d L#8 (32KB) + L1i L#8 (32KB) + Core L#8
          PU L#16 (P#8)
          PU L#17 (P#104)
        L2 L#9 (512KB) + L1d L#9 (32KB) + L1i L#9 (32KB) + Core L#9
          PU L#18 (P#9)
          PU L#19 (P#105)
        L2 L#10 (512KB) + L1d L#10 (32KB) + L1i L#10 (32KB) + Core L#10
          PU L#20 (P#10)
          PU L#21 (P#106)
        L2 L#11 (512KB) + L1d L#11 (32KB) + L1i L#11 (32KB) + Core L#11
          PU L#22 (P#11)
          PU L#23 (P#107)
        L2 L#12 (512KB) + L1d L#12 (32KB) + L1i L#12 (32KB) + Core L#12
          PU L#24 (P#12)
          PU L#25 (P#108)
        L2 L#13 (512KB) + L1d L#13 (32KB) + L1i L#13 (32KB) + Core L#13
          PU L#26 (P#13)
          PU L#27 (P#109)
        L2 L#14 (512KB) + L1d L#14 (32KB) + L1i L#14 (32KB) + Core L#14
          PU L#28 (P#14)
          PU L#29 (P#110)
        L2 L#15 (512KB) + L1d L#15 (32KB) + L1i L#15 (32KB) + Core L#15
          PU L#30 (P#15)
          PU L#31 (P#111)
      L3 L#2 (32MB)
        L2 L#16 (512KB) + L1d L#16 (32KB) + L1i L#16 (32KB) + Core L#16
          PU L#32 (P#16)
          PU L#33 (P#112)
        L2 L#17 (512KB) + L1d L#17 (32KB) + L1i L#17 (32KB) + Core L#17
          PU L#34 (P#17)
          PU L#35 (P#113)
        L2 L#18 (512KB) + L1d L#18 (32KB) + L1i L#18 (32KB) + Core L#18
          PU L#36 (P#18)
          PU L#37 (P#114)
        L2 L#19 (512KB) + L1d L#19 (32KB) + L1i L#19 (32KB) + Core L#19
          PU L#38 (P#19)
          PU L#39 (P#115)
        L2 L#20 (512KB) + L1d L#20 (32KB) + L1i L#20 (32KB) + Core L#20
          PU L#40 (P#20)
          PU L#41 (P#116)
        L2 L#21 (512KB) + L1d L#21 (32KB) + L1i L#21 (32KB) + Core L#21
          PU L#42 (P#21)
          PU L#43 (P#117)
        L2 L#22 (512KB) + L1d L#22 (32KB) + L1i L#22 (32KB) + Core L#22
          PU L#44 (P#22)
          PU L#45 (P#118)
        L2 L#23 (512KB) + L1d L#23 (32KB) + L1i L#23 (32KB) + Core L#23
          PU L#46 (P#23)
          PU L#47 (P#119)
    Group0 L#1
      NUMANode L#1 (P#1 188GB)
      L3 L#3 (32MB)
        L2 L#24 (512KB) + L1d L#24 (32KB) + L1i L#24 (32KB) + Core L#24
          PU L#48 (P#24)
          PU L#49 (P#120)
        L2 L#25 (512KB) + L1d L#25 (32KB) + L1i L#25 (32KB) + Core L#25
          PU L#50 (P#25)
          PU L#51 (P#121)
        L2 L#26 (512KB) + L1d L#26 (32KB) + L1i L#26 (32KB) + Core L#26
          PU L#52 (P#26)
          PU L#53 (P#122)
        L2 L#27 (512KB) + L1d L#27 (32KB) + L1i L#27 (32KB) + Core L#27
          PU L#54 (P#27)
          PU L#55 (P#123)
        L2 L#28 (512KB) + L1d L#28 (32KB) + L1i L#28 (32KB) + Core L#28
          PU L#56 (P#28)
          PU L#57 (P#124)
        L2 L#29 (512KB) + L1d L#29 (32KB) + L1i L#29 (32KB) + Core L#29
          PU L#58 (P#29)
          PU L#59 (P#125)
        L2 L#30 (512KB) + L1d L#30 (32KB) + L1i L#30 (32KB) + Core L#30
          PU L#60 (P#30)
          PU L#61 (P#126)
        L2 L#31 (512KB) + L1d L#31 (32KB) + L1i L#31 (32KB) + Core L#31
          PU L#62 (P#31)
          PU L#63 (P#127)
      L3 L#4 (32MB)
        L2 L#32 (512KB) + L1d L#32 (32KB) + L1i L#32 (32KB) + Core L#32
          PU L#64 (P#32)
          PU L#65 (P#128)
        L2 L#33 (512KB) + L1d L#33 (32KB) + L1i L#33 (32KB) + Core L#33
          PU L#66 (P#33)
          PU L#67 (P#129)
        L2 L#34 (512KB) + L1d L#34 (32KB) + L1i L#34 (32KB) + Core L#34
          PU L#68 (P#34)
          PU L#69 (P#130)
        L2 L#35 (512KB) + L1d L#35 (32KB) + L1i L#35 (32KB) + Core L#35
          PU L#70 (P#35)
          PU L#71 (P#131)
        L2 L#36 (512KB) + L1d L#36 (32KB) + L1i L#36 (32KB) + Core L#36
          PU L#72 (P#36)
          PU L#73 (P#132)
        L2 L#37 (512KB) + L1d L#37 (32KB) + L1i L#37 (32KB) + Core L#37
          PU L#74 (P#37)
          PU L#75 (P#133)
        L2 L#38 (512KB) + L1d L#38 (32KB) + L1i L#38 (32KB) + Core L#38
          PU L#76 (P#38)
          PU L#77 (P#134)
        L2 L#39 (512KB) + L1d L#39 (32KB) + L1i L#39 (32KB) + Core L#39
          PU L#78 (P#39)
          PU L#79 (P#135)
      L3 L#5 (32MB)
        L2 L#40 (512KB) + L1d L#40 (32KB) + L1i L#40 (32KB) + Core L#40
          PU L#80 (P#40)
          PU L#81 (P#136)
        L2 L#41 (512KB) + L1d L#41 (32KB) + L1i L#41 (32KB) + Core L#41
          PU L#82 (P#41)
          PU L#83 (P#137)
        L2 L#42 (512KB) + L1d L#42 (32KB) + L1i L#42 (32KB) + Core L#42
          PU L#84 (P#42)
          PU L#85 (P#138)
        L2 L#43 (512KB) + L1d L#43 (32KB) + L1i L#43 (32KB) + Core L#43
          PU L#86 (P#43)
          PU L#87 (P#139)
        L2 L#44 (512KB) + L1d L#44 (32KB) + L1i L#44 (32KB) + Core L#44
          PU L#88 (P#44)
          PU L#89 (P#140)
        L2 L#45 (512KB) + L1d L#45 (32KB) + L1i L#45 (32KB) + Core L#45
          PU L#90 (P#45)
          PU L#91 (P#141)
        L2 L#46 (512KB) + L1d L#46 (32KB) + L1i L#46 (32KB) + Core L#46
          PU L#92 (P#46)
          PU L#93 (P#142)
        L2 L#47 (512KB) + L1d L#47 (32KB) + L1i L#47 (32KB) + Core L#47
          PU L#94 (P#47)
          PU L#95 (P#143)
      HostBridge
        PCIBridge
          PCIBridge
            PCIBridge
              PCI 24:00.0 (NVMExp)
                Block(Disk) "nvme0n1"
            PCIBridge
              PCI 44:00.0 (Ethernet)
                Net "ens33"
  Package L#1
    Group0 L#2
      NUMANode L#2 (P#2 187GB)
```

Memory:

```
sudo dmidecode -t memory

Handle 0x0070, DMI type 17, 84 bytes
Memory Device
	Array Handle: 0x0007
	Error Information Handle: 0x006F
	Total Width: 72 bits
	Data Width: 64 bits
	Size: 32 GB
	Form Factor: DIMM
	Set: None
	Locator: CPU1_DIMM_Q1
	Bank Locator: P1 CHANNEL Q
	Type: DDR4
	Type Detail: Synchronous Registered (Buffered)
	Speed: 3200 MT/s
	Manufacturer: Micron Technology
	Serial Number: F3A21FA0
	Asset Tag: DIMM Q1_AssetTag
	Part Number: 36ASF4G72PZ-3G2E7   
	Rank: 2
	Configured Memory Speed: 2933 MT/s
	Minimum Voltage: 1.2 V
	Maximum Voltage: 1.2 V
	Configured Voltage: 1.2 V
	Memory Technology: DRAM
	Memory Operating Mode Capability: Volatile memory
	Firmware Version: 36ASF4G72PZ-3G2E7   
	Module Manufacturer ID: Bank 1, Hex 0x2C
	Module Product ID: Unknown
	Memory Subsystem Controller Manufacturer ID: Unknown
	Memory Subsystem Controller Product ID: Unknown
	Non-Volatile Size: None
	Volatile Size: 32 GB
	Cache Size: None
	Logical Size: None
```

### ScaNN doc

Git: https://github.com/google-research/google-research/tree/master/scann

Setting params: "When partitioning, num_leaves should be roughly the square root of the number of datapoints."

Ref: https://github.com/google-research/google-research/blob/master/scann/docs/algorithms.md

Python API: https://github.com/google-research/google-research/blob/master/scann/scann/scann_ops/py/scann_ops_pybind.py

```
  def search_batched(
      self,
      queries,
      final_num_neighbors=None,
      pre_reorder_num_neighbors=None,
      leaves_to_search=None,
  ):

  def search_batched_parallel(
      self,
      queries,
      final_num_neighbors=None,
      pre_reorder_num_neighbors=None,
      leaves_to_search=None,
      batch_size=256,
  )
```

Tree builer API: https://github.com/google-research/google-research/blob/master/scann/scann/scann_ops/py/scann_builder.py
```
  def tree(
      self,
      num_leaves,
      num_leaves_to_search,
      training_sample_size=100000,
      min_partition_size=50,
      training_iterations=12,
      spherical=False,
      quantize_centroids=False,
      random_init=True,
      incremental_threshold=None,
      avq=None,
      soar_lambda=None,
      overretrieve_factor=None,
      # the following are set automatically
      distance_measure=None,
  ):

def score_ah(
      self,
      dimensions_per_block,
      anisotropic_quantization_threshold=float("nan"),
      training_sample_size=100000,
      min_cluster_size=100,
      hash_type="lut16",
      training_iterations=10,
      # the following are set automatically
      residual_quantization=None,
      n_dims=None,
  ):
```

* SIMD LUT implementation: https://github.com/google-research/google-research/blob/8df36a6121df3a4f8243cbf42c53f300e10dad90/scann/scann/hashes/internal/lut16_avx2.inc

* Batched searching implementation: https://github.com/google-research/google-research/blob/8df36a6121df3a4f8243cbf42c53f300e10dad90/scann/scann/scann_ops/cc/scann.cc#L445-L468

  * It seems this stuff is simply assign the search to multiple threads, thus no explicit data reuse (each thread still need to run over the search process itself)

```
Status ScannInterface::SearchBatchedParallel(const DenseDataset<float>& queries,
                                             MutableSpan<NNResultsVector> res,
                                             int final_nn, int pre_reorder_nn,
                                             int leaves, int batch_size) const {
  SCANN_RET_CHECK_EQ(queries.dimensionality(), dimensionality_);
  const size_t numQueries = queries.size();
  const size_t numCPUs = parallel_query_pool_->NumThreads();

  const size_t kBatchSize =
      std::min(std::max(min_batch_size_, DivRoundUp(numQueries, numCPUs)),
               static_cast<size_t>(batch_size));
  return ParallelForWithStatus<1>(
      Seq(DivRoundUp(numQueries, kBatchSize)), parallel_query_pool_.get(),
      [&](size_t i) {
        size_t begin = kBatchSize * i;
        size_t curSize = std::min(numQueries - begin, kBatchSize);
        vector<float> queryCopy(
            queries.data().begin() + begin * dimensionality_,
            queries.data().begin() + (begin + curSize) * dimensionality_);
        DenseDataset<float> curQueryDataset(std::move(queryCopy), curSize);
        return SearchBatched(curQueryDataset, res.subspan(begin, curSize),
                             final_nn, pre_reorder_nn, leaves);
      });
}
```

## Setup env

```
# Install conda: https://www.anaconda.com/download/success
conda create -n py38 python=3.8 -y
conda activate py38                                                                                                              
pip install scann
```

# Evaluation results

```
python microbench.py
```

Config:

```
nvec = int(1e7) # 10M -> so we can evaluate dataset larger than cache size
dim = 768 # sbert
nq = 10000

# Scann params
ah=8
bytes_per_vec = dim / ah # regarless of lut16 or lut256, each PQ code is stored in 1 byte -> check saved index for this
reorder_num = 1
leaf_size = int(4e3)
perc_to_search = 0.1 # single-thread

search_mt_batch_size_list = [24, 96, 1000, 10000] # cpu_count # 128
perc_to_search_list = [0.001, 0.002, 0.005, 0.01, 0.02, 0.05, 0.1]
```

Example log:

```
Index exists, loading...
dataset:  10000000 768
queries:  (10000, 768)
leaf_size: 4000	num_leaves: 2500
perc_to_search: 0.01	num_leaves_to_search: 25
ah: 8, bytes_per_vec: 96.0

Single thread search starts (searching all leaves)
perc_to_search: 0.001	num_leaves_to_search: 2
Sinlge-thread Time: 1.6336536407470703
	 compute throughput: 3.09 GB/s 	memory throughput 4.70 GB/s
perc_to_search: 0.005	num_leaves_to_search: 12
Sinlge-thread Time: 2.6820828914642334
	 compute throughput: 9.04 GB/s 	memory throughput 17.18 GB/s
perc_to_search: 0.01	num_leaves_to_search: 25
Sinlge-thread Time: 4.045190811157227
	 compute throughput: 12.16 GB/s 	memory throughput 23.73 GB/s
perc_to_search: 0.05	num_leaves_to_search: 125
Sinlge-thread Time: 14.414651155471802
	 compute throughput: 16.73 GB/s 	memory throughput 33.30 GB/s
perc_to_search: 0.1	num_leaves_to_search: 250
Sinlge-thread Time: 27.062594175338745
	 compute throughput: 17.78 GB/s 	memory throughput 35.47 GB/s

Multi-thread search starts (searching all leaves)
=== Thread batch size: 24 ===

perc_to_search: 0.001	num_leaves_to_search: 2
Multi-thread Time: 0.2037208080291748
	 compute throughput: 24.74 GB/s 	memory throughput 37.70 GB/s
perc_to_search: 0.002	num_leaves_to_search: 5
Multi-thread Time: 0.2862727642059326
	 compute throughput: 37.73 GB/s 	memory throughput 67.07 GB/s
perc_to_search: 0.005	num_leaves_to_search: 12
Multi-thread Time: 0.5083720684051514
	 compute throughput: 47.68 GB/s 	memory throughput 90.64 GB/s
perc_to_search: 0.01	num_leaves_to_search: 25
Multi-thread Time: 0.9016368389129639
	 compute throughput: 54.57 GB/s 	memory throughput 106.47 GB/s
perc_to_search: 0.02	num_leaves_to_search: 50
Multi-thread Time: 1.7631402015686035
	 compute throughput: 55.13 GB/s 	memory throughput 108.90 GB/s
perc_to_search: 0.05	num_leaves_to_search: 125
Multi-thread Time: 4.187558650970459
	 compute throughput: 57.60 GB/s 	memory throughput 114.63 GB/s
perc_to_search: 0.1	num_leaves_to_search: 250
Multi-thread Time: 7.700155735015869
	 compute throughput: 62.49 GB/s 	memory throughput 124.67 GB/s
=== Thread batch size: 96 ===

perc_to_search: 0.001	num_leaves_to_search: 2
Multi-thread Time: 0.12847042083740234
	 compute throughput: 39.23 GB/s 	memory throughput 59.78 GB/s
perc_to_search: 0.002	num_leaves_to_search: 5
Multi-thread Time: 0.21007728576660156
	 compute throughput: 51.41 GB/s 	memory throughput 91.39 GB/s
perc_to_search: 0.005	num_leaves_to_search: 12
Multi-thread Time: 0.4222753047943115
	 compute throughput: 57.40 GB/s 	memory throughput 109.12 GB/s
perc_to_search: 0.01	num_leaves_to_search: 25
Multi-thread Time: 0.852508544921875
	 compute throughput: 57.71 GB/s 	memory throughput 112.61 GB/s
perc_to_search: 0.02	num_leaves_to_search: 50
Multi-thread Time: 1.6127843856811523
	 compute throughput: 60.27 GB/s 	memory throughput 119.05 GB/s
perc_to_search: 0.05	num_leaves_to_search: 125
Multi-thread Time: 3.7828140258789062
	 compute throughput: 63.76 GB/s 	memory throughput 126.89 GB/s
perc_to_search: 0.1	num_leaves_to_search: 250
Multi-thread Time: 7.2210187911987305
	 compute throughput: 66.64 GB/s 	memory throughput 132.95 GB/s
=== Thread batch size: 1000 ===

perc_to_search: 0.001	num_leaves_to_search: 2
Multi-thread Time: 0.10451650619506836
	 compute throughput: 48.22 GB/s 	memory throughput 73.48 GB/s
perc_to_search: 0.002	num_leaves_to_search: 5
Multi-thread Time: 0.1939997673034668
	 compute throughput: 55.67 GB/s 	memory throughput 98.97 GB/s
perc_to_search: 0.005	num_leaves_to_search: 12
Multi-thread Time: 0.3942122459411621
	 compute throughput: 61.49 GB/s 	memory throughput 116.89 GB/s
perc_to_search: 0.01	num_leaves_to_search: 25
Multi-thread Time: 0.7705230712890625
	 compute throughput: 63.85 GB/s 	memory throughput 124.59 GB/s
perc_to_search: 0.02	num_leaves_to_search: 50
Multi-thread Time: 1.4979090690612793
	 compute throughput: 64.89 GB/s 	memory throughput 128.18 GB/s
perc_to_search: 0.05	num_leaves_to_search: 125
Multi-thread Time: 0.687361478805542
	 compute throughput: 350.91 GB/s 	memory throughput 698.32 GB/s
perc_to_search: 0.1	num_leaves_to_search: 250
Multi-thread Time: 1.0480096340179443
	 compute throughput: 459.16 GB/s 	memory throughput 916.02 GB/s
=== Thread batch size: 10000 ===

perc_to_search: 0.001	num_leaves_to_search: 2
Multi-thread Time: 0.15301275253295898
	 compute throughput: 32.94 GB/s 	memory throughput 50.19 GB/s
perc_to_search: 0.002	num_leaves_to_search: 5
Multi-thread Time: 0.24365901947021484
	 compute throughput: 44.32 GB/s 	memory throughput 78.80 GB/s
perc_to_search: 0.005	num_leaves_to_search: 12
Multi-thread Time: 0.15006494522094727
	 compute throughput: 161.53 GB/s 	memory throughput 307.07 GB/s
perc_to_search: 0.01	num_leaves_to_search: 25
Multi-thread Time: 0.1579434871673584
	 compute throughput: 311.50 GB/s 	memory throughput 607.81 GB/s
perc_to_search: 0.02	num_leaves_to_search: 50
Multi-thread Time: 0.20764946937561035
	 compute throughput: 468.10 GB/s 	memory throughput 924.64 GB/s
perc_to_search: 0.05	num_leaves_to_search: 125
Multi-thread Time: 0.3974933624267578
	 compute throughput: 606.80 GB/s 	memory throughput 1207.57 GB/s
perc_to_search: 0.1	num_leaves_to_search: 250
Multi-thread Time: 0.7120893001556396
	 compute throughput: 675.76 GB/s 	memory throughput 1348.15 GB/s
```

Analysis of results:
* Hardware
  * m6a.12xlarge
  * 24 cores ( AMD EPYC 7R13 @2650MHz)
  * 153.6 GB/s
* Batching:
  * Seems when scan ratio is high, another config is used -> e.g., using higher scan ratio 0.05  is faster than 0.02 -> so something must be batched, turning the problem into compute bound
    * there's a sudden leap of memory throughput ~ 120 GB -> 600 ~ 1300GB/s
    * e.g., see thread batch size of 10000
  * So we only target the case without data reuse
* Memory and storage:
  * It seems ScaNN use 1 byte to store 1 lut16, instead of using 4-bit
  * So for compute, I normalize the performance to the one with 4-bit storage format 
  * For memory, I assume root is always in cache, only counting the bytes for leaves; also, here 1 byte to store 1 lut16
* End-to-end results:
  * CPU throughput
    * up to 17.8 GB/s per core
  * Bandwidth (when reaching the limit of the non-reuse batching policy, last result in each thread number)
    * 124.67 ~ 132.95 GB/s 
    * 81.1 ~ 86.5 GB/s

