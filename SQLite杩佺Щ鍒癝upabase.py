"""将旧版思维罗盘 SQLite 数据迁移到 Supabase。

运行前：
1. pip install supabase
2. 设置环境变量 SUPABASE_URL、SUPABASE_SERVICE_ROLE_KEY
3. 将旧数据库文件 sixiangluopan.db 放在本脚本同一目录，或通过第一个参数指定路径
4. 先在 Supabase SQL Editor 执行 supabase_schema.sql
5. python SQLite迁移到Supabase.py [sixiangluopan.db]

脚本按原 id 迁移学生和测评记录，避免历史记录关联错位。建议迁移前先备份数据库。
"""
import json
import os
import sqlite3
import sys
from pathlib import Path
from supabase import create_client


def decode_json(value, default):
    if value is None or value == "":
        return default
    if isinstance(value, (dict, list)):
        return value
    try:
        return json.loads(value)
    except Exception:
        return default


def chunks(items, size=500):
    for i in range(0, len(items), size):
        yield items[i:i + size]


def main():
    db_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).with_name("sixiangluopan.db")
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
    if not db_path.exists():
        raise SystemExit(f"找不到 SQLite 数据库文件：{db_path}\n请先从旧运行环境取得 sixiangluopan.db。")
    if not url or not key:
        raise SystemExit("请先设置 SUPABASE_URL 和 SUPABASE_SERVICE_ROLE_KEY 环境变量。")

    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    students = [dict(r) for r in conn.execute("select * from students order by id")]
    assessments = [dict(r) for r in conn.execute("select * from assessments order by id")]
    conn.close()

    client = create_client(url, key)
    for batch in chunks(students):
        client.table("students").upsert(batch, on_conflict="id").execute()
    print(f"学生档案迁移完成：{len(students)} 条")

    converted = []
    for row in assessments:
        converted.append({
            "id": row["id"],
            "student_id": row["student_id"],
            "assessed_at": row["assessed_at"],
            "overall": row["overall"],
            "dim_scores": decode_json(row.get("dim_scores"), {}),
            "answers": decode_json(row.get("answers"), {}),
            "report": row.get("report") or "",
            "report_source": row.get("report_source") or "",
        })
    for batch in chunks(converted):
        client.table("assessments").upsert(batch, on_conflict="id").execute()
    print(f"测评记录迁移完成：{len(converted)} 条")
    print("迁移完成。请在 Supabase SQL Editor 执行以下语句，校准自增编号：")
    print("select setval(pg_get_serial_sequence('public.students','id'), coalesce(max(id), 1), max(id) is not null) from public.students;")
    print("select setval(pg_get_serial_sequence('public.assessments','id'), coalesce(max(id), 1), max(id) is not null) from public.assessments;")


if __name__ == "__main__":
    main()
