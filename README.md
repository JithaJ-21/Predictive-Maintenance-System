### 🚀 Industrial Predictive Maintenance System

#### Simulated Industrial Monitoring using ESP32 (Wokwi), ThingSpeak, Machine Learning & Streamlit Dashboard

#### ✨ Features

- Industrial IoT based Predictive Maintenance
- ESP32 Sensor Simulation using Wokwi
- ThingSpeak Cloud Integration
- Rule-Based Anomaly Detection
- Machine Learning based Health Prediction
- Machine Learning based Fault Prediction
- RMS & Peak Signal Analysis
- Health Score & Remaining Useful Life Estimation
- Historical Trend Visualization
- Professional PDF Report Generation
- Streamlit Interactive Dashboard
---------

#### Project Structure

```
Predictive_Maintenance/
│
├── main.py
├── config.py
│
├── data/
│     └── machine_log.csv
├── Dataset/
│     └── machine_dataset.csv
├── graphs/
│
├── python/
│     ├── anomaly.py
│     ├── analysis.py
│     ├── cloud.py
│     ├── csv_logger.py
|     ├── dashboard.py
│     ├── fault_predict.py
|     ├── generate_dataset.py
│     ├── historical.py
│     ├── live_sensor.py
│     ├── pdf_report.py
│     ├── predict.py
│     ├── read_thingspeak.py
|     ├── simulator.py
|     ├── train_fault_model.py
|     ├── train_model.py
│
└── README.md
```
--------
#### Module Description
##### 1) main.py

The central execution file of the project.

Responsibilities:

- Reads sensor values from ThingSpeak
- Generates vibration signals
- Performs signal processing
- Executes anomaly detection
- Runs AI prediction
- Calculates Health Score, Efficiency and Remaining Useful Life
- Uploads processed results back to ThingSpeak
- Stores data in CSV
- Generates graphs

This file acts as the main controller of the complete system.

##### 2) dashboard.py

Implements the Streamlit web dashboard.

Displays:

- Machine Health
- Temperature
- RMS
- Peak Value
- Health Score
- Efficiency
- Remaining Useful Life
- AI Prediction
- Fault Analysis
- Historical Trends

Also provides the Generate PDF Report button, which invokes the PDF report generation module.

##### 3) pdf_report.py

Generates the industrial maintenance report using ReportLab.

The report includes:

- Cover Page
- Executive Summary
- Machine Status
- AI Assessment
- Fault Probability Analysis
- Root Cause Analysis
- Engineering Recommendations
- Sensor Trend Graphs
- End Page

##### 4) anomaly.py

Implements the rule-based anomaly detection engine.

Calculates:

- RMS
- Peak Value
- Machine Status
- Health Score
- Efficiency
- Remaining Useful Life
- Maintenance Recommendation

##### 5) predict.py

Implements the machine learning model that predicts the overall machine condition.

Model Used:
- Random Forest Classifier

Outputs:

- Healthy
- Warning
- Critical

along with prediction confidence.

##### 6) fault_predict.py

Predicts the most probable fault category.

Model Used:
- Random Forest Classifier

Possible outputs:

- Bearing Wear
- Rotor Imbalance
- Shaft Misalignment
- Severe Machine Failure

along with confidence.

##### 7) analysis.py

Processes vibration signals.

Functions include:

- Synthetic vibration signal generation
- Gaussian noise addition
- Signal filtering
- FFT generation
- Graph generation

##### 8) historical.py

Generates historical trend graphs from the stored CSV data.

Creates plots for:

- Temperature
- RMS
- Peak
- Health Score
- Efficiency
- Remaining Useful Life
- Fault Count

##### 9) read_thingspeak.py

Retrieves the latest sensor values from the ThingSpeak cloud using the REST API.

##### 10) cloud.py

Uploads processed machine parameters to ThingSpeak.

Uploads:

- RMS
- Temperature
- Status
- Fault Count
- Health Score
- Efficiency
- Remaining Useful Life
- Peak

##### 11) csv_logger.py

Stores each monitoring cycle into the local CSV database.

This CSV serves as the historical dataset used for:

- Dashboard visualisation
- Trend analysis
- PDF report generation

##### 12) live_sensor.py

Provides live sensor acquisition support.

(Current implementation retrieves data from ThingSpeak.)

##### 13) config.py

Stores configurable project parameters.

Example:

- ThingSpeak API Keys
- Update Interval
- Channel IDs

----------
### Model Development Modules

> These scripts are executed **once during model development** to generate the training dataset and train the machine learning models. They are **not part of the normal runtime workflow**.

##### 1) `generate_dataset.py`

###### Purpose
Generates a synthetic machine condition dataset used for training the machine learning models.

###### Working
- Calls `generate_machine_data()` from `simulator.py`.
- Simulates **Healthy**, **Warning**, and **Critical** machine conditions.
- Processes the generated vibration signal using `anomaly.py`.
- Extracts machine features:
  - Temperature
  - RMS
  - Peak
  - Health Score
  - Efficiency
- Assigns machine status and fault labels.
- Removes contradictory samples (e.g., Healthy fault but Critical status).
- Generates approximately **10,000** samples.

###### Output
```
Dataset/machine_dataset.csv
```

This dataset is used to train both the **Machine Status Prediction Model** and the **Fault Prediction Model**.

##### 2) `simulator.py`

###### Purpose
Creates realistic synthetic machine data representing different industrial operating conditions.

###### Working
Randomly simulates three machine states:

- 🟢 Healthy
- 🟡 Warning
- 🔴 Critical

For each machine state, it generates:

- Temperature
- Vibration amplitude
- Gaussian noise
- Healthy reference signal
- Actual vibration signal

Different mechanical faults are simulated by introducing unique vibration signatures:

- Bearing Wear
- Rotor Imbalance
- Shaft Misalignment
- Severe Machine Failure

Additional sensor spikes are inserted for **Warning** and **Critical** conditions to imitate abnormal industrial machine behaviour.

###### Returns

- Time Vector
- Healthy Signal
- Faulty Signal
- Temperature
- Fault Type

##### 3) `train_model.py`

###### Purpose
Trains the **Machine Health Classification Model**.

###### Input
```
Dataset/machine_dataset.csv
```

###### Features Used
- Temperature
- RMS
- Peak
- Health Score
- Efficiency

###### Target
```
Status
```

Possible outputs:

- HEALTHY
- WARNING
- CRITICAL

###### Algorithm
- Random Forest Classifier

###### Process
- Loads the dataset.
- Splits data into training and testing sets.
- Trains the machine learning model.
- Evaluates model performance.
- Displays:
  - Accuracy
  - Classification Report
  - Confusion Matrix
- Saves the trained model as:

```
python/saved_model.pkl
```

This model is later loaded by **`predict.py`** during runtime to predict the overall machine condition.

##### 4) `train_fault_model.py`

###### Purpose
Trains the **Fault Diagnosis Model**.

###### Input
```
Dataset/machine_dataset.csv
```

###### Features Used
- Temperature
- RMS
- Peak
- Health Score
- Efficiency

###### Target
```
FaultType
```

Possible fault predictions include:

- Healthy
- Bearing Wear
- Rotor Imbalance
- Shaft Misalignment
- Severe Machine Failure

###### Algorithm
- Random Forest Classifier

###### Process
- Loads the dataset.
- Performs train-test split.
- Trains the fault prediction model.
- Evaluates model performance.
- Displays:
  - Accuracy
  - Classification Report
  - Confusion Matrix
- Saves the trained model as:

```
python/fault_model.pkl
```

This model is later loaded by **`fault_predict.py`** during runtime to perform real-time fault diagnosis.

#### Model Development Workflow
```
simulator.py
        │
        ▼
generatedataset.py
        │
        ▼
machine_dataset.csv
        │
        ├──────────────► train_model.py
        │                     │
        │                     ▼
        │              saved_model.pkl
        │
        └──────────────► train_fault_model.py
                              │
                              ▼
                       fault_model.pkl

```

--------
### Execution Sequence
##### Step 1

Run the ESP32 simulation in Wokwi.
```
https://wokwi.com/projects/469505239406401537
```

##### Step 2

The ESP32 uploads sensor readings to ThingSpeak.
```
https://thingspeak.mathworks.com/channels/3426878/private_show
```

##### Step 3

Run:

```
python main.py
```

This will:

- Read sensor data
- Analyze machine health
- Predict faults
- Update cloud data
- Save logs
- Generate graphs
  
##### Step 4

Open the dashboard:

```
streamlit run dashboard.py
```

The dashboard displays:

- Real-time machine condition
- Historical trends
- AI prediction
- Fault analysis
- Machine health indicators

##### Step 5

Click Generate PDF Report from the dashboard to download a complete industrial maintenance report.

### Project Workflow
```
Wokwi ESP32 Simulation
            │
            ▼
     ThingSpeak Cloud
            │
            ▼
   read_thingspeak.py
            │
            ▼
        main.py
            │
 ┌──────────┼──────────┐
 ▼          ▼          ▼
Signal   Rule-Based    ML Models
Processing Detection
 │          │          │
 └──────────┼──────────┘
            ▼
     Health Assessment
            │
 ┌──────────┼──────────┐
 ▼          ▼          ▼
CSV Log   ThingSpeak   Graphs
            │
            ▼
      Streamlit Dashboard
            │
            ▼
      PDF Report Generator
```
