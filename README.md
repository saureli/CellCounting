# CC Tool

## Overview

This repository provides a Python-based image analysis pipeline for the detection and quantification of senescent cells in microscopy images.
The method combines nuclear segmentation from fluorescence microscopy (DAPI staining) with senescence-associated β-galactosidase (SA-β-gal / X-Gal) signal detection from brightfield images.

The final output includes:

* Total number of detected nuclei (cells)
* Number of senescent cells (SA-β-gal positive)
* Visual overlay of detected cells and markers

---

## Input Data

The script requires two co-registered microscopy images of the same field of view:

1. **DAPI fluorescence image**

   * Used for nuclear detection
   * Extracted from the blue channel of the image stack

2. **Brightfield image (X-Gal / SA-β-gal staining)**

   * Used to detect senescence-associated staining regions

⚠️ The two images must correspond to the same sample region.

---

## Output

The script generates:

* A visualization showing:

  * Raw DAPI image
  * Brightfield image
  * Detected nuclei (red markers)
  * Detected senescence-associated regions (colored overlay)

* Console output:

  * `dapi cells = N`
  * `senescent cells = M`

Where:

* **N** = total number of nuclei detected
* **M** = number of senescent cells identified

---

## Methodology

The analysis pipeline consists of the following steps:

### 1. Image preprocessing

* Gaussian filtering is applied to reduce noise:

  * DAPI channel: σ = 10
  * Brightfield channel: σ = 4

### 2. Threshold optimization

* An adaptive threshold is selected by maximizing the number of detected objects across intensity levels.

### 3. Nuclear segmentation

* Local maxima detection is used to identify nuclear centers.
* Connected components labeling is applied to count nuclei.

### 4. Senescence detection

* X-Gal positive regions are identified via thresholding.
* Edge/border detection is used to define staining regions.

### 5. Association step

* A nucleus is classified as senescent if it is within a fixed distance (50 pixels) from a detected X-Gal positive region.

---

## Requirements

The script depends on the following Python libraries:

```bash
numpy
matplotlib
mahotas
pylab
```

Install them using:

```bash
pip install numpy matplotlib mahotas
```

---

## Usage

Run the script directly:

```bash
python script.py
```

Make sure the following files are in the same directory:

* `E_pozzo1-1-d_2995.png` (DAPI image)
* `E_pozzo1-1-b_2994.png` (brightfield image)

---

## Notes

* Image filenames are currently hardcoded in the script and should be modified for new datasets.
* The distance threshold (50 pixels) used for senescence classification may require tuning depending on microscope resolution.
* The pipeline assumes perfect spatial alignment between the two images.
