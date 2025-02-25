## 中文版

# OCR 到 SQL 转换流程

本流程展示了如何从截图获取数据，经过 OCR 识别和 SQL 转换，最终将数据导入到 MySQL 数据库中。

### 流程步骤

1. **获取截图**
   - 首先，截取需要处理的图片或扫描件，确保截图清晰，文字易于识别。

2. **运行 `dp_ocr`**
   - 使用 `dp_ocr` 工具对截图进行 OCR 处理，生成文本文件 `raw.txt`。

3. **替换 `raw.txt` 中的“年份”**
   - 打开 `raw.txt` 文件，将文件中的“年份”替换为“换行（\n）+年份”。这一步骤可以确保文件格式正确，便于后续的 SQL 生成。

4. **运行 `get_sql`**
   - 运行 `get_sql` 工具，将格式化后的 `raw.txt` 转换为 SQL 文件 `raw.sql`。

5. **执行 SQL**
   - 将 `raw.sql` 中的 SQL 语句复制到 MySQL 中并执行，数据将被成功导入数据库。

## English Version

# OCR to SQL Conversion Workflow

This workflow demonstrates how to extract data from a screenshot, process it through OCR recognition, convert it to SQL, and then import the data into a MySQL database.

### Steps in the Process

1. **Obtain a Screenshot**
   - Start by taking a screenshot or scanning the document you need to process. Ensure the image is clear and the text is easy to recognize.

2. **Run `dp_ocr`**
   - Use the `dp_ocr` tool to perform OCR on the screenshot, generating the `raw.txt` text file.

3. **Replace "Year" in `raw.txt`**
   - Open the `raw.txt` file and replace the occurrences of "Year" with a newline (`\n`) followed by "Year". This ensures the file is formatted correctly for SQL generation.

4. **Run `get_sql`**
   - Run the `get_sql` tool to convert the formatted `raw.txt` into an SQL file (`raw.sql`).

5. **Execute SQL**
   - Copy the SQL statements from the `raw.sql` file and run them in MySQL to import the data into the database.

这样就完成了 OCR 转换到 SQL 的整个流程！



















