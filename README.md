

# Urban Streetscape Health Explorer



**An AI-assisted, GIS-based prototype for interpretable streetscape assessment in Amsterdam.**



This project explores how street-level imagery, geospatial analysis and vision-language models can support the assessment of urban environments. It provides an interactive dashboard for inspecting sampled street locations, comparing visual indicators and examining the evidence behind AI-generated classifications.



The prototype was developed as a small research demonstration relevant to AI-assisted urban redesign.



## Interactive dashboard



The Streamlit dashboard allows users to:



- Explore 50 sampled locations in Amsterdam on an interactive map.

- Select locations directly by clicking map markers.

- Inspect two opposite street-level views at each location.

- Compare four AI-classified streetscape indicators.

- Read visual evidence supporting cycling-infrastructure classifications.



**Live demo:** To be added after deployment.



**Dashboard screenshot:** To be added.



## Study area and dataset



The pilot covers a selected area of Amsterdam, approximately bounded by:



- Longitude: 4.900–4.930° E

- Latitude: 52.350–52.368° N



The dataset consists of 50 sampled panorama locations and 100 corridor-facing perspective images, with two opposite views per location.



The imagery was obtained from Amsterdam's municipal panorama service. Nearby street-network geometry was used to support the orientation and generation of perspective views.



Image redistribution permissions and attribution must be verified before publishing the photographs.



## Methodology



The workflow consists of five main stages:



1. **Spatial sampling:** Select geographically distributed panorama locations within the study area.

2. **Image processing:** Generate two corridor-facing perspective images from each 360° panorama.

3. **Human annotation:** Annotate a subset of images using four categorical streetscape indicators.

4. **AI classification and evaluation:** Apply a vision-language model, refine the cycling-classification prompt and evaluate the resulting hybrid approach.

5. **Interactive visualization:** Join predictions to geographic coordinates and display the results in a Streamlit dashboard.



### Streetscape indicators



| Indicator | Classes |

|---|---|

| Greenery | Low, medium, high, unclear |

| Pedestrian environment | Weak, moderate, strong, unclear |

| Cycling infrastructure | Absent, present, unclear |

| Motor-vehicle dominance | Low, medium, high, unclear |



The indicators describe visible characteristics of individual street images. They are not direct measurements of accessibility, safety or health outcomes.



### AI classification



The project uses a fixed version of GPT-4.1 mini to classify the perspective images.



Two classification approaches were explored:



- **Original:** Direct classification of the four streetscape indicators.

- **Evidence-first:** Generation of visual evidence before assigning categorical labels, with additional instructions distinguishing designated cycling infrastructure from parked bicycles and cyclists.



Development-set experiments informed a **hybrid approach**: the original model's predictions are retained for greenery, pedestrian environment and motor-vehicle dominance, while evidence-first predictions are used for cycling infrastructure.



All 100 perspective images have been processed using this hybrid approach.



## Evaluation



A subset of 40 images from 20 locations was manually annotated. The evaluation was split by location into:



- Development: 16 images from 8 locations.

- Holdout: 24 images from 12 locations.



The holdout annotations were reviewed before the final holdout inference and evaluation.



### Holdout results



| Indicator | Original accuracy | Hybrid accuracy | Original macro-F1 | Hybrid macro-F1 |

|---|---:|---:|---:|---:|

| Greenery | 0.458 | 0.458 | 0.355 | 0.355 |

| Pedestrian environment | 0.542 | 0.542 | 0.467 | 0.467 |

| Cycling infrastructure | 0.333 | 0.625 | 0.333 | 0.605 |

| Motor-vehicle dominance | 0.333 | 0.333 | 0.251 | 0.251 |



The hybrid approach improved cycling-infrastructure classification on the 24-image holdout. The other indicators are unchanged between configurations by design.



These results are exploratory. The evaluation sample is small, opposite views from the same location may be correlated, and the reference annotations were not independently validated by multiple annotators. The model's performance on greenery and motor-vehicle dominance remains limited.



## Run the dashboard locally



Create a Python virtual environment and install the dashboard dependencies:



```bash

pip install -r requirements.txt

```



Start the application from the project root:



```bash

streamlit run web/app.py

```



The dashboard reads `data/processed/streetscape_hybrid.geojson` and the perspective images in `data/processed/perspective_views/`.



No API key is needed to run the dashboard.



## Project structure



```text

urban-streetscape-health-explorer/

├── data/

│   ├── annotations/

│   ├── processed/

│   │   ├── perspective_views/

│   │   └── streetscape_hybrid.geojson

│   └── raw/

├── notebooks/

├── results/

│   ├── evaluation/

│   └── vlm/

├── web/

│   └── app.py

├── requirements.txt

└── README.md

```



Raw panoramas, local credentials and intermediate datasets are not required to run the dashboard.



## Limitations and future work



This prototype demonstrates an exploratory workflow rather than a validated health-assessment system. Its outputs should not be interpreted as causal evidence about the effects of street design.



Potential future extensions include larger and independently annotated datasets, more reliable greenery and pedestrian-environment assessment, network-based aggregation, and evaluation of how the visual indicators relate to independently measured urban outcomes.



## Data attribution



Street-level imagery: City of Amsterdam, municipal panorama service.



Street-network data: City of Amsterdam.



Basemap: © OpenStreetMap contributors.



The exact imagery licence, redistribution conditions and required attribution will be confirmed before public deployment.



