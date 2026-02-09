from typing import List, Dict, Any
from db import get_db_connection
import crud

class DBService:
    def __init__(self):
        print("[DBService] Initializing...")

    def search_structured(self, query: str) -> Dict[str, Any]:
        """정형 데이터(SQL) 검색 - 키워드 기반 간이 검색"""
        conn = get_db_connection()
        results = {"employees": [], "sales": [], "leaves": []}
        try:
            # 1. 직원 검색
            all_employees = crud.list_employees(conn)
            for emp in all_employees:
                if query in emp['name'] or query in emp['dept']:
                    results["employees"].append(emp)
                    
            # 2. 매출 검색
            all_sales = crud.list_sales(conn, limit=100)
            for sale in all_sales:
                if query in sale['dept'] or (sale['description'] and query in sale['description']):
                    results["sales"].append(sale)
                    
            # 3. 휴가 검색 (검색된 직원이 있는 경우에만 관련 휴가 조회)
            if results["employees"]:
                for emp in results["employees"]:
                    leave = crud.get_leave_by_employee(conn, emp['id'])
                    if leave:
                        results["leaves"].append({
                            "employee_name": emp['name'], 
                            "total": leave['total'], 
                            "used": leave['used'], 
                            "remaining": leave['remaining']
                        })
        finally:
            conn.close()
        return results

# 싱글톤 인스턴스
db_service = DBService()
