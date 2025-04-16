import random

def generate_random_binary_sequence():
    return ''.join(random.choice('01') for _ in range(128))

if __name__ == "__main__":
    random_sequence = generate_random_binary_sequence()
    print("Случайная 128-битная бинарная последовательность:", random_sequence)
