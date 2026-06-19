from knowledge_base import KB, agent_reasoning
import time

def main():
    print('Welcome to the smart home system.')
    nb_rooms = int(input('Please fill in the number of rooms in your house: '))
    duration = int(input('Please fill in the number of seconds for which you would like the program to last: '))
    start_time = int(time.time())
    kb = KB(nb_rooms)
    last_randomized = start_time
    print('\n' + "#"*75 + '\n')
    while True:
        time_now = int(time.time())
        if time_now - start_time >= duration:
            break
        
        for i in range(1, nb_rooms + 1):
            agent_reasoning(kb, "room" + str(i))
        
        if time_now - last_randomized >= 1:
            kb.randomize()
            last_randomized = time_now
    print('\n' + "#"*35)
    print('\tLOGS')
    print("#"*35 + '\n')
    for key, value in kb.logs.items():
        print(f"{key.title()} has been switched {value} time(s).")

if __name__ == "__main__":
    main()
    
    