# TravelCopilot

## Introduction

This is a travel recommendation system based on **Yelp**. Based on the cities and dates selected by the user, personalized attractions, hotels and restaurants are recommended. The models used by the recommendation algorithm are **SVD** and **Light-GCN**. And use **pywebio** to implement web UI and user interaction.

## Display of results

Click  [here](doc/TravelCopilot.pdf)  to view the results of a full run.

## Document description

```
.
├── Readme.md															
# this file 
├── code																	
# code directory
│   ├── Data Processing and Analysis										
# data processing and analysis
│   │   ├── Data_Load_And_Cleaning_Business.ipynb						
# data cleaning and processing of business data
│   │   ├── Data_Load_And_Cleaning_Review.ipynb							
# data cleaning and processing of review data
│   │   ├── loading-yelp-json-data-and-visualization.ipynb				
# data loading and visualization
│   │   ├── nohup.out													
# log file for a training process
│   │   ├── mkyelp2018.py												
# data processing for Light-GCN												
│   │   └── plot.ipynb													
# data visualization for log file
│   ├── Procedure.py														
# test and train function
│   ├── TravelCopilot.py													
# TravelCopilot system entrance
│   ├── checkpoints														
# model checkpoints directory
│   │   └── lgn-yelp2018-3-64.pth.tar									
│   ├── dataloader.py														
# dataloader in yelp		
│   ├── filter.py															
# filter function for business data
│   ├── generate_guide.py													
# generate guide function
│   ├── idIndex.py															
# idIndex function for business ID and business number in Light-GCN
│   ├── model.py															
# model definition
│   ├── parse.py															
# parse function 
│   ├── rcmdweb.py															
# web UI and user interaction
│   ├── recommendation.py													
# recommendation function for tour, hotel and restaurant
│   ├── register.py															
# register function 
│   ├── train.py															
# train function
│   ├── utils.py															
# utils function
│   └── world.py															
# world function 
├── data																
# data directory for Light-GCN	
│   └── yelp2018															
# data directory for yelp
│       ├── item_list.txt													
# business Id and business number
│       ├── s_pre_adj_mat.npz												
# pre-processed adjacency matrix
│       ├── test.txt														
# test data
│       ├── train.txt														
# train data
│       └── user_list.txt													
# user Id and user number				
├── doc																	
# document directory
│   ├── TravelCopilot.pdf												
# results of a full run
│   ├── TravelCopilot.pptx													
# ppt of TravelCopilot				
│   └── report.pdf															
# report of TravelCopilot		
├── output_csv															
# data directory for SVD		
│   ├── business_PA_Philly_clean.csv										
# business data after cleaning	
│   ├── business_PA_Philly_clean_tour.csv									
# business data after cleaning and filtering	
│   ├── review_PA_Philly_clean.csv											
# review data after cleaning
│   └── review_PA_Philly_clean_tour.csv										
# review data after cleaning and filtering
└── yelp_dataset														
# original yelp2023 data directory
    ├── Dataset_User_Agreement.pdf										    
    ├── yelp_academic_dataset_business.json	
    ├── yelp_academic_dataset_checkin.json	
    ├── yelp_academic_dataset_review.json	
    ├── yelp_academic_dataset_tip.json	
    └── yelp_academic_dataset_user.json	
```

## Train your own model

train LightGCN on Yelp dataset:

- command

```shell
 cd code && python train.py --decay=1e-4 --lr=0.001 --layer=3 --seed=2020 --dataset="Yelp2018" --topks="[20]" --recdim=64
```

## Run TravelCopilot

- command

```shell
cd code && TravelCopilot.py	
```

### Reference

>  https://github.com/gusye1234/LightGCN-PyTorch
