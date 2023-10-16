from keras.models import Sequential
from keras.layers import Dense, Flatten
from keras.optimizers import Adam
from rl.agents import DQNAgent
from rl.policy import BoltzmannQPolicy
from rl.memory import SequentialMemory


class Agent:
    def __init__(self, env):
        self.states = env.observation_space.shape
        self.actions = env.action_space.n
        self.env = env

    def build_model(self):
        model = Sequential()
        model.add(Dense(24, activation='relu', input_shape=(1,2)))
        model.add(Dense(24, activation='relu'))
        model.add(Dense(self.actions, activation='linear'))
        model.add(Flatten())
        return model

    def build_agent(self):
        model = self.build_model()
        policy = BoltzmannQPolicy()
        memory = SequentialMemory(limit=5000, window_length=1)
        dqn = DQNAgent(model=model, memory=memory, policy=policy,
                       nb_actions=self.actions, nb_steps_warmup=10)
        return dqn

    def train(self, steps):
        dqn = self.build_agent()
        dqn.compile(Adam(learning_rate=1e-3), metrics=['mae'])
        dqn.fit(self.env, nb_steps=steps, visualize=False, verbose=1)



