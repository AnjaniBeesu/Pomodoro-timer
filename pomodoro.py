import time
print("Pomodoro Timer")
print("1. 25 min work / 5 min break")
print("2. 50 min work / 10 min break")
print("3. 100 min work / 20 min break")
choice = input("Choose option (1/2/3): ")
if choice == "1":
    work = 25  
    brk = 5
elif choice == "2":
    work = 50
    brk = 10
elif choice == "3":
    work = 100
    brk = 20
else:
    print("Invalid choice")
    input("Press Enter to exit...")
    exit()
cycles = int(input("How many cycles?: "))
def countdown(timer, label):
    while timer > 0:
        minutes = timer // 60
        seconds = timer % 60
        print(f"{label} {minutes:02d}:{seconds:02d}")
        user = input("Press Enter to continue or 'p' to pause: ")
        if user.lower() == 'p':
            input("Paused. Press Enter to resume...")
        timer -= 1
for i in range(1, cycles + 1):
    print(f"\nCycle {i} - Work")
    countdown(work, "Work")
    if i != cycles:
        print("Break time")
        countdown(brk, "Break")
print("\nAll cycles complete!")
input("Press Enter to exit...")
