from methods import data_handler, gradcam, LRP, SHAP, lime, integrated_gradients, confidence_scores
import models
import argparse
import numpy as np
import cv2
import matplotlib.pyplot as plt
import os
import torch
from datetime import datetime
import random


# TODO gradcam

def main():
    parser = argparse.ArgumentParser(description='run explain methods')
    parser.add_argument('--VGG', type=bool, default=True)
    parser.add_argument('--AlexNet', type=bool, default=True)
    parser.add_argument('--LRP', type=bool, default=False)
    parser.add_argument('--gradCam', type=bool, default=False)
    parser.add_argument('--Lime', type=bool, default=True)
    parser.add_argument('--CEM', type=bool, default=False)
    parser.add_argument('--SHAP', type=bool, default=False)
    parser.add_argument('--num_images', type=int, default=4)
    parser.add_argument('--img_folder', type=str, default='./data/')
    args = parser.parse_args()

    # define models
    models_list = []
    if args.VGG:
        vgg = models.Vgg16()
        models_list.append(vgg)
    if args.AlexNet:
        alex = models.AlexNet()
        models_list.append(alex)

    # import image
    data = data_handler.get_image(args.img_folder)
    files = data_handler.get_files(args.img_folder)
    files.sort()
    labels = data_handler.get_labels()

    """
    for i in range(args.num_images):
        img, _ = next(data)

        #org_img = np.array(cv2.imread(args.img_folder + "images/" + files[i]))
        #org_img = np.asarray(cv2.resize(org_img, (224, 224), interpolation=cv2.INTER_CUBIC), dtype=np.float32)
        #org_img = cv2.cvtColor(org_img, cv2.COLOR_BGR2RGB)
    """
        #img_org_np, img_prep_torch, img_name, img_true_label_str = data_handler.get_question_image(
            #r'C:\Users\rfroe\OneDrive\Documents\Uni\SOSE22\PJ DS\development\data2\imagenetv2-matched-frequency-format-val',
            #1,
            #labels)
    """
        for model in models_list:
            # LRP.explain(model.model,img, files[i], model.name)
            gradcam.explain(model.model, img_prep_torch, img_org_np)
            # SHAP.explain(model.model, img, org_img, files[i], labels, model.name)

            # model_dict = dict(type=model.name, arch=model.model, layer_name=model.ce_layer_name, input_size=(224, 224))
            # ce = contrastive_explanation.ContrastiveExplainer(model_dict)
            # # Choice of contrast; The Q in `Why P, rather than Q?'. Class 130 is flamingo
            # ce.explain(org_img, img, 130, f"./results/ContrastiveExplanation/{model.name}_{files[i]}")

            # TODO Adjust this a bit so we dont initilize the model eight times only two
            # lime_ex = lime.LIMEExplainer(model)
            # lime_ex.explain(img, files[i])

    """

    
    # load questionaire_list from .json or .pickle
    questionaires_list = data_handler.get_questionaires("data2/questionaires.pickle")

    # create root folder for questionaires
    current_dir = os.getcwd()
    folder_path = os.path.join(current_dir, f"questionaire_forms_{datetime.now().strftime('%d-%m_%H-%M')}")
    if not os.path.exists(folder_path):
            os.mkdir(folder_path)

    
    # create all questionaires according to questionares_list
    for idx, questionaire in enumerate(questionaires_list):
        sub_folder_path = os.path.join(folder_path, f"questionaire_{idx+1}")
        if not os.path.exists(sub_folder_path):
            os.mkdir(sub_folder_path)

        # create questionaire_n subfolders
        for qu_idx, question in enumerate(questionaire):

            # load image by index

            img_idx, model_name_used, xai_used, bool_used  = question

            model_used = models.Vgg16() if model_name_used == "vgg" else models.AlexNet()
            model_used.train()

            img_org_np, img_prep_torch, img_name, img_true_label_str = data_handler.get_question_image(
                r'/Users/tobiaslabarta/Downloads/imagenetv2-matched-frequency-format-val',
                img_idx,
                labels)

            if xai_used == "gradCAM":
                fig_explanation = gradcam.explain(model_used.model, img_prep_torch, img_org_np)
            elif xai_used == "LRP":
                fig_explanation = LRP.explain(model_used.model, img_prep_torch, img_name, model_used.name)
            elif xai_used == "LIME":
                lime_ex = lime.LIMEExplainer(model_used)
                fig_explanation = lime_ex.explain(img_org_np)
            elif xai_used == "SHAP":
                fig_explanation = SHAP.explain(model_used.model, img_prep_torch, img_org_np, labels)
            elif xai_used == "IntegratedGradients":
                ige = integrated_gradients.IntegratedGradientsExplainer(model_used)
                fig_explanation = ige.explain(img_prep_torch)
            elif xai_used == "ConfidenceScores":
                fig_explanation = confidence_scores.explain(model_used, img_prep_torch, labels, 3)
            
            
            # save explanation and original image for current question in appropriate questionaire folder
            fig_explanation.savefig(os.path.join(sub_folder_path, f"{qu_idx+1}_{model_name_used}_{bool_used}_{xai_used}_{img_name}"))
            
            fig_org = data_handler.get_figure_from_img_array(img_org_np[0], f"True class: {img_true_label_str}")
            fig_org.savefig(os.path.join(sub_folder_path, f"{qu_idx+1}_org_{img_name}"))





if __name__ == '__main__':
    main()