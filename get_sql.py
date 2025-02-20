import re

def parse_records(raw_data):
    """
    将原始数据按照空行分割成记录，并解析每一行的“键: 值”
    """
    # 按照一个或多个空行分割记录
    records = re.split(r'\n\s*\n', raw_data.strip())
    parsed_records = []
    for record in records:
        record_data = {}
        # 按行分割每条记录
        lines = record.strip().splitlines()
        for line in lines:
            # 使用正则表达式匹配键和值，支持“：”或“:”分隔
            match = re.match(r'^\s*(.+?)[：:]\s*(.*)$', line)
            if match:
                key = match.group(1).strip()
                value = match.group(2).strip()
                record_data[key] = value
        parsed_records.append(record_data)
    return parsed_records

def process_record(record):
    """
    对每条记录做进一步处理，比如：
    - 将“年份”转换为 int
    - 从“专业招生人数”中提取数字
    - 将“学费”和“录取最低分”转换为 int（若存在）
    """
    processed = {}
    
    # 年份
    processed['year'] = int(record.get('年份', 0)) if record.get('年份') else None
    # 本科专业
    processed['undergraduate_major'] = record.get('本科专业', '')
    # 院校名称
    processed['institution_name'] = record.get('院校名称', '')
    # 联合培养学校
    processed['joint_training_school'] = record.get('联合培养学校', '')
    
    # 专业招生人数：例如 "40人 展开详情"，提取其中的数字
    enrollment = record.get('专业招生人数', '')
    num_match = re.search(r'(\d+)', enrollment)
    processed['enrollment'] = int(num_match.group(1)) if num_match else None
    
    # 考试科目
    processed['exam_subjects'] = record.get('考试科目', '')
    
    # 学费：如果值为纯数字则转换为 int，否则置为 None
    tuition = record.get('学费', '')
    processed['tuition'] = int(tuition) if tuition.isdigit() else None
    
    # 录取最低分：同样处理
    lowest_score = record.get('录取最低分', '')
    processed['lowest_score'] = int(lowest_score) if lowest_score.isdigit() else None

    return processed

def sql_escape(s):
    """
    简单转义 SQL 中的单引号
    """
    return s.replace("'", "''")

def generate_sql(processed_records):
    """
    根据处理后的记录生成 SQL 语句，包括建表语句和插入语句
    """
    sql_statements = []
    
    # 1. 创建表格的 SQL 语句
    create_table_sql = """DROP TABLE IF EXISTS university_admissions;

CREATE TABLE university_admissions (
  id INT AUTO_INCREMENT PRIMARY KEY,
  year INT COMMENT '年份',
  undergraduate_major VARCHAR(100) COMMENT '本科专业',
  institution_name VARCHAR(200) COMMENT '院校名称',
  joint_training_school VARCHAR(200) COMMENT '联合培养学校',
  enrollment INT COMMENT '专业招生人数',
  exam_subjects TEXT COMMENT '考试科目',
  tuition INT COMMENT '学费',
  lowest_score INT COMMENT '录取最低分'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;"""
    sql_statements.append(create_table_sql)
    
    # 2. 插入语句
    insert_prefix = "INSERT INTO university_admissions (year, undergraduate_major, institution_name, joint_training_school, enrollment, exam_subjects, tuition, lowest_score) VALUES\n"
    rows = []
    for record in processed_records:
        year = record['year'] if record['year'] is not None else 'NULL'
        ug_major = f"'{sql_escape(record['undergraduate_major'])}'" if record['undergraduate_major'] else "''"
        inst_name = f"'{sql_escape(record['institution_name'])}'" if record['institution_name'] else "''"
        joint_training = f"'{sql_escape(record['joint_training_school'])}'" if record['joint_training_school'] else "''"
        enrollment = record['enrollment'] if record['enrollment'] is not None else 'NULL'
        exam_subjects = f"'{sql_escape(record['exam_subjects'])}'" if record['exam_subjects'] else "''"
        tuition = record['tuition'] if record['tuition'] is not None else 'NULL'
        lowest_score = record['lowest_score'] if record['lowest_score'] is not None else 'NULL'
        
        row = f"({year}, {ug_major}, {inst_name}, {joint_training}, {enrollment}, {exam_subjects}, {tuition}, {lowest_score})"
        rows.append(row)
    insert_sql = insert_prefix + ",\n".join(rows) + ";"
    sql_statements.append(insert_sql)
    
    return "\n\n".join(sql_statements)

def main():
    # 从 raw.txt 中读取原始数据（请确保 raw.txt 与该脚本在同一目录下）
    with open("raw.txt", "r", encoding="utf-8") as infile:
        raw_data = infile.read()
    
    # 解析原始数据
    records = parse_records(raw_data)
    # 对每条记录做后续数据处理
    processed_records = [process_record(record) for record in records]
    
    # 生成 SQL 语句
    sql_content = generate_sql(processed_records)
    
    # 将生成的 SQL 语句保存到 raw.sql 文件中
    with open("raw.sql", "w", encoding="utf-8") as outfile:
        outfile.write(sql_content)
    
    print("SQL 语句已生成并保存至 raw.sql")

if __name__ == "__main__":
    main()
