#!/bin/bash 
#python3 feature_extract.py --dataset UCF_Crime --snapshot ./model/i3d/i3d_model_weight/model_kinetics_rgb.pth --datamodal rgb --modelName i3d
#python3 feature_extract.py --dataset UCF_Crime --snapshot ./model/i3d/i3d_model_weight/model_kinetics_flow.pth --datamodal flow --modelName i3d
python3 dataset_creater.py --dataset UCF_Crime


#python3 feature_extract.py --dataset UCSD/UCSDPed2 --snapshot ./model/i3d/i3d_model_weight/model_kinetics_flow.pth --datamodal flow
#python3 feature_extract.py --dataset UCSD/UCSDPed2 --snapshot ./model/i3d/i3d_model_weight/model_kinetics_rgb.pth --datamodal rgb
