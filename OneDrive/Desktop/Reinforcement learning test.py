import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim

class create_environment():
    def __init__(self,dim_x : int,dim_y : int) -> None:
        self.running = True
        self.board = self.init_board(dim_x ,dim_y)#2d array with all the co-ordinates if i want to create a diagram in future
        self.player_pos = [0,0]
        # have values of 0 and 1  to show where the object is
        self.dim_x = dim_x
        self.dim_y = dim_y
        self.init_pos = self.init_position()
        self.target_pos = [dim_x,dim_y]

    def init_board(self,dim_x : int,dim_y : int):
        full = []
        row = []
        for x in range(0,dim_x):
            for y in range(0,dim_y):
                row.append(0)
            full.append(row)#creates 2D array
        return full
    
    def init_position(self,init_pos = [5,5]):
        '''allows for adaptive starting positions'''
        self.player_pos = init_pos

    def move(self,movement : str):
        '''takes input of "up","down","left","right" and moves the char on the board '''
        if (movement not in ["up","down","left","right"]):
            print("failed")
            raise Exception ("model has given an invalid response please rename dat")
        
        if (movement == "up"):
            temp = self.player_pos[1] + 1
            if (temp < self.dim_y):
                self.player_pos[1] = temp
            else:
                print("OoB - Cannot move up")
                self.running = False
                return "OoB"
        elif (movement == "down"):
            temp = self.player_pos[1] - 1
            if (temp >= 0):
                self.player_pos[1] = temp
            else:
                print("OoB - Cannot move down")
                self.running = False
                return "OoB"
        elif (movement == "right"):
            temp = self.player_pos[0] + 1
            if (temp < self.dim_x):
                self.player_pos[0] = temp
            else:
                print("OoB - Cannot move right")
                self.running = False
                return "OoB"
        elif (movement == "left"):
            temp = self.player_pos[0] - 1
            if (temp >= 0):
                self.player_pos[0] = temp
            else:
                print("OoB - Cannot move left")
                self.running = False
                return "OoB"
        
    def play_game(self,movement :str):
        if self.running == True:
            result = self.move(movement)
            return result
        else:
            print("Game is stopped - out of bounds")
            return "OoB"



    def Testing_movement(self):
        '''for testing purposes only'''
        print(self.player_pos)
        print(self.board)
        print("Current Player Position: ", self.player_pos)
        for i in range(0,3):
            if (self.play_game("up") == "OoB"):
                break
            print(self.player_pos)
        for i in range(0,2):
            if (self.play_game("down") == "OoB"):
                break
            print(self.player_pos)
        for i in range(0,2):
            if (self.play_game("right") == "OoB"):
                break
            print(self.player_pos)
        for i in range(0,2):
            if (self.play_game("left") == "OoB"):
                break
            print(self.player_pos)

            

class Reinforcement_learning():
    def __init__(self):
        '''epsilon greedy algo'''
        self.epsilon = 0.8
        self.reward = 0
        self.model = self.init_model()
        self.current_iteration = []
    def epsilon_greedy_res(self,probabilities : list):
        rand = np.random.rand()
        if (rand < self.epsilon):
            #explore
            action = np.random.choice(len(probabilities))
        else:
            #exploit
            action = np.argmax(probabilities)
        return action
    def init_model(self):
        model = nn.Sequential(nn.Linear(2,4),nn.Linear(4,32),nn.Linear(32,4))
        return model
    def use_model(self,pos = [0,0]):
        self.current_iteration.append((int(pos[0]),int(pos[1])))
        self.model.eval()
        with torch.no_grad():
            y_pred = self.model(pos)
            result = self.convert_num_string(self.epsilon_greedy_res(y_pred))
        return result
    def convert_num_string(self,input):
        input = int(input)
        if input == 0:
            return "up"
        elif input == 1:
            return "down"
        elif input == 2:
            return "left"
        elif input == 3:
            return "right" 

        raise Exception("Invalid action" + str(input))  
    def update_model(self):
        gamma = 1
        reward = -100
        for pos in self.current_iteration:
            gamma = gamma * 0.75
            reward_temp = reward * gamma
            y_pred = self.model(pos)
            result = self.convert_num_string(self.epsilon_greedy_res(y_pred))

            
            
        
        


if __name__ == "__main__":
    env = create_environment(10,10)
    rl_agent = Reinforcement_learning()
    
    # Use the RL agent with the environment
    while True:
        pos_tensor = torch.tensor(env.player_pos, dtype=torch.float32)
        movement = rl_agent.use_model(pos=pos_tensor)
        output = env.play_game(movement)
        print(rl_agent.current_iteration)
        if output == "OoB":
            break