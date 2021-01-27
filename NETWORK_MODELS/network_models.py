import numpy as np
import pandas as pd
import random


def sir_network(graph, num_nodes, t_sim, infection_probability=0.3, recovery_period=7, num_infected_init=None):
    Pi = infection_probability  # beta (infection probability)
    Pr = 1/recovery_period      # gamma (1/7 days) (recovery time)

    if not num_infected_init:
        num_infected_init = int(num_nodes/100)

    # State vector # (0 susceptible, 1 infected, 2 recovered)
    S = np.zeros((t_sim,num_nodes))

    idx_init = list(np.random.randint(0, num_nodes, num_infected_init))

    S[0,idx_init]  = 1; # Seed the initial infected
    df_states = pd.DataFrame(index = pd.date_range(start=0, periods=t_sim, freq='D'), columns = ['S','I','R']).fillna(0)
    susceptibles_time = [num_nodes-num_infected_init ]
    infected_time     = [num_infected_init ]
    recovered_time    = [0]
    # Time loop
    for t in range(1,t_sim):
        # Individual loop

        # Individuals in each state.
        infected  = []
        recovered = []
        for ni, node_i  in enumerate(list(graph.nodes)):
            # check if already recovered:
            if S[t-1, ni]==2:
                recovered.append( ni )

            # check if infected
            if S[t-1, ni]==1:
                # Two cases: (A) Recover or (B) infect neighbors
                if random.random() < Pr: #or S[:,ni].sum()>=int(1/Pr):
                    recovered.append( ni )
                else:
                    infected.append( ni )

                # Loop over neighbors
                for nn in  graph.neighbors(node_i):
                    # Check if neighbor is susceptible and infect it
                    if S[t-1, nn] == 0 and random.random() < Pi:
                            infected.append( nn )
        infected  = list(np.unique(infected))
        recovered = list(np.unique(recovered))

        susceptibles_time.append(num_nodes-len(infected)-len(recovered))
        infected_time.append(len(infected))
        recovered_time.append(len(recovered))

        # Update graph state
        S[t, infected]  = 1
        S[t, recovered] = 2

    df_states['S'] = susceptibles_time
    df_states['I'] = infected_time
    df_states['R'] = recovered_time

    df_graph = pd.DataFrame(S)
    df_graph.index = df_states.index.values
    df_graph.rename({i: ni for i, ni in enumerate(graph.nodes) } )

    # return DF with graph sates and variables in time
    return (df_graph, df_states)


def seir_network(graph, num_nodes, t_sim, infection_probability=0.3, incubation_period=4, recovery_period=7, num_infected_init=None):

    Pe = infection_probability  # beta (infection probability)
    Pi = 1/incubation_period    # kappa (1/5 days) (incubation time)
    Pr = 1/recovery_period      # gamma (1/7 days) (recovery time)

    if not num_infected_init:
        num_infected_init = round(num_nodes/100)+1

    # State vector # (0 susceptible, 1 exposed, 2 infected, 3 recovered)
    S = np.zeros((t_sim,num_nodes))
    idx_init = list(np.random.randint(0, num_nodes, num_infected_init))

    S[0,idx_init]  = 2; # Seed the initial infected
    df_states = pd.DataFrame(index = pd.date_range(start=0, periods=t_sim, freq='D'), columns = ['S','E','I','R']).fillna(0)

    susceptibles_time = [num_nodes-num_infected_init ]
    exposed_time      = [0]
    infected_time     = [num_infected_init ]
    recovered_time    = [0]

    # Time loop
    for t in range(1,t_sim):
        # Individual loop
        # Individuals in each state.
        exposed   = []
        infected  = []
        recovered = []

        for ni, node_i  in enumerate( graph.nodes ):
            # check if already recovered:
            if S[t-1, ni]==3:
                recovered.append( ni )

            # check if exposed
            if S[t-1, ni]==1 and random.random() < Pi: #or S[t-int(1/Pi):t-1, ni].sum()>=1/Pi:
                infected.append( ni )
            elif S[t-1, ni]==1:
                exposed.append( ni )

            # check if infected
            if S[t-1, ni]==2:
                # Two cases: (A) Recover or (B) infect neighbors
                if random.random() < Pr:# or S[t-int(1/Pr)-1:t+1, ni].sum() /2>=1/Pr:
                    recovered.append( ni )
                else:
                    infected.append( ni )

                # Loop over neighbors
                for nn in  graph.neighbors( node_i ):
                    # Check if neighbor is susceptible and infect it
                    if S[t-1, nn] == 0 and random.random() < Pe:
                            exposed.append( nn )

        exposed   = list(np.unique(exposed))
        infected  = list(np.unique(infected))
        recovered = list(np.unique(recovered))

        susceptibles_time.append(num_nodes-len(exposed)-len(infected)-len(recovered))
        exposed_time.append(len(exposed))
        infected_time.append(len(infected))
        recovered_time.append(len(recovered))

        # Update graph state
        S[t, exposed]   = 1
        S[t, infected]  = 2
        S[t, recovered] = 3

    df_states['S'] = susceptibles_time
    df_states['E'] = exposed_time
    df_states['I'] = infected_time
    df_states['R'] = recovered_time

    df_graph = pd.DataFrame(S)
    df_graph.index = df_states.index.values
    df_graph.rename({i: ni for i, ni in enumerate(graph.nodes) } )

    # return DF with graph sates and variables in time
    return (df_graph, df_states)