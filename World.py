from Agent import Agent
import numpy as np
import random


class World():
    """
    Objective of this class is to determine what is the well the water is
    being pumped to and create agents according to the prior type passed in.

    Parameters:

        correctWell (int): 0, 1, or 2
        wellA (x,y): Tuple of the x- and y-coordinates
        wellB (x,y): Tuple of the x- and y-coordinates
        wellC (x,y): Tuple of the x- and y-coordinates
        population (int): Keeps track of our population numbers
    """

    def __init__(self, good=0,bad=0, people=200, global_confidence=-1):
        """ Initialize the case of Uniform, Unique, Good or Bad

        ratio ((2,), ndarray): [%neutral, %good, %bad]
        """
        #initialize data list
        self.get_data = []

        #establish population and ratio
        self.population = people
        self.ratio = np.array([people-good-bad,good,bad])/people

        #establish locations of the wells
        distance = np.linspace(-1,1,101)
        wellA = (np.random.choice(distance),np.random.choice(distance))
        wellB = (np.random.choice(distance),np.random.choice(distance))
        wellC = (np.random.choice(distance),np.random.choice(distance))
        self.well_locations = np.concatenate(([wellA],[wellB],[wellC]))

        #make list of agents
        self.Agent_list = [Agent(global_confidence) for i in range(self.population)]


    def seed_list(self, correctWell):
        """

        Parameters:
            correctWell (int): 0,1,2 the correct_well
        """
        #make them random and get how many good and bad
        random.shuffle(self.Agent_list)
        num_Good = int(np.round(self.ratio[1]*self.population))
        num_Bad = int(np.round(self.ratio[2]*self.population))
        #num_Good, num_Bad = tuple(np.round(self.ratio[1:]*self.population).astype(int))

        if self.ratio[0] != 1:
            #seed the agents
            for agent in self.Agent_list[:num_Good]:
                agent.seed("good",correctWell)
            for agent in self.Agent_list[num_Good:num_Good+num_Bad]:
                agent.seed("bad",correctWell)
            for egent in self.Agent_list[num_Good+num_Bad:]:
                agent.seed("neutral",correctWell)

            random.shuffle(self.Agent_list)

    def each_day(self, cascade =True):
        correctWell = np.random.choice(np.array([0, 1, 2]))

        #seed list
        self.seed_list(correctWell)

        #tracking the actions of the agents
        if self.population == 0:
            return

        observations = [self.Agent_list[0].act([],correctWell, self.well_locations)]

        for agent in self.Agent_list[1:]:
            if cascade:
                observations.append(agent.act(observations,correctWell, self.well_locations))
            else:
                observations.append(agent.act([],correctWell, self.well_locations))

        data = []
        for i, obs in enumerate(observations):
            data.append([i,correctWell,obs,self.Agent_list[i].seed_type])

        #update agents/population based on deaths
        Agent_remove = []
        for agent in self.Agent_list:
            if agent.health == 0:
                Agent_remove.append(agent)
        for agent in Agent_remove:
            self.Agent_list.remove(agent)
        self.population = len(self.Agent_list)

        self.collect_data(observations,correctWell)

        #print(np.array(data))

        #return correctWell, np.sum(np.array(observations) == correctWell), self.population


    def collect_data(self, obs, correctWell):
        """ This function is to collect what we do each day. We call it at the
            end of the each_day() function and we pass in observations and the
            correct well. The goal is to see what we do each day

        Parameters:
            obs (list): list of the actions of the day
        """
        well1 = np.sum(np.array(obs) == 0)
        well2 = np.sum(np.array(obs) == 1)
        well3 = np.sum(np.array(obs) == 2)


        percent_correct = np.sum(np.array(obs) == correctWell)/self.population if self.population != 0 else 0


        #print(self.get_data)
        data = list(self.get_data)
        data.append(np.array([self.population, percent_correct, well1,well2,well3]))
        self.get_data = np.array(data)



        #self.get_data = np.append(self.get_data,np.array([self.population, percent_correct, well1,well2,well3]))
