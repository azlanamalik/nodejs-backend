

#work 1 at a time as we noise/denoise coinstantly hence worth to have 1 image at a time
import os
import cv2 as cv
import random as rand
import sys
import numpy as np
class getting_batches:
    def __init__(self):
        pass
    def get_pairs(self,path):
        img = self.load_img_grey_scaled(path)
        return img

    def load_img_grey_scaled(self, path):
        img = cv.imread(path) 
        if img is None:
            sys.exit("Could not read the image.")
        img = img.astype(np.float32) / 255.0
        return img




class diffusion_model:
    def __init__(self):
        self.T = 90  # Total diffusion steps
        self.betas = self.linear_beta_schedule(timesteps=self.T)
        self.alphas = 1.0 - np.array(self.betas)
        self.alphas_cumprod = self.cumulative_prod(self.alphas)
        self.sigmas = [beta**0.5 for beta in self.betas]

        self.dense_weights = None
        self.dense_bias = None


    def cumulative_prod(self,arr):
        output = []
        prod = 1.0 #init as 1 but doesnt matter as 1.0 or 1 as python is dynamic lang
        for val in arr:
            prod *= val
            output.append(prod)
        return output
    def linear_beta_schedule(self,timesteps):
        """choosing any random linear beta start and end can tune this later"""
        beta_start = 0.0001
        beta_end = 0.02
        beta = []
        for i in range(timesteps):
            beta.append(beta_start + i * (beta_end - beta_start) / (timesteps - 1))
        return beta
    def forward_pass(self,img,noise_level=0.1):
        self.x_t_list = []
        self.noise1 = self.get_noise(img.shape)
        x_tPREV = img
        self.eps_list = [] 
        ##adding noise
        for t in range(1, self.T):
            noise = self.get_noise(img.shape)
            x_t = ((1 - self.betas[t])**0.5) * x_tPREV + (self.betas[t]**0.5) * noise
            self.x_t_list.append(x_t)
            self.eps_list.append(noise)
            x_tPREV = x_t
        self.print_img(x_t)
        return self.x_t_list[-1]

    def print_img(self,img):
        img = np.clip(img * 255.0, 0, 255).astype(np.uint8)
        cv.imshow("image", img)
        cv.waitKey(0)
        cv.destroyAllWindows()


    def get_noise(self,shape):
        return np.random.normal(size=shape).astype(np.float32)
    def reverse_pass(self,noised_img):
        x = noised_img
        alpha_x = self.alphas[1]
        alpha_bar_x = alpha_x
        sigma_x = self.betas[1] ** 0.5
        z_x = self.build_0_matrix(x.shape)
        for t in range(0, self.T - 1):
            eps_theta = self.model(x, t, self.eps_list[t], error_scale=0.1)
            x_0_hat = 1 / np.sqrt(alpha_x) * (x - (1 - alpha_x) / np.sqrt(1 - alpha_bar_x) * eps_theta) + sigma_x * z_x
            x = x_0_hat
            alpha_x = self.alphas[t]
            alpha_bar_x = alpha_x
            sigma_x = self.betas[t] ** 0.5
            z_x = self.build_0_matrix(x.shape)#should stay the same but keep just incase
        self.print_img(x_0_hat)

    def model(self, x_t, t, true_eps, error_scale=0.1):
        return true_eps + error_scale * np.random.randn(*x_t.shape)
    def build_0_matrix(self,shape):
        return np.zeros(shape, dtype=np.float32)







def main():
    path = "C:\\Users\\Azlan\\OneDrive\\Pictures\\Screenshots\\Screenshot 2025-09-15 131423.png"
    data_loader = getting_batches()
    img = data_loader.get_pairs(path)
    print("here")
    model = diffusion_model()
    noised_images = model.forward_pass(img)
    print("here")
    model.reverse_pass(noised_images)

main()