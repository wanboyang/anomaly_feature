#!/bin/bash 
#python3 feature_extract.py --dataset Avenue --snapshot ./model/c3d/c3d.pickle --datamodal rgb --modelName c3d --fc_layer fc6
#python3 feature_extract.py --dataset Avenue --snapshot ./model/c3d/c3d.pickle --datamodal rgb --modelName c3d --fc_layer fc7
#python3 feature_extract.py --dataset UCSDPed2 --snapshot ./model/c3d/c3d.pickle --datamodal rgb --modelName c3d --fc_layer fc6
#python3 feature_extract.py --dataset UCSDPed2 --snapshot ./model/c3d/c3d.pickle --datamodal rgb --modelName c3d --fc_layer fc7
#python3 feature_extract.py --dataset shanghaitech --snapshot ./model/c3d/c3d.pickle --datamodal rgb --modelName c3d --fc_layer fc6
#python3 feature_extract.py --dataset shanghaitech --snapshot ./model/c3d/c3d.pickle --datamodal rgb --modelName c3d --fc_layer fc7
#python3 dataset_creater_C3D.py --dataset Avenue
#python3 dataset_creater_C3D.py --dataset UCSDPed2
#python3 dataset_creater_C3D.py --dataset shanghaitech
#python3 feature_extract.py --dataset UCF_Crime --snapshot ./model/c3d/c3d.pickle --datamodal rgb --modelName c3d --fc_layer fc6
#python3 feature_extract.py --dataset UCF_Crime --snapshot ./model/c3d/c3d.pickle --datamodal rgb --modelName c3d --fc_layer fc7
python3 dataset_creater_C3D.py --dataset UCF_Crime

#python3 feature_extract.py --dataset UCSD/UCSDPed2 --snapshot ./model/i3d/i3d_model_weight/model_kinetics_flow.pth --datamodal flow
#python3 feature_extract.py --dataset UCSD/UCSDPed2 --snapshot ./model/i3d/i3d_model_weight/model_kinetics_rgb.pth --datamodal rgb
