from PIL import Image
import numpy as np


##this is an edited verison of the cnn model
##pixel cnn is completely different to normal cnn however i can still use certain classes to save time



#current assumption is that all images are black and white so can take single values from RGB as black to white share same RGB can change this easily later
class layer0 :
    def forward_propogation(self,image_path,image_set = None):
        if image_set != None:
            self.output = image_set
        else:
            self.output =  self.image_to_pixel_val(image_path)
        self.image_width , self.image_height = self.image_MetaData(image_path)
    def image_MetaData(self,image_path):
        image = Image.open(image_path)
        image_width = image.width
        image_height = image.height
        return image_width , image_height


    def image_to_pixel_val(self,image_path):
        image = Image.open(image_path).convert('L')
        image = np.asarray(image)
        return image







class 



class Convolutional_Layer():
    def __init__(self,prev_layer = None,dim = 3,bias = 0 , kernal = [[10,10,10],[10,10,10],[10,10,10]]):
        self.prev_layer = prev_layer
        #passing class layer0 wont be demanding as its pass by reference
        self.dim = dim
        self.kernal = kernal
        self.bias = bias
    def forward_propogation(self,prev_layer):
        self.prev_layer = prev_layer
        self.output = self.relu(self.get_sample_from_image(self.prev_layer))

        self.image_width , self.image_height = self.image_metadata()
    def relu(self,input):
        return np.maximum(0,input)

    def image_metadata(self):
        #for the next layers kernal restrictions
        try:
            width = len(self.output[0])
        except:
            raise Exception("there has been an issue with the output in layer 1,specifically with the output (caught in image_metadata method)")
        return int(width) , int(len(self.output))
   
    def get_sample_from_image(self,prev_layer):
        #lets say we do a 1 3x3 kernal(later we can create instances with random values as kernals)
        #implimentation will be top upper left will be the first and we will calculate from that
        #careful of boundaries
        top_left = [0,0]
        min_sample = [] #allows for 2d array so can easily to a matrix multiplication
        sample = []
        try:
            x = prev_layer.image_height
        except:
            raise Exception(prev_layer)
        output = 0
        output_matrix = []
        #cross corrolation
        for y in range(top_left[0], prev_layer.image_height - self.dim + 1):  # y-direction (rows)
            output_row = []
            for x in range(top_left[1], prev_layer.image_width - self.dim + 1):  # x-direction (columns)
                sample = []
                for i in range(self.dim):
                    row = []
                    for j in range(self.dim):
                        row.append(float(prev_layer.output[y + i][x + j]))
                    sample.append(row)
                sample = np.array(sample)
                output = (np.sum(sample * self.kernal)) + self.bias
                output_row.append(float(output))#was getting logic errors before
            output_matrix.append(output_row)
        #self.show_image_of_layer(output_matrix) #this just shows the output visually
        return np.array(output_matrix)
    def show_image_of_layer(self,output_matrix):
        #fun little method that will allow me to see the output image of each layer to see how and what the neural network is doing
        # Normalize output_matrix to 0–255
        output_array = np.array(output_matrix, dtype=np.float32)
        output_array = output_array - output_array.min()
        #self.Pixel_to_image(output_array)


    def Pixel_to_image(self,output_array):
        if output_array.max() > 0:
            output_array = output_array / output_array.max()
        output_array = (output_array * 255).astype(np.uint8)
        rgb_image = np.stack([output_array]*3, axis=-1)  # shape: (height, width, 3)


        # Create image and display
        img = Image.fromarray(rgb_image, mode='RGB')
        img.show()
    def RELU(self,input):
        return np.maximum(0,input)
    def backward_propogation(self,dL_da,learning_rate = 0.002):
        print(dL_da)
        #key - even though last layer will still need to return output as if i add 2/3 conv layers (which is common) it needs to be able to process it
        dL_dz = dL_da * (self.output > 0).astype(float)
        dL_dW = np.zeros_like(self.kernal, dtype=float)
        input_data = self.prev_layer.output
        for y in range(dL_dz.shape[0]):
            for x in range(dL_dz.shape[1]):
                sample = []
                for i in range(self.dim):
                    row = []
                    for j in range(self.dim):
                        row.append(int(input_data[y+i][x+j]))
                    sample.append(row)
                sample = np.array(sample)
                dL_dW += dL_dz[y, x] * sample
        
        # Rotate kernel by 180 degrees for backpropagation
        rot_kernel = np.rot90(self.kernal, 2)
        #kernel update
        self.kernal -= learning_rate * dL_dW


        # dL/dI
        dL_dI = np.zeros_like(input_data, dtype=float)
        for y in range(dL_dI.shape[0] - self.dim + 1):
            for x in range(dL_dI.shape[1] - self.dim + 1):
                for i in range(self.dim):
                    for j in range(self.dim):
                        dL_dI[y+i, x+j] += dL_dz[y, x] * rot_kernel[i, j]
        print(self.kernal)
        return dL_dI









input_layer = layer0()
layers = [
    Convolutional_Layer(prev_layer=input_layer, dim=3, bias=0)
]


def run_pipeline(image_path):
    input_layer.forward_propogation(image_path)
    prev_layer = input_layer
    for layer in layers:
        layer.forward_propogation(prev_layer)
        prev_layer = layer
    return prev_layer.output




output = run_pipeline(r'C:\Users\Azlan\OneDrive\Desktop\StockAnalysisTool\trianing_dat.jpg')