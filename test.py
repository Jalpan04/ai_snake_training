import torch


# Make sure you have the file containing your model's class definition
# For example, from model import Linear_QNet

# --- Assume this is your model's architecture ---
# You must have this class definition available
class Linear_QNet(torch.nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super().__init__()
        self.linear1 = torch.nn.Linear(input_size, hidden_size)
        self.linear2 = torch.nn.Linear(hidden_size, output_size)
        self.relu = torch.nn.ReLU()

    def forward(self, x):
        x = self.linear1(x)
        x = self.relu(x)
        x = self.linear2(x)
        return x


# ------------------------------------------------

# 1. Define model parameters (must match the saved model)
INPUT_SIZE = 11  # Example: size of your state vector
HIDDEN_SIZE = 256  # Example: hidden layer size
OUTPUT_SIZE = 3  # Example: number of actions (straight, right, left)

# 2. Instantiate the model
model = Linear_QNet(INPUT_SIZE, HIDDEN_SIZE, OUTPUT_SIZE)

# 3. Load the saved weights from the .pth file
model.load_state_dict(torch.load('model/model.pth'))

# 4. Set the model to evaluation mode
model.eval()


# --- Now you can use the model to make predictions ---

def get_action(state):
    """
    This function takes the game state and returns the best action.
    """
    # Convert state to a PyTorch tensor
    # The state needs to be in the correct format (e.g., a tensor of floats)
    state_tensor = torch.tensor(state, dtype=torch.float)

    # Get model prediction (no gradient calculation needed for inference)
    with torch.no_grad():
        prediction = model(state_tensor)

    # The action is the index of the highest value in the prediction
    # e.g., if prediction is [0.1, 2.5, -1.2], argmax is 1
    action = torch.argmax(prediction).item()

    # The final move will be a one-hot encoded vector, e.g., [0, 1, 0]
    final_move = [0, 0, 0]
    final_move[action] = 1

    return final_move


# Example usage within your game loop:
# Get the current state from the game
current_state = [0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1]  # A sample state vector

# Ask the trained model for the best move
best_move = get_action(current_state)

print(f"For state: {current_state}")
print(f"The AI chose move: {best_move}")