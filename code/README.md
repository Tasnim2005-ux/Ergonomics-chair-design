🪑 Anthropometric Data-Based Ergonomic Classroom Chair Design
📌 Project Overview

This project focuses on the data-driven ergonomic design of classroom chairs using anthropometric measurements collected from university students.

The primary objective is to investigate whether a classroom chair can be designed systematically from the physical dimensions of its intended users rather than relying only on conventional or manually selected chair dimensions.

Anthropometric data from male and female participants are collected, cleaned, statistically analyzed, and converted into engineering design dimensions using percentile-based ergonomic design principles.

The project currently develops two separate preliminary chair dimension sets:

Male Classroom Chair
Female Classroom Chair

The calculated dimensions are presented through an interactive Python + Streamlit dashboard. The next stage of the project is to convert these calculated dimensions into detailed 3D chair models using SolidWorks, followed by ergonomic and practical design evaluation.

🎯 Why Are We Designing the Chair?

Classroom furniture is used for long periods of sitting, yet chair dimensions are often selected using fixed standard dimensions or commercially available designs.

However, people within the same population do not have identical body dimensions.

For example, differences in:

Popliteal Height
Buttock-Popliteal Length
Hip Breadth
Sitting Shoulder Height
Sitting Knee Height
Thigh Clearance
Buttock-Knee Length
Foot Length

can influence how a person interacts with a chair.

Therefore, this project follows a user-centered, anthropometric approach, where the dimensions of the chair are derived from the measured dimensions of the intended user population.

The central idea of the project is:

Human Body Dimensions
        ↓
Anthropometric Data
        ↓
Statistical Analysis
        ↓
Percentile Analysis
        ↓
Ergonomic Design Rules
        ↓
Chair Dimensions
        ↓
3D CAD Design
        ↓
Prototype / Ergonomic Validation
👥 Target Users

The current study focuses on university-level students and considers male and female anthropometric groups separately.

Separate datasets are used because the collected anthropometric distributions differ between the two groups. Rather than forcing both datasets into one identical calculation, the project generates separate preliminary dimensional requirements for each group.

The current dataset contains:

Group	Valid Participants
Male	204
Female	203
Total	407
📏 Anthropometric Data Collection
How Was the Data Collected?

Anthropometric measurements were collected from participants using standardized measurement procedures.

During measurement:

Participants removed their shoes.
Participants maintained an upright sitting posture.
Relevant joints were positioned according to the measurement procedure.
Measurements were taken with the participant wearing relatively thin clothing.
Measurements were recorded systematically for subsequent statistical analysis.

The purpose of following a consistent measurement procedure is to reduce unnecessary variation caused by posture, footwear, or measurement conditions.

📊 Measurements Collected

The current dataset contains eight primary anthropometric measurements.

Measurement	Abbreviation	Unit	Design Relevance
Popliteal Height	PH	cm	Seat height
Buttock-Popliteal Length	BPL	cm	Seat depth
Hip Breadth	HB	cm	Seat width
Sitting Shoulder Height	SSH	cm	Backrest height
Sitting Knee Height	SKH	cm	Knee/leg clearance
Thigh Clearance	TC	cm	Under-seat/desk clearance
Buttock-Knee Length	BKL	cm	Leg-space validation
Foot Length	FL	cm	Foot placement

These measurements were selected because they represent important body dimensions that interact with the major geometric features of a classroom chair.

🧹 Data Processing and Cleaning

The raw data are stored separately in Excel files:

data/
├── male.xlsx
└── female.xlsx

The Python application performs the main data-processing operations automatically.

The processing workflow includes:

Excel Dataset
      ↓
Column Name Cleaning
      ↓
Data Type Conversion
      ↓
Missing Data Detection
      ↓
Invalid / Incomplete Row Exclusion
      ↓
Validated Dataset
      ↓
Statistical Analysis

This approach allows the calculations to be reproduced automatically rather than manually calculating every parameter in Excel.

The current validated dataset contains:

204 male observations
203 female observations
407 observations in total
📈 Statistical Analysis

After data cleaning, the project calculates descriptive statistics for every anthropometric measurement.

The following parameters are calculated:

Minimum
Maximum
Mean
Median
Standard Deviation
Variance
5th Percentile (P5)
25th Percentile (P25)
50th Percentile (P50)
75th Percentile (P75)
95th Percentile (P95)

The percentile analysis is particularly important because different chair dimensions require different portions of the user population to be accommodated.

📐 Why Percentiles Are Used

A single average body dimension cannot adequately represent the full range of body sizes within a population.

For ergonomic design, different dimensions are therefore associated with different percentile requirements.

For example:

A smaller user may need to be accommodated when determining seat height.
A larger user may need to be accommodated when determining seat width.
A central population value may be used for certain back-support dimensions.

Therefore, this project uses P5, P50, and P95 according to the design requirements.

🪑 Anthropometric Design Rules

The preliminary chair dimensions are calculated using the following design rules.

1. Seat Height

Seat height is based on the 5th percentile Popliteal Height.

Seat Height = P5 Popliteal Height − 2 cm

The subtraction is used as an adjustment based on the design rule adopted for this project.

2. Seat Depth

Seat depth is based on the 5th percentile Buttock-Popliteal Length.

Seat Depth = P5 BPL − 3 cm

The clearance is intended to prevent excessive forward extension of the seat pan relative to the user's lower leg region.

3. Seat Width

Seat width is based on the 95th percentile Hip Breadth.

Seat Width = P95 Hip Breadth + 2–3 cm

Using the upper percentile for hip breadth allows the design to account for users with larger hip breadth.

4. Backrest Height

Backrest height is based on the 50th percentile Sitting Shoulder Height.

Backrest Height = P50 Sitting Shoulder Height

This provides a central reference dimension for the preliminary backrest design.

🧮 Preliminary Design Results

Based on the current anthropometric datasets and the above design rules, the system generates the following preliminary dimensions.

Male Chair
Design Parameter	Preliminary Dimension
Seat Height	39.90 cm / 399 mm
Seat Depth	41.00 cm / 410 mm
Seat Width	39.30–40.30 cm / 393–403 mm
Backrest Height	59.90 cm / 599 mm
Female Chair
Design Parameter	Preliminary Dimension
Seat Height	36.70 cm / 367 mm
Seat Depth	37.60 cm / 376 mm
Seat Width	37.80–38.80 cm / 378–388 mm
Backrest Height	55.90 cm / 559 mm

These values are automatically generated from the anthropometric datasets rather than being manually entered into the application.

Important: These are preliminary anthropometric design dimensions. They are not presented as final manufacturing dimensions until CAD modeling, practical design review, prototype development, and ergonomic validation are completed.

💻 Interactive Streamlit Dashboard

The complete analysis is implemented as an interactive Streamlit dashboard.

The dashboard allows a user or researcher to explore the anthropometric data and design outputs without directly interacting with the Python code.

Dashboard Architecture
                    STREAMLIT DASHBOARD
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
     Dataset            Analysis           Design
        │                  │                  │
        ↓                  ↓                  ↓
 Male / Female      Statistics &        Male Chair
 Data Analysis      Percentiles         Female Chair
        │                  │                  │
        └──────────────────┼──────────────────┘
                           ↓
                  Final Design Summary
🖥️ Dashboard Sections
1. Overview

Provides a general introduction to the project, dataset, and ergonomic design objective.

2. Descriptive Statistics

This section allows the user to select either the male or female dataset and view:

Minimum
Maximum
Mean
Median
Standard Deviation
Variance
P5
P25
P50
P75
P95

It also provides additional visualization for selected anthropometric measurements.

3. Percentile Analysis

This section allows users to select an anthropometric measurement and inspect its percentile distribution.

The dashboard displays:

P5
P25
P50
P75
P95

The section also explains how the selected measurement contributes to chair design.

For example:

Popliteal Height
       ↓
      P5
       ↓
Seat Height
4. Male vs Female Comparison

The dashboard provides direct comparison between male and female anthropometric measurements.

Users can compare:

Mean
P5
P50
P95

for each measurement.

This makes it possible to visually investigate dimensional differences between the two datasets.

5. Male Chair Design

This section automatically calculates the preliminary male chair dimensions using the male anthropometric statistics.

The dashboard displays:

P5 Popliteal Height
P5 Buttock-Popliteal Length
P95 Hip Breadth
P50 Sitting Shoulder Height
Design formulas
Final calculated dimensions
Dimensions in cm and mm
6. Female Chair Design

This section performs the same design calculation using the female anthropometric dataset.

The resulting dimensions are presented independently from the male chair design.

7. Final Design Summary

The final dashboard page combines the outputs of both designs into one engineering summary.

It presents:

Male chair dimensions
Female chair dimensions
Anthropometric parameters used
Percentiles used
Design formulas
Male–female dimensional comparison
Additional ergonomic considerations

This section is intended to provide a quick reference before moving to the CAD design stage.

🧩 Additional Anthropometric Considerations

Not every collected measurement directly determines one of the four primary chair dimensions.

However, the remaining measurements are important for subsequent design validation.

Measurement	Application
Sitting Knee Height	Knee and lower-leg clearance
Thigh Clearance	Clearance beneath desk/seat structure
Buttock-Knee Length	Leg-space validation
Foot Length	Foot placement and floor contact

These parameters will become particularly important when the chair is evaluated together with a classroom desk.

🚫 Armrest Design

The current chair concept is a classroom chair without armrests.

Therefore, Elbow Rest Height is not used as a primary design parameter in the current chair geometry.

The design instead focuses on:

Seat
├── Seat Height
├── Seat Depth
├── Seat Width
└── Backrest
    └── Backrest Height

This keeps the current design focused on the major anthropometric requirements of a classroom seating system.

🧰 Next Stage — SolidWorks CAD Design

The next major stage of the project is to convert the calculated anthropometric dimensions into detailed 3D CAD models using SolidWorks.

Two separate chair models will be developed:

Anthropometric Analysis
        ↓
Male Design Dimensions
        ↓
SolidWorks
        ↓
Male Chair 3D Model


Anthropometric Analysis
        ↓
Female Design Dimensions
        ↓
SolidWorks
        ↓
Female Chair 3D Model

The CAD stage will allow the calculated dimensions to be translated into an actual engineering product concept.

The SolidWorks models will consider additional geometric features such as:

Seat geometry
Backrest geometry
Structural frame
Seat thickness
Backrest thickness
Support members
Connection points
Overall chair proportions
Classroom usability

The exact structural dimensions will be finalized during the CAD development stage rather than being assumed from the anthropometric calculations alone.

🔬 From Data Analysis to Physical Design

The complete project is intended to progress through the following stages:

Stage 1 — Data Collection

Collect anthropometric measurements from the target population.

Stage 2 — Data Processing

Clean and validate the collected datasets using Python.

Stage 3 — Statistical Analysis

Calculate descriptive statistics and percentile distributions.

Stage 4 — Ergonomic Dimension Calculation

Apply percentile-based design rules to obtain preliminary chair dimensions.

Stage 5 — CAD Modeling

Develop separate male and female chair models using SolidWorks.

Stage 6 — Design Evaluation

Evaluate the proposed chair designs based on anthropometric compatibility, posture, clearance, proportions, and practical classroom requirements.

Stage 7 — Prototype Development

A future prototype can be developed to evaluate the practical usability and comfort of the proposed dimensions.

🛠️ Technologies Used
Programming & Data Analysis
Python
Pandas
NumPy
Dashboard
Streamlit
Data Storage
Microsoft Excel
OpenPyXL
CAD Design
SolidWorks (planned next stage)
Engineering Methods
Anthropometry
Descriptive Statistics
Percentile Analysis
Ergonomic Design
Data-Driven Product Design
📁 Project Structure
ergonomics chair design/
│
├── data/
│   ├── male.xlsx
│   └── female.xlsx
│
├── code/
│   └── app.py
│
├── .gitignore
│
└── README.md
▶️ How to Run the Dashboard
1. Clone the repository
git clone <YOUR_GITHUB_REPOSITORY_URL>
2. Open the project directory
cd "ergonomics chair design"
3. Install the required Python packages
py -m pip install pandas numpy streamlit openpyxl
4. Run the Streamlit application
py -m streamlit run code/app.py

The Streamlit dashboard will then open in the browser.

📌 Key Contribution of the Project

The main contribution of this project is the integration of anthropometric data analysis and engineering chair design into a single reproducible workflow.

Instead of treating anthropometric analysis and product design as separate activities, the project connects them:

Real Human Measurements
          ↓
Data Processing
          ↓
Statistical Evidence
          ↓
Percentile Selection
          ↓
Engineering Design Rules
          ↓
Chair Dimensions
          ↓
CAD Model
          ↓
Future Prototype

This creates a traceable relationship between the measured characteristics of the target users and the dimensions of the proposed chair.

🚀 Future Development

Future development of the project may include:

Complete SolidWorks 3D modeling
Detailed engineering drawings
Material and structural design
Chair–desk compatibility analysis
Ergonomic posture assessment
Prototype fabrication
User comfort evaluation
Additional statistical data-quality analysis
Validation with a larger participant population
Iterative redesign based on prototype feedback
👨‍💻 Authors
Tasnim Bin Nasim

Department of Industrial & Production Engineering
Jashore University of Science and Technology (JUST)

MD Raisul Islam

Department of Industrial & Production Engineering
Jashore University of Science and Technology (JUST)

📜 Project Status

Current Status:

✅ Anthropometric Data Collection
✅ Data Cleaning
✅ Statistical Analysis
✅ Percentile Analysis
✅ Male–Female Comparison
✅ Preliminary Chair Dimension Calculation
✅ Interactive Streamlit Dashboard
🔄 SolidWorks 3D Modeling
🔜 Engineering Drawing
🔜 Prototype Development
🔜 Ergonomic Validation
⭐ Final Perspective

This project aims to demonstrate how Industrial Engineering, Ergonomics, Anthropometry, Statistical Analysis, Data Science, and CAD Design can be integrated to develop a data-driven classroom seating solution.

The final goal is not simply to calculate anthropometric statistics, but to transform measured human dimensions into an engineering design that can be modeled, evaluated, and eventually validated through a physical prototype.