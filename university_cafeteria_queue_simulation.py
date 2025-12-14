import simpy
import random
import statistics

# -------------------------------------------------
# Simulation Parameters
# -------------------------------------------------
RANDOM_SEED = 123
SERVICE_RATE = 15      # μ = 15 students/hour
ARRIVAL_RATE = 10      # λ = 10 students/hour
SIM_TIME = 6 * 60      # 6 hours (minutes)

MEAN_SERVICE_TIME = 60 / SERVICE_RATE
MEAN_INTERARRIVAL = 60 / ARRIVAL_RATE

# -------------------------------------------------
# Student Process
# -------------------------------------------------
def student(env, cafeteria_counter, waiting_times):
    arrival_time = env.now

    with cafeteria_counter.request() as request:
        yield request
        wait_time = env.now - arrival_time
        waiting_times.append(wait_time)

        service_time = random.expovariate(1.0 / MEAN_SERVICE_TIME)
        yield env.timeout(service_time)

# -------------------------------------------------
# Arrival Generator
# -------------------------------------------------
def student_arrivals(env, cafeteria_counter, waiting_times):
    while True:
        interarrival_time = random.expovariate(1.0 / MEAN_INTERARRIVAL)
        yield env.timeout(interarrival_time)
        env.process(student(env, cafeteria_counter, waiting_times))

# -------------------------------------------------
# Simulation Execution
# -------------------------------------------------
def run_simulation():
    random.seed(RANDOM_SEED)
    waiting_times = []

    env = simpy.Environment()
    cafeteria_counter = simpy.Resource(env, capacity=1)

    env.process(student_arrivals(env, cafeteria_counter, waiting_times))
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
