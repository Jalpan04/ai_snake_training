# train.py
import torch
import csv
from agent import Agent
from snake_game import SnakeGameAI
from helper import plot


# --- Function to setup the CSV file ---
def setup_csv(filename='training_data.csv'):
    header = [
        'game', 'epsilon', 'score', 'record',
        'state', 'action', 'reward', 'done', 'next_state'
    ]
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
    return filename


# --- Function to append data to the CSV file ---
def append_to_csv(filename, data_row):
    with open(filename, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(data_row)


def train():
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record = 0
    agent = Agent()
    game = SnakeGameAI()

    # --- Initialize CSV logger ---
    data_filename = setup_csv()

    while True:
        # Get old state
        state_old = agent.get_state(game)

        # Get move
        final_move = agent.get_action(state_old)

        # Perform move and get new state
        reward, done, score = game.play_step(final_move)
        state_new = agent.get_state(game)

        # --- Log the data for this step ---
        # Convert numpy arrays to lists for better CSV formatting
        state_old_list = state_old.tolist()
        final_move_list = final_move
        state_new_list = state_new.tolist()

        data_row = [
            agent.n_games, agent.epsilon, score, record,
            state_old_list, final_move_list, reward, done, state_new_list
        ]
        append_to_csv(data_filename, data_row)
        # --- End of logging ---

        # Train short memory
        agent.train_short_memory(state_old, final_move, reward, state_new, done)

        # Remember
        agent.remember(state_old, final_move, reward, state_new, done)

        if done:
            # Train long memory (experience replay)
            game.reset()
            agent.n_games += 1
            agent.train_long_memory()

            if score > record:
                record = score
                agent.model.save()

            print('Game', agent.n_games, 'Score', score, 'Record:', record)

            plot_scores.append(score)
            total_score += score
            mean_score = total_score / agent.n_games
            plot_mean_scores.append(mean_score)
            plot(plot_scores, plot_mean_scores)


if __name__ == '__main__':
    train()