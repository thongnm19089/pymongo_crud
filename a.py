# ...existing code...

import pymongo
from pymongo import MongoClient

# Chuỗi kết nối MongoDB
chuoi_ket_noi_mongo = "mongodb+srv://thongnmnde19089:nvSvj8bU91D4iTw2@cluster0.oligx.mongodb.net/"

# Tạo một MongoClient để kết nối với mongod đang chạy
client = MongoClient(chuoi_ket_noi_mongo)

db = client.get_database('bulkflow')

collection_sinh_vien = db['students']

def them_sinh_vien():
    ten = input("Nhập tên sinh viên: ")
    tuoi = int(input("Nhập tuổi sinh viên: "))
    gioi_tinh = input("Nhập giới tính sinh viên: ")
    diem_toan = float(input("Nhập điểm Toán: "))
    diem_ly = float(input("Nhập điểm Lý: "))
    diem_hoa = float(input("Nhập điểm Hóa: "))
    
    tai_lieu_sinh_vien = {
        "ten": ten,
        "tuoi": tuoi,
        "gioi_tinh": gioi_tinh,
        "diem": {
            "toan": diem_toan,
            "ly": diem_ly,
            "hoa": diem_hoa
        }
    }
    
    collection_sinh_vien.insert_one(tai_lieu_sinh_vien)
    print("Đã thêm sinh viên thành công.")

def hien_thi_tat_ca_sinh_vien():
    sinh_vien_list = collection_sinh_vien.find()
    for sv in sinh_vien_list:
        print(sv)

def xoa_sinh_vien_theo_id():
    id_sinh_vien = input("Nhập ID sinh viên cần xóa: ")
    collection_sinh_vien.delete_one({"_id": pymongo.ObjectId(id_sinh_vien)})
    print("Đã xóa sinh viên thành công.")

def tim_kiem_sinh_vien_theo_ten_tuoi():
    ten = input("Nhập tên sinh viên cần tìm: ")
    tuoi = int(input("Nhập tuổi sinh viên cần tìm: "))
    sinh_vien_list = collection_sinh_vien.find({"ten": ten, "tuoi": tuoi})
    for sv in sinh_vien_list:
        print(sv)

def tim_kiem_sinh_vien_diem_mon_lon_hon():
    mon = input("Nhập tên môn học (toan, ly, hoa): ")
    diem = float(input(f"Nhập điểm {mon} cần tìm: "))
    sinh_vien_list = collection_sinh_vien.find({f"diem.{mon}": {"$gt": diem}})
    for sv in sinh_vien_list:
        print(sv)

def tim_kiem_sinh_vien_tong_diem_lon_hon():
    tong_diem = float(input("Nhập tổng điểm cần tìm: "))
    sinh_vien_list = collection_sinh_vien.find()
    for sv in sinh_vien_list:
        diem = sv["diem"]
        if diem["toan"] + diem["ly"] + diem["hoa"] > tong_diem:
            print(sv)

def menu():
    while True:
        print("\nMenu:")
        print("1. Thêm sinh viên")
        print("2. Hiển thị tất cả sinh viên")
        print("3. Xóa sinh viên theo ID")
        print("4. Tìm kiếm sinh viên theo tên, tuổi")
        print("5. Tìm kiếm sinh viên có điểm môn xxx > yyy")
        print("6. Tìm kiếm sinh viên có tổng điểm 3 môn > xxx")
        print("0. Thoát")
        
        lua_chon = input("Nhập lựa chọn của bạn: ")
        
        if lua_chon == "1":
            them_sinh_vien()
        elif lua_chon == "2":
            hien_thi_tat_ca_sinh_vien()
        elif lua_chon == "3":
            xoa_sinh_vien_theo_id()
        elif lua_chon == "4":
            tim_kiem_sinh_vien_theo_ten_tuoi()
        elif lua_chon == "5":
            tim_kiem_sinh_vien_diem_mon_lon_hon()
        elif lua_chon == "6":
            tim_kiem_sinh_vien_tong_diem_lon_hon()
        elif lua_chon == "0":
            break
        else:
            print("Lựa chọn không hợp lệ. Vui lòng thử lại.")

if __name__ == "__main__":
    menu()

# ...existing code...
