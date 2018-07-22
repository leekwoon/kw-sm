# 자동예약 테스트 

from korail2 import Korail
import time
import numpy as np

def main():    
    dep = "울산"
    arr = "서울"
    date = "20180720"
    dep_time = "184000"
    
    login_update_every = 300 # login 갱신 
    login_update_time = time.time()
    
    korail = Korail(ID, PASSWORD, auto_login=False) 
    korail.login()
    trains = korail.search_train(dep, arr, date, dep_time, include_no_seats=True)

    while True:
        time.sleep(0.1)
        try:
            if time.time() - login_update_time > login_update_every:
                login_update_time = time.time()
                korail = Korail("010-2857-7771", "2rydnstm@@", auto_login=False)
                korail.login()
                trains = korail.search_train(dep, arr, date, dep_time, include_no_seats=True)
                print('login again')
            
            target = np.random.choice([0])
            print(trains[target])
            # target = np.random.choice([0, 1, 2])
            
            seat = korail.reserve(trains[target])
            print('success')
            break
        except:
            pass
            # print('fail [no seat]')
    
if __name__ == "__main__":
    main()