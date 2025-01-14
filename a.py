from pymongo import MongoClient
from bson import ObjectId
from pymongo.errors import ConnectionFailure

chuoi_ket_noi_mongo = "mongodb+srv://thongnmnde19089:nvSvj8bU91D4iTw2@cluster0.oligx.mongodb.net/"

client = MongoClient(chuoi_ket_noi_mongo)
try:
    client.admin.command('ping')
    print("\nKết nối thành công đến MongoDB")
except ConnectionFailure:
    print("\nKết nối thất bại đến MongoDB")
db = client.get_database('bulkflow')
collection_sinh_vien = db['students']

def show_sv(sinh_vien_list):
    print("\n------------------------------------------Danh sách sinh viên:----------------------------------------")
    print(f"{'ID'.ljust(32)}{'Tên'.ljust(16)}{'Tuổi'.ljust(10)}{'Giới tính'.ljust(15)}{'Toán'.ljust(10)}{'Lý'.ljust(10)}{'Hóa'.ljust(10)}")
    sinh_vien = list(sinh_vien_list)
    if not sinh_vien:
        print("Không có sinh viên nào !!")
    else:
        for sv in sinh_vien:
            if "ten" in sv:
                id_sv = str(sv["_id"])
                ten_sv = sv["ten"] if "ten" in sv else sv.get("name", "Không có tên")
                tuoi_sv = str(sv["tuoi"]) if "tuoi" in sv else str(sv.get("age", "null"))
                gioi_tinh_sv = sv["gioi_tinh"] if "gioi_tinh" in sv else sv.get("gender", "Không có giới tính")
                toan = str(sv['diem']['toan'] if 'diem' in sv and 'toan' in sv['diem'] else sv.get('scores', {}).get('math', 'Không có điểm Toán'))
                ly = str(sv['diem']['ly'] if 'diem' in sv and 'ly' in sv['diem'] else sv.get('scores', {}).get('physics', 'Không có điểm Lý'))
                hoa = str(sv['diem']['hoa'] if 'diem' in sv and 'hoa' in sv['diem'] else sv.get('scores', {}).get('chemistry', 'Không có điểm Hóa'))
                print(f"{id_sv.ljust(32)}{ten_sv.ljust(16)}{tuoi_sv.ljust(10)}{gioi_tinh_sv.ljust(15)}{toan.ljust(10)}{ly.ljust(10)}{hoa.ljust(10)}")

def them_sinh_vien():
    ten = input("Nhập tên sinh viên: ")
    tuoi = int(input("Nhập tuổi sinh viên: "))
    gioi_tinh = input("Nhập giới tính sinh viên: ")
    while True:
        diem_toan = float(input("Nhập điểm Toán: "))
        if diem_toan >= 0 and diem_toan <= 10:
            break
        else:
            print("Điểm phải nằm trong khoảng từ 0 đến 10. Vui lòng nhập lại.")

    while True:
        diem_ly = float(input("Nhập điểm Lý: "))
        if diem_ly >= 0 and diem_ly <= 10:
            break
        else:
            print("Điểm phải nằm trong khoảng từ 0 đến 10. Vui lòng nhập lại.")
            
    while True:
        diem_hoa = float(input("Nhập điểm Hóa: "))
        if diem_hoa >= 0 and diem_hoa <= 10:
            break
        else:
            print("Điểm phải nằm trong khoảng từ 0 đến 10. Vui lòng nhập lại.")
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
    show_sv(sinh_vien_list)
        

def xoa_sinh_vien_theo_id():
    id_sinh_vien = input("Nhập ID sinh viên cần xóa: ")
    result = collection_sinh_vien.delete_one({"_id": ObjectId(id_sinh_vien)})
    if result.deleted_count > 0:
            print("Đã xóa sinh viên thành công.")
    else:
        print("Không tìm thấy sinh viên với ID đã nhập.")

def tim_kiem_sinh_vien_theo_ten_tuoi():
    ten = input("Nhập tên sinh viên cần tìm: ")
    while True:
        tuoi = input("Nhập tuổi sinh viên cần tìm: ")
        if tuoi.isdigit():
            tuoi = int(tuoi)
            break
        elif tuoi == "":
            tuoi = None
            break
        else:
            print("Tuổi phải là số. Vui lòng nhập lại.")
    quyery = {}
    if ten:
        quyery["ten"] = ten
    if tuoi:
        quyery["tuoi"] = tuoi
    sinh_vien_list = collection_sinh_vien.find(quyery)
    show_sv(sinh_vien_list)

def tim_kiem_sinh_vien_diem_mon_lon_hon():
    mon = input("Nhập tên môn học (toan, ly, hoa): ")
    diem = float(input(f"Nhập điểm {mon} cần tìm: "))
    qery = {f"diem.{mon}": {"$gte": diem}} 
    sinh_vien_list = collection_sinh_vien.find(qery)
    show_sv(sinh_vien_list)

def tim_kiem_sinh_vien_tong_diem_lon_hon():
    tong_diem = float(input("Nhập tổng điểm cần tìm: "))
    sinh_vien = collection_sinh_vien.find()
    sinh_vien_list = []
    for sv in sinh_vien:
        if "diem" in sv:
            diem = sv["diem"]
            if (diem["toan"] + diem["ly"] + diem["hoa"]) > tong_diem:
                sinh_vien_list.append(sv)
    show_sv(sinh_vien_list)

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
        try:
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
        except KeyboardInterrupt:
            print("\nChương trình đã bị dừng bởi người dùng.")
            break
if __name__ == "__main__":
    menu()
