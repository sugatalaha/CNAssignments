import random
import matplotlib.pyplot as plt

class Node:
    def __init__(self, node_id, probability, queue_size):
        self.node_id = node_id
        self.probability = probability  # p-persistent probability
        self.queue = [1] * queue_size  # Frames to be sent (represented as 1s)
        self.backoff_time = 0  # Time to wait before retrying after collision
        self.total_delay = 0  # To measure forwarding delay
        self.k=0

    def has_frame_to_send(self):
        return len(self.queue) > 0

    def send_frame(self):
        if self.backoff_time > 0:
            self.backoff_time -= 1
            return False  # Node is waiting due to backoff
        if random.random() <= self.probability:
            return True  # Send frame with probability p
        return False

    def detect_collision(self):
        # Random collision probability (simulate collision)
        return random.random() < 0.2  # Assume 20% chance of collision

    def backoff(self):
        # Exponential backoff
        self.backoff_time = random.randint(0,pow(2,self.k)-1)
    
    def remove_frame(self):
        if self.queue:
            self.queue.pop(0)

    def add_delay(self, delay):
        self.total_delay += delay

class CSMA_CD:
    def __init__(self, num_nodes, probability, queue_size):
        self.nodes = [Node(i, probability, queue_size) for i in range(num_nodes)]
        self.time = 0  # Time slot count
        self.throughput = 0  # Successful frames transmitted
        self.total_delay = 0  # Total delay of all frames

    def run_simulation(self, max_time):
        while self.time < max_time:
            print(f"--------------------------------Slot {self.time}--------------------------------")
            # Step 1: Sense the channel for idle/busy (basic simulation)
            transmitting_nodes = []
            for node in self.nodes:
                if node.has_frame_to_send() and node.send_frame():
                    print(f"Node {node.node_id} is willing to send data")
                    transmitting_nodes.append(node)

            # Step 2: Handle collisions
            if len(transmitting_nodes) > 1:  # More than one node tries to send
                for node in transmitting_nodes:
                    if node.detect_collision():
                        print(f"Node {node.node_id} is backing off")
                        node.k+=1
                        node.backoff()  # Collision detected, backoff
                    else:
                        print(f"Packet from Node {node.node_id} has collided!")
                        node.k+=1
                        node.backoff()
            elif len(transmitting_nodes) == 1:  # Only one node is transmitting
                node = transmitting_nodes[0]
                print(f"Node {node.node_id} is transmitting data successfully...")
                self.throughput += 1
                node.remove_frame()
                node.k=0
                node.add_delay(self.time)

            self.time += 1  # Advance simulation time

        # Measure average forwarding delay (total delay/number of nodes)
        self.total_delay = sum([node.total_delay for node in self.nodes]) / len(self.nodes)

    def get_metrics(self):
        throughput = self.throughput / self.time  # Bits per time unit
        avg_forwarding_delay = self.total_delay
        return throughput, avg_forwarding_delay

# Simulation Parameters
num_nodes = 5  # Number of nodes in the simulation
queue_size = 10  # Number of frames per node
simulation_time = 5  # Total simulation time slots

# Function to run simulation with varying probabilities
def simulate_varying_p(probabilities):
    throughput_list = []
    delay_list = []

    for p in probabilities:
        print(f"Running simulation for p={p}")
        csma_cd_simulation = CSMA_CD(num_nodes, p, queue_size)
        csma_cd_simulation.run_simulation(simulation_time)
        throughput, avg_forwarding_delay = csma_cd_simulation.get_metrics()
        throughput_list.append(throughput)
        delay_list.append(avg_forwarding_delay)

    return throughput_list, delay_list

# Define a range of probabilities for p-persistent CSMA
probabilities = [1.0]

# Run the simulation and collect results
throughput_list, delay_list = simulate_varying_p(probabilities)

# Plot results
fig, ax1 = plt.subplots()

color = 'tab:red'
ax1.set_xlabel('Probability p')
ax1.set_ylabel('Throughput', color=color)
ax1.plot(probabilities, throughput_list, color=color, marker='o', label='Throughput')
ax1.tick_params(axis='y', labelcolor=color)

ax2 = ax1.twinx()  
color = 'tab:blue'
ax2.set_ylabel('Forwarding Delay', color=color)  
ax2.plot(probabilities, delay_list, color=color, marker='o', label='Forwarding Delay')
ax2.tick_params(axis='y', labelcolor=color)

fig.tight_layout()  
plt.title('Throughput and Forwarding Delay vs p')
plt.show()

# Observations
for i, p in enumerate(probabilities):
    print(f"For p = {p:.1f}, Throughput: {throughput_list[i]:.4f}, Avg Forwarding Delay: {delay_list[i]:.4f}")
