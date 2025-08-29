# analyze.py
import pandas as pd
import matplotlib.pyplot as plt
import ast # To convert string representations of lists back to lists

# Load the training data
df = pd.read_csv('training_data.csv')

# The 'state', 'action', and 'next_state' columns are saved as strings
# We need to convert them back to lists of numbers
df['state'] = df['state'].apply(ast.literal_eval)
df['action'] = df['action'].apply(ast.literal_eval)

# --- Example Analysis ---

# 1. Print the first few rows of the data
print("--- First 5 rows of data ---")
print(df.head())

# 2. Print basic statistics
print("\n--- Basic Statistics ---")
print(df[['game', 'score', 'reward']].describe())

# 3. Plot the distribution of rewards
plt.figure(figsize=(10, 6))
df['reward'].value_counts().plot(kind='bar', title='Distribution of Rewards')
plt.xlabel('Reward Value')
plt.ylabel('Frequency')
plt.show()

# 4. Plot score progression over games
# Get the final score for each game
final_scores = df.groupby('game')['score'].max()

plt.figure(figsize=(12, 7))
plt.plot(final_scores.index, final_scores.values, label='Score per Game')
plt.plot(final_scores.index, final_scores.rolling(window=50).mean(), label='50-Game Moving Average', color='red')
plt.title('Score Progression Over Training')
plt.xlabel('Game Number')
plt.ylabel('Final Score')
plt.legend()
plt.grid(True)
plt.show()