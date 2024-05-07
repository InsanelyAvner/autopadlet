import concurrent.futures
from main import main_bot

def main():

    ############## CONFIGURATION ####################
    MODE = "like" # "comment" or "like"

    # Number of parallel bot instances
    # WARNING: THE MORE INSTANCES THERE IS, THE MORE SYSTEM RESOURCES IS TAKEN
    parallel_instances = 5 # recommended: 3-8 (depending on your computeing power)
    #################################################

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(main_bot, MODE, i + 1) for i in range(parallel_instances)]
        for future in concurrent.futures.as_completed(futures):
            result = future.result()  

if __name__ == '__main__':
    main()
