# scann_microbench

## Docs

### Hardware

AMD milan instances on AWS: m6a: https://aws.amazon.com/ec2/instance-types/m6a/ 

AMD Milan intro: https://www.amd.com/en/products/processors/server/epyc/7003-series.html 

m6a.metal: 48 core x 2 sockets; 768 GB memory (32 x 24 channels DDR4 3200MT/s -> 24 x 25.6 GB/s = 614.4 GB/s)

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

## Setup env

# Install conda: https://www.anaconda.com/download/success

```
conda create -n py38 python=3.8 -y
conda activate py38                                                                                                              
pip install scann
```
