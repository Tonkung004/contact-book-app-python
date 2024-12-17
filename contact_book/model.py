import datetime  # นำเข้า datetime เพื่อใช้ในการจัดการวันที่และเวลา

class Contact:
    def __init__(self, employee_id=None, name=None, department=None, contact_number=None, position=None, date_created=None, date_updated=None):
        # ตรวจสอบว่ามีการกำหนดข้อมูลพื้นฐานหรือไม่
        self.employee_id = employee_id or "N/A"  # ใช้ "N/A" หากไม่มีค่า employee_id
        self.name = name or "Unknown"  # ใช้ "Unknown" หากไม่มีชื่อ
        self.department = department or "N/A"  # ใช้ "N/A" หากไม่มีแผนก
        self.contact_number = str(contact_number) if contact_number is not None else "N/A"  # หากไม่มีหมายเลขติดต่อให้ใช้ "N/A"
        self.position = position if position is not None else 0  # กำหนดตำแหน่งเริ่มต้นเป็น 0
        # กำหนดวันที่สร้างและอัปเดตเป็นเวลาปัจจุบัน
        self.date_created = date_created if date_created is not None else datetime.datetime.now().isoformat()
        self.date_updated = date_updated if date_updated is not None else datetime.datetime.now().isoformat()

    def __repr__(self) -> str:
        return f"({self.employee_id}, {self.name}, {self.department}, {self.contact_number}, {self.position}, {self.date_created}, {self.date_updated})"
