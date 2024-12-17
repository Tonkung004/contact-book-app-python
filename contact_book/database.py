from typing import List
import datetime
from contact_book.model import Contact
from contact_book import db, ContactQuery


def create(contact: Contact) -> None:
    # กำหนดตำแหน่งให้กับผู้ติดต่อใหม่
    contact.position = len(db) + 1
    
    # ตรวจสอบว่า employee_id เป็น list หรือไม่
    employee_id = contact.employee_id
    if isinstance(employee_id, list):
        employee_id = ''.join(employee_id)  # แปลงเป็น string หากเป็น list
    
    # สร้าง dictionary สำหรับผู้ติดต่อใหม่
    new_contact = {
        'employee_id': employee_id,  # ใช้ employee_id ที่แปลงแล้ว
        'name': contact.name,
        'department': contact.department,
        'contact_number': contact.contact_number,
        'position': contact.position,
        'date_created': contact.date_created,
        'date_updated': contact.date_updated
    }
    
    # เพิ่มผู้ติดต่อใหม่ลงในฐานข้อมูล
    db.insert(new_contact)


def read() -> List[Contact]:
    # อ่านข้อมูลทั้งหมดจากฐานข้อมูล
    results = db.all()
    contacts = []
    
    # สร้าง list ของ Contact objects จากข้อมูลที่อ่านได้
    for result in results:
        # ตรวจสอบว่า employee_id เป็น list หรือไม่
        employee_id = result.get('employee_id', '')
        if isinstance(employee_id, list):  # ถ้าเป็น list
            employee_id = ''.join(employee_id)  # แปลงให้เป็น string
        
        # ตรวจสอบว่า 'department' มีอยู่ในผลลัพธ์หรือไม่
        department = result.get('department', 'N/A')  # กำหนดค่า default ถ้าไม่มี 'department'
        
        new_contact = Contact(employee_id, result['name'], department, result['contact_number'],
                              result['position'], result['date_created'], result['date_updated'])
        contacts.append(new_contact)
    
    return contacts


def update(position: int, name: str = None, department: str = None, contact_number: str = None, employee_id: str = None) -> None:
    # อ่านข้อมูลเดิมจากฐานข้อมูลก่อน
    current_contact = db.get(ContactQuery.position == position)
    
    # ถ้าค่าที่กรอกไม่ใช่ None ให้ใช้ค่าที่กรอก
    update_data = {}
    
    if name is not None:
        update_data['name'] = name
    else:
        update_data['name'] = current_contact['name']  # ถ้าไม่กรอกชื่อใหม่, ใช้ชื่อเดิม

    if department is not None:
        update_data['department'] = department
    else:
        update_data['department'] = current_contact['department']  # ใช้แผนกเดิม

    if contact_number is not None:
        update_data['contact_number'] = contact_number
    else:
        update_data['contact_number'] = current_contact['contact_number']  # ใช้หมายเลขเดิม

    if employee_id is not None:
        update_data['employee_id'] = employee_id
    else:
        update_data['employee_id'] = current_contact['employee_id']  # ใช้ employee_id เดิม
    
    # เพิ่มการอัปเดตวันที่เวลาปัจจุบัน
    update_data['date_updated'] = datetime.datetime.now().isoformat()
    
    # ตรวจสอบว่า dictionary update_data มีข้อมูลหรือไม่
    if update_data:
        db.update(update_data, ContactQuery.position == position)


def delete(position: int) -> None:
    # ตรวจสอบว่ามี contact ในตำแหน่งที่ระบุหรือไม่
    current_contact = db.get(ContactQuery.position == position)
    if current_contact is None:
        print(f"Invalid position: {position}")
        return

    # ลบผู้ติดต่อที่ตำแหน่งนี้
    db.remove(ContactQuery.position == position)

    # ปรับตำแหน่งของผู้ติดต่อที่เหลือ
    contacts = db.all()  # ดึงข้อมูลผู้ติดต่อทั้งหมดหลังจากลบ
    for index, contact in enumerate(contacts, start=1):
        db.update({'position': index}, ContactQuery.position == contact['position'])


def change_position(old_position: int, new_position: int) -> None:
    # ปรับตำแหน่งของผู้ติดต่อ
    db.update({'position': new_position}, ContactQuery.position == old_position)
