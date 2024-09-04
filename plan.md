### Web Application Functional Requirements

**Purpose**:  
The application is designed to enable users to easily view, manipulate, and manage data stored in a database table. The app’s primary functions involve interacting with the data in a user-friendly manner, allowing modifications through a web interface.

### Key Features

1. **CSV File Upload**:  
   Users should be able to upload a CSV file that serves as the initial source for the data. The contents of the CSV file will be used to create and populate a single table in the underlying database. The uploaded file will determine the structure of the table (i.e., columns will be derived from the headers in the CSV, and rows will reflect the data).

2. **View Data**:  
   After uploading the CSV file, the data from the created table should be displayed in a tabular format. The interface should allow the user to visually inspect the contents of the table easily.

3. **Update a Row**:  
   Users should have the ability to modify the content of any row within the table. The interface should allow users to select a row, edit the data within the fields, and save the changes back to the database.

4. **Delete a Row**:  
   The application should provide functionality to delete a row of data from the table. Upon selecting a row, users can choose to delete it, and the application will remove the corresponding record from the database.

5. **Download Table Data**:  
   The user should be able to download the entire table as a CSV file at any time. The downloaded CSV should reflect the current state of the table, including any updates or deletions made by the user.

### Constraints

- **Single Table**: The application will work with a single table. Once the CSV has been uploaded and the table initialized, the application will not allow for deletion or overwriting of the table.
- **No Table Overwrites**: After the initial upload of a CSV file, no further table creation or overwriting will be allowed. The users can only modify the existing rows or delete them.
