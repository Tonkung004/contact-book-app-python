import typer
from rich.console import Console
from rich.table import Table
from contact_book.model import Contact
from contact_book.database import create, read, update, delete

app = typer.Typer()
console = Console()

@app.command(short_help='adds a contact')
def add():
    """คำสั่งสำหรับกรอกข้อมูลและเพิ่มผู้ติดต่อ"""
    employee_id = typer.prompt("Enter the contact's employee ID")
    name = typer.prompt("Enter the contact's name")
    department = typer.prompt("Enter the contact's department")
    contact_number = typer.prompt("Enter the contact's phone number")

    # ตรวจสอบว่า employee_id เป็นตัวเลขหรือไม่
    if not employee_id.isdigit():
        console.print("[bold red]Employee ID must be a number![/bold red]")
        raise typer.Exit()

    if not name or not contact_number or not employee_id:
        console.print("[bold red]Name, Contact Number, and Employee ID cannot be empty![/bold red]")
        raise typer.Exit()

    contacts = read()  # อ่านข้อมูลผู้ติดต่อจากฐานข้อมูล
    position = len(contacts) + 1  # กำหนดตำแหน่งใหม่

    contact = Contact(employee_id=employee_id, name=name, department=department, contact_number=contact_number, position=position)

    create(contact)  # เพิ่มผู้ติดต่อใหม่ลงในฐานข้อมูล

    console.print(f"[bold green]Contact {name} added successfully![/bold green]")
    show()  # แสดงรายการผู้ติดต่อทั้งหมด

@app.command(short_help='shows all contacts')
def show():
    contacts = read()  # อ่านข้อมูลผู้ติดต่อทั้งหมดจากฐานข้อมูล

    console.print("[bold magenta]Contact Book[/bold magenta]", "📕")

    if len(contacts) == 0:
        console.print("[bold red]No contacts to show[/bold red]")
    else:
        table = Table(show_header=True, header_style="bold blue", show_lines=True)
        table.add_column("#", style="dim", width=3, justify="center")
        table.add_column("Employee ID", style="dim", width=12, justify="center")
        table.add_column("Name", min_width=20, justify="center")
        table.add_column("Department", min_width=12, justify="center")
        table.add_column("Contact Number", min_width=12, justify="center")
        table.add_column("Date Created", min_width=12, justify="center")
        table.add_column("Date Updated", min_width=12, justify="center")

        for contact in contacts:
            table.add_row(
                str(contact.position),
                f'[green]{contact.employee_id}[/green]', 
                f'[cyan]{contact.name}[/cyan]',
                f'[yellow]{contact.department}[/yellow]',
                f'[green]{contact.contact_number}[/green]',
                f'[yellow]{contact.date_created}[/yellow]',
                f'[yellow]{contact.date_updated}[/yellow]'
            )
        console.print(table)

@app.command(short_help='edits a contact')
def edit(position: int):
    """คำสั่งสำหรับแก้ไขข้อมูลผู้ติดต่อ"""
    
    contacts = read()  # อ่านข้อมูลผู้ติดต่อทั้งหมด
    contact = next((c for c in contacts if c.position == position), None)
    
    if contact is None:
        console.print("[bold red]Contact not found[/bold red]")
        return
    
    # ใช้ค่า default เฉพาะเมื่อผู้ใช้ไม่กรอกใหม่
    employee_id = typer.prompt(f"Enter the new employee ID for position {position} [Current: {contact.employee_id}]", default=contact.employee_id)
    name = typer.prompt(f"Enter the new name for position {position} [Current: {contact.name}]", default=contact.name) 
    department = typer.prompt(f"Enter the new department for position {position} [Current: {contact.department}]", default=contact.department)
    contact_number = typer.prompt(f"Enter the new contact number for position {position} [Current: {contact.contact_number}]", default=contact.contact_number)

    # ตรวจสอบว่าไม่มีข้อมูลว่างในชื่อหรือหมายเลขติดต่อ
    if not name or not contact_number:
        console.print("[bold red]Name and Contact Number cannot be empty![/bold red]")
        return

    # ตรวจสอบการเปลี่ยนแปลงจริง ๆ
    updated = False
    if name != contact.name:
        contact.name = name
        updated = True
    if contact_number != contact.contact_number:
        contact.contact_number = contact_number
        updated = True
    if employee_id != contact.employee_id:
        contact.employee_id = employee_id
        updated = True
    if department != contact.department:
        contact.department = department
        updated = True

    # แก้ไขฟังก์ชัน edit()
    if updated:
        # ส่งค่าที่ต้องการอัปเดตไปยังฟังก์ชัน update() แทนที่จะส่ง contact ทั้งอ็อบเจ็กต์
        update(position, employee_id=employee_id, name=name, department=department, contact_number=contact_number)
        console.print(f"[bold green]Contact at position {position} updated successfully![/bold green]")
    else:
        console.print("[bold yellow]No changes detected![/bold yellow]")

    show()  # แสดงข้อมูลหลังจากแก้ไข


@app.command(short_help='removes a contact')
def remove(position: int):
    """คำสั่งสำหรับลบผู้ติดต่อ"""
    contacts = read()  # อ่านข้อมูลผู้ติดต่อทั้งหมด
    contact = next((c for c in contacts if c.position == position), None)
    
    if contact is None:
        console.print(f"[bold red]No contact found at position {position}[/bold red]")
        return

    typer.echo(f"Removing contact at position {position}")
    delete(position)  # ลบผู้ติดต่อจากฐานข้อมูล
    show()  # แสดงข้อมูลหลังจากลบ

if __name__ == "__main__":
    app()  # เรียกใช้แอปพลิเคชัน
