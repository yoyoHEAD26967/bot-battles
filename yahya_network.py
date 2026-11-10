import torch
import torch.nn as nn
from torch import optim

from robot import Robot
from arena import Arena
from yahya_bot import YahyaBot
from balanced_bot import BalancedBot

import numpy as np

import os
import json

class ArenaEnvironment(Arena):
    def __init__(self):
        super().__init__(BalancedBot(), YahyaBot())

        self.episode = 0
        self.steps = 0
        self.last_reward = None

    def reset(self):
        if self.steps > 0:
            self.episode += 1

        super().setup()

        self.steps = 0

        return BotWorker.combine_state_datas(self.robot1, self.robot2)

    def step(self, action):
        self.robot2.decision = action

        self.round(self.steps)

        status = self.get_winner()

        if status == None:
            return BotWorker.combine_state_datas(self.robot1, self.robot2), 0, False

        elif status == True:
            return BotWorker.combine_state_datas(self.robot1, self.robot2), 100, True

        elif status == False:
            return BotWorker.combine_state_datas(self.robot1, self.robot2), -100, True

        else:
            print("Error - get_winner() method failed to give game status!")
            return


class BotNetwork(nn.Module):
    def __init__(self, inputs = 7, outputs = 3, h1 = 16, h2 = 8):
        super(BotNetwork, self).__init__()

        self.input_neurons = inputs
        self.output_neurons = outputs

        self.fc1 = nn.Linear(inputs, h1)
        self.fc2 = nn.Linear(h1, h2)
        self.out = nn.Linear(h2, outputs)
        self.relu = nn.ReLU()
        self.dropout = nn.Dropout()

    def forward(self, x):
        x = self.relu(self.fc1(x))
        x = self.dropout(x)

        x = self.relu(self.fc2(x))
        x = self.dropout(x)

        x = self.out(x)

        return x

"""
0: repair
1: attack
2: special attack
"""

class BotWorker():
    def __init__(self, data: list = []):
        self.model = BotNetwork()
        self.discount_factor = 0.9995
        self.learning_rate = 0.001

        self.optimizer = optim.Adam(self.model.parameters(), lr=self.learning_rate)
        self.states, self.actions, self.rewards = [], [], []


    @classmethod
    def combine_state_datas(cls, enemy: Robot, bot: Robot):
        data_entry = {"enemy_structural_integrity": enemy.structural_integrity,
                      "enemy_battery": enemy.battery,
                      "enemy_damage": enemy.calculate_damage(),
                      "bot_structural_integrity": bot.structural_integrity,
                      "bot_battery": bot.battery,
                      "bot_damage": bot.calculate_damage(),
                      "bot_armour": bot.armour
        }

        return list(data_entry.values())

    def get_action(self, state):

        

        with torch.no_grad():
            logits = self.model(torch.as_tensor(state, dtype=torch.float32))
            probs = torch.softmax(logits, dim=-1).numpy()

        return int(np.random.choice(self.model.output_neurons, p=probs))

    def discounted_rewards(self, rewards):
        discounted = np.zeros_like(rewards, dtype=np.float32)
        running = 0

        for t in reversed(range(len(rewards))):
            running = running * self.discount_factor + rewards[t]

            discounted[t] = running

        return discounted

    def append_sample(self, state, action, reward):
        self.states.append(state)
        self.actions.append(action)
        self.rewards.append(reward)        

    def train_model(self):
        returns = self.discounted_rewards(np.array(self.rewards, dtype=np.float32))

        returns = (returns - returns.mean()) / (returns.std() + 0.00000008)

        states = torch.as_tensor(np.array(self.states), dtype=torch.float32)
        actions = torch.as_tensor(self.actions, dtype=torch.long)
        returns_t = torch.as_tensor(returns, dtype=torch.float32)

        logits = self.model(states)
        log_probs = torch.log_softmax(logits, dim=-1)
        chosen = log_probs.gather(1, actions.unsqueeze(1)).squeeze(1)
        loss = -(chosen * returns_t).sum()

        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

        self.states, self.actions, self.rewards = [], [], []

    def save_model(self, model_path, dimension_path):
        torch.save({})


if __name__ == "__main__":
    episodes = 2000

    env = ArenaEnvironment()
    bot = BotWorker()
    global_step = 0

    for e in range(episodes):
        done = False
        score = 0
        state = np.array(env.reset(), dtype=np.float32)

        while not done:
            global_step += 1
            action = bot.get_action(state)
            next_state, reward, done = env.step(action)
            next_state = np.array(next_state, dtype=np.float32)

            bot.append_sample(state, action, reward)
            score += reward

            state = next_state

            if done:
                bot.train_model()
                print(f"episode: {e}  score: {round(score, 2)}  steps: {global_step}")
        