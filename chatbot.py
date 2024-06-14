import re
import json
import random
import math

class ComplexChatBot:
    def __init__(self):
        self.memory = {}  # Dictionary to store learned information
        self.file_path = "learned_responses.json"
        self.load_learned_responses()

    def load_learned_responses(self):
        try:
            with open(self.file_path, 'r') as file:
                self.memory = json.load(file)
        except FileNotFoundError:
            # Handle case where the file doesn't exist yet
            pass

    def learn_from_input(self, message):
        # Use regex to match and extract the learning pattern
        pattern = re.compile(r"learn: (.*)", re.IGNORECASE)
        match = pattern.match(message)
        if match:
            info = match.group(1).strip()
            if '=' in info:
                key, value = info.split('=')
                self.memory[key.strip()] = value.strip()
                self.save_learned_responses()
                return "Learned!"
        return None

    def save_learned_responses(self):
        with open(self.file_path, 'w') as file:
            json.dump(self.memory, file, indent=4)

    def respond(self, message):
        # Check if the message is for learning
        learned_response = self.learn_from_input(message)
        if learned_response:
            return learned_response

        # Check memory for learned responses
        for key in self.memory:
            if key.lower() in message.lower():
                return f"{self.memory[key]}"

        # Check for mathematical calculations
        try:
            # Evaluate general mathematical expressions
            result = eval(message)
            return f"The answer is {result}"

        except Exception as e:
            pass

        # Check for square root and other complex expressions
        try:
            # Check for square root followed by arithmetic operations
            if any(op in message for op in ['+', '-', '*', '/']) and "sqrt" in message.lower():
                # Replace 'sqrt' with 'math.sqrt' and evaluate
                expr = re.sub(r'sqrt\((.*?)\)', r'math.sqrt(\1)', message)
                result = eval(expr)
                return f"The result of {message} is {result}"

            # Check for logarithm
            if "log" in message.lower():
                # Extract base and value from message
                parts = re.findall(r'log(\d+)\((.*?)\)', message, re.IGNORECASE)
                if parts:
                    base = parts[0][0]
                    value = parts[0][1]
                    result = math.log(float(value), float(base))
                    return f"The logarithm of {value} with base {base} is {result}"

        except Exception as e:
            pass

        # Default responses if no match found
        responses = [
            "I'm not sure I understand.",
            "Could you please elaborate?",
            "Hmm, interesting.",
        ]
        return random.choice(responses)

# Create an instance of the ComplexChatBot
bot = ComplexChatBot()

# Main interaction loop
print("Bot: Hello! How can I help you today?")
while True:
    user_input = input("You: ")
    if user_input.lower() == 'exit':
        print("Bot: Bye! Have a great day.")
        break
    response = bot.respond(user_input)
    print("Bot:", response)
