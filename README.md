
# CycloDSP

CycloDSP is GNU Radio module containing a set of building block functions, aimed at estimating functions, such as the cyclic correlation functions, typically employed for cyclostationary signal analysis.

## Description

CycloDSP is under development; at the momenti it is composed by the following sub-modules/blocks:

* CycXCorr.py: a GNU Radio block aimed at estimating cyclic (conjugate) correlation functions in both, time domain, and, cycle-frequency domain.

## Getting Started

### Dependencies

The following procedure has been tested on Ubuntu 22.04.2, but it can work on other linux distributions with modifications of dependencies.

* gnuradio
* gnuradio-dev
* cmake
* libspdlog-dev
* clang-format
* numpy
* scipy

### Installing

In order to install the GNU Radio OOT module run the following commands:

```
$ mkdir build
$ cd build
$ cmake ../
$ make
$ sudo make install
```

In `examples/cyc_cross_corr.grc` you can find a simple example flowgraph.

## Acknowledgments

This project has been developed within the collaboration between the Safty and Security department of the [Italian Aerospace Research Centre (CIRA)](https://www.cira.it/en) and the [SPRINT](https://sprint.dieti.unina.it/index.php/en) research group.

<!---If you find this project useful for your research, please considering cite this tool as:

G. Gelli, I. Iudice and D. Pascarella, "A cloud-assisted ADS-B network for UAVs based on SDR," *2022 IEEE 9th International Workshop on Metrology for AeroSpace (MetroAeroSpace)*, Pisa, Italy, 2022, pp. 7-12, doi: [10.1109/MetroAeroSpace54187.2022.9856398](https://doi.org/10.1109/MetroAeroSpace54187.2022.9856398).

You can find the bibtex code below:

```
@INPROCEEDINGS{9856398,
  author={Gelli, Giacinto and Iudice, Ivan and Pascarella, Domenico},
  booktitle={2022 IEEE 9th International Workshop on Metrology for AeroSpace (MetroAeroSpace)}, 
  title={A cloud-assisted ADS-B network for UAVs based on SDR}, 
  year={2022},
  pages={7-12},
  doi={10.1109/MetroAeroSpace54187.2022.9856398}
}
```
-->
