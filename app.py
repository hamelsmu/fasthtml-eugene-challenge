from fasthtml.common import *
import csv
import io
from fastlite import database
from starlette.responses import FileResponse, StreamingResponse
import pandas as pd

app, rt = fast_app()

# Initialize database
db = database('data.db')
table = db.t.csv_data

# Helper function to check if table exists
def table_exists():
    return 'csv_data' in db.t

@rt("/")
def get():
    if not table_exists():
        return Titled("CSV Data Manager", 
            Form(
                Input(type="file", name="csv_file", accept=".csv"),
                Button("Upload CSV", type="submit"),
                action="/upload", method="post", enctype="multipart/form-data"
            )
        )
    else:
        data = db.q(f"select * from {db.t.csv_data}")
        headers = data[0].keys() if data else []
        return Titled("CSV Data Manager",
            Div(
                Div(
                    A(Button("Download CSV", hx_swap="none"), href="/download"),
                    style="position: sticky; top: 0; padding: 10px; z-index: 1000;"
                ),
                Table(
                    Tr(*[Th(header) for header in headers]),
                    *[Tr(*[Td(row[header]) for header in headers],
                        Td(Button("Edit", hx_get=f"/edit/{row['id']}", hx_target=f"#row-{row['id']}")),
                        Td(Button("Delete", hx_delete=f"/delete/{row['id']}", hx_target=f"#row-{row['id']}")),
                        id=f"row-{row['id']}"
                    ) for row in data]
                )
            )
        )

@rt("/upload")
def post(csv_file: UploadFile):
    print("Received file:", csv_file)
    if not csv_file:
        print("No file uploaded")
        return "No file uploaded", 400
    
    print("File name:", csv_file.filename)
    print("Content type:", csv_file.content_type)
    
    if not table_exists():
        try:
            content = csv_file.file.read().decode('utf-8')
            csv_data = csv.DictReader(io.StringIO(content))
            headers = csv_data.fieldnames
            if not headers:
                return "CSV file is empty or has no headers", 400
            table.create(**{header: str for header in headers}, pk='id')
            for row in csv_data:
                table.insert(row)
        except Exception as e:
            return f"Error processing CSV file: {str(e)}", 400
    return RedirectResponse("/", status_code=303)

@rt("/edit/{id}")
def get(id: int):
    row = table[id]
    return Form(
        *[Input(name=key, value=value) for key, value in row.items() if key != 'id'],
        Button("Save", type="submit"),
        hx_put=f"/update/{id}", hx_target=f"#row-{id}"
    )

@rt("/update/{id}")
def put(id: int, **data):
    table.update(data, id)
    updated_row = table[id]
    return Tr(*[Td(updated_row[key]) for key in updated_row.keys() if key != 'id'],
        Td(Button("Edit", hx_get=f"/edit/{id}", hx_target=f"#row-{id}")),
        Td(Button("Delete", hx_delete=f"/delete/{id}", hx_target=f"#row-{id}")),
        id=f"row-{id}"
    )

@rt("/delete/{id}")
def delete(id: int):
    table.delete(id)
    return ""

@rt("/download")
def get():
    print("Download route called")
    data = db.q(f"select * from {db.t.csv_data}")
    print(f"Data retrieved: {len(data)} rows")
    if not data:
        return "No data to download"
    
    # Convert data to pandas DataFrame
    df = pd.DataFrame(data)
    
    # Save DataFrame to CSV
    csv_path = "csv_data.csv"
    df.to_csv(csv_path, index=False)
    
    # Return FileResponse
    return FileResponse(csv_path, media_type="text/csv", filename="csv_data.csv")

serve()