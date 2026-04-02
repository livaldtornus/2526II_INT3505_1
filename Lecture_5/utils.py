import math
import base64
from flask import jsonify

def success_response(data, message="Success", metadata=None):
    """Chuẩn hóa wrapper cho thành công"""
    res = {
        "status": "success",
        "message": message,
        "data": data
    }
    if metadata:
        res["metadata"] = metadata
    return jsonify(res)

def error_response(message="Error", code=400):
    """Chuẩn hóa wrapper cho lỗi"""
    return jsonify({
        "status": "error",
        "message": message
    }), code


def paginate_offset(data, page, per_page):
    """Offset/Limit Pagination"""
    total = len(data)
    total_pages = math.ceil(total / per_page) if per_page > 0 else 0
    offset = (page - 1) * per_page
    items = data[offset:offset + per_page]
    
    return items, {
        "pagination": {
            "type": "offset",
            "page": page,
            "per_page": per_page,
            "total_items": total,
            "total_pages": total_pages,
            "has_next": page < total_pages,
            "has_prev": page > 1,
            "next_page": page + 1 if page < total_pages else None,
            "prev_page": page - 1 if page > 1 else None,
        }
    }

def paginate_cursor(data, cursor_str, limit):
    """Cursor-based Pagination (dùng ID làm cursor)"""
    start_idx = 0
    if cursor_str:
        try:
            cursor_id = int(base64.b64decode(cursor_str).decode())
            # Giả định data đã có thuộc tính 'id' (do đã là dataclass hoặc dict)
            for i, item in enumerate(data):
                item_id = item.id if hasattr(item, 'id') else item["id"]
                if item_id == cursor_id:
                    start_idx = i + 1
                    break
        except Exception:
            pass # Invalid cursor handled gracefully

    items = data[start_idx:start_idx + limit]
    
    next_cursor = None
    if start_idx + limit < len(data):
        next_item = data[start_idx + limit - 1]
        next_id = next_item.id if hasattr(next_item, 'id') else next_item["id"]
        next_cursor = base64.b64encode(str(next_id).encode()).decode()

    prev_cursor = None
    if start_idx > 0:
        prev_start = max(0, start_idx - limit)
        prev_item = data[prev_start] if prev_start > 0 else None
        if prev_item:
            prev_id = prev_item.id if hasattr(prev_item, 'id') else prev_item["id"]
            prev_cursor = base64.b64encode(str(prev_id).encode()).decode()

    return items, {
        "pagination": {
            "type": "cursor",
            "limit": limit,
            "total_items": len(data),
            "next_cursor": next_cursor,
            "prev_cursor": prev_cursor,
            "has_next": next_cursor is not None,
            "has_prev": start_idx > 0,
        }
    }

def paginate_page_based(data, page_number, page_size):
    """Page-based Pagination"""
    total = len(data)
    total_pages = math.ceil(total / page_size) if page_size > 0 else 0
    page_number = max(1, min(page_number, total_pages or 1))
    start = (page_number - 1) * page_size
    items = data[start:start + page_size]
    
    pages_range = list(range(max(1, page_number - 2), min(total_pages + 1, page_number + 3)))
    
    return items, {
        "pagination": {
            "type": "page-based",
            "current_page": page_number,
            "page_size": page_size,
            "total_items": total,
            "total_pages": total_pages,
            "pages": pages_range,
            "is_first": page_number == 1,
            "is_last": page_number == total_pages,
        }
    }
