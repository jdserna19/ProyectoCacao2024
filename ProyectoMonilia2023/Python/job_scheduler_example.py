import schedule
import time


def job(param):
    print("I'm working...")
    print("Param: {}".format(param))


schedule.every(1).seconds.do(job, "Hello World!")
# schedule.every().monday.at("10:28").do(job, "Hello World!")
# schedule.every().hour.do(job)
schedule.every().day.at("18:18").do(job, "Hello World!")
'''
schedule.every().monday.do(job)
schedule.every().wednesday.at("13:15").do(job)
'''

while True:
    schedule.run_pending()
    print("Running...")
    time.sleep(10)
