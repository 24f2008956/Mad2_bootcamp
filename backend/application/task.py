from celery import shared_task
import time
from .models import db, Parking_lot
import csv
import os 

@shared_task(name = "test task" )
def test_task():
    time.sleep(30)
    return "it's done"  

@shared_task(name = "download_csv_admin")
def csv_down_ad():
    lots =Parking_lot.query.all()
    os.makedirs("./static" ,exist_ok= True )

    filename = "admin_csv_download.csv" 
    time.sleep(20)
    with open( f"./static/{filename}", "w") as csvfile:
        csv_obj = csv.writer(csvfile , delimiter=",")

        csv_obj.writerow(["No." , "ParkingLot Name" , "Address" ,"No.of Spots"])
        for index , lot in enumerate(lots):
            csv_obj.writerow([index+1 , lot.lot_name , lot.lot_address , len(lot.spots)])
    

    return filename