import simpy
import random
import statistics

# -------------------------------------------------
# Simulation Parameters
# -------------------------------------------------
RANDOM_SEED = 123
SERVICE_RATE = 15      # μ = 15 students per hour
ARRIVAL_RATE = 10      # λ = 10 students per hour
SIM_TIME = 6 * 60      # 6 hours (in minutes)

# Convert rates to minutes
MEAN_SERVICE_TIME = 60 / SERVICE_RATE
MEAN_INTERARRIVAL = 60 / ARRIVAL_RATE

waiting_times = []

# -------------------------------------------------
# Student Process
# -------------------------------------------------
def student(env, student_id, cafeteria_counter):
    arrival_time = env.now

    # Request service
    with cafeteria_counter.request() as request:
        yield request

        # Waiting time
        wait_time = env.now - arrival_time
        waiting_times.append(wait_time)

        # Service time (Exponential)
        service_time = random.expovariate(1.0 / MEAN_SERVICE_TIME)
        yield env.timeout(service_time)

# -------------------------------------------------
# Arrival Generator
# -------------------------------------------------
def student_arrivals(env, cafeteria_counter):
    student_id = 0
    while True:
        interarrival_time = random.expovariate(1.0 / MEAN_INTERARRIVAL)
        yield env.timeout(interarrival_time)
        student_id += 1
        env.process(student(env, student_id, cafeteria_counter))

# -------------------------------------------------
# Simulation Execution
# -------------------------------------------------
def run_simulation():
    random.seed(RANDOM_SEED)
    env = simpy.Environment()

    # Single cafeteria counter
    cafeteria_counter = simpy.Resource(env, capacity=1)

    env.process(student_arrivals(env, cafeteria_counter))
    env.run(until=SIM_TIME)

    return waiting_times

# -------------------------------------------------
# Main Program
# -------------------------------------------------
if __name__ == "__main__":
    results = run_simulation()

    print("University Cafeteria Queue Simulation Completed")
    print(f"Total students served: {len(results)}")
    print(f"Average waiting time: {statistics.mean(results):.2f} minutes")
    print(f"Maximum waiting time: {max(results):.2f} minutes")
