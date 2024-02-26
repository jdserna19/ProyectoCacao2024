from time import sleep
from apscheduler.schedulers.background import BackgroundScheduler as Scheduler

sched = Scheduler()
variable = False


def print_text(text):
    global variable
    variable = True
    print(text)
    sleep(10)
    variable = False
 
    
def print_other_text(text):
    global variable
    while variable:
        print("Waiting...")
        None
    variable = True
    print(text)
    sleep(6)
    variable = False
   
    
'''
def main():
    job = sched.add_job(print_text, 'date', '2018-08-22 10:15:00', ["Hello"])
    sched.start()
    while True:
        sleep(1)

        
if __name__ == "__main__":
    main()


'''
sched.add_job(func=print_other_text, trigger='date', run_date='2018-08-22 14:18:00', args=["Hello"])
# sched.add_job(print_text, 'interval', seconds=2, start_date='2018-08-22 11:17:30', args=["Hello"])
# sched.add_job(print_other_text, 'interval', seconds=1, start_date='2018-08-22 11:17:30', args=["Hello 2"])
sched.start()
while True:
    if not variable:
        print_text("Normal data visualization.")
    sleep(1)
    print("Ends sleeping")
