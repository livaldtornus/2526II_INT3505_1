from flask import Flask, jsonify, request, abort
from flask_cors import CORS
from datetime import datetime, timedelta
import math
import base64
import json

app = Flask(__name__)
CORS(app)

# ============================================================
# MOCK DATA - Hệ thống quản lý thư viện
# ============================================================

GENRES = ["Fiction", "Non-Fiction", "Science", "History", "Technology", "Biography", "Fantasy", "Mystery"]

BOOKS = [
    {"id": 1, "title": "Clean Code", "author_id": 1, "isbn": "978-0132350884", "genre": "Technology", "year": 2008, "total_copies": 5, "available_copies": 3, "description": "A handbook of agile software craftsmanship", "tags": ["programming", "best-practices"]},
    {"id": 2, "title": "The Pragmatic Programmer", "author_id": 2, "isbn": "978-0135957059", "genre": "Technology", "year": 2019, "total_copies": 4, "available_copies": 2, "description": "Your journey to mastery", "tags": ["programming", "career"]},
    {"id": 3, "title": "Design Patterns", "author_id": 3, "isbn": "978-0201633610", "genre": "Technology", "year": 1994, "total_copies": 3, "available_copies": 3, "description": "Elements of reusable object-oriented software", "tags": ["programming", "architecture"]},
    {"id": 4, "title": "Dune", "author_id": 4, "isbn": "978-0441013593", "genre": "Fiction", "year": 1965, "total_copies": 6, "available_copies": 4, "description": "Epic science fiction novel set in the distant future", "tags": ["sci-fi", "epic"]},
    {"id": 5, "title": "Sapiens", "author_id": 5, "isbn": "978-0062316110", "genre": "History", "year": 2011, "total_copies": 4, "available_copies": 1, "description": "A Brief History of Humankind", "tags": ["history", "anthropology"]},
    {"id": 6, "title": "The Great Gatsby", "author_id": 6, "isbn": "978-0743273565", "genre": "Fiction", "year": 1925, "total_copies": 5, "available_copies": 5, "description": "The story of the mysteriously wealthy Jay Gatsby", "tags": ["classic", "american-literature"]},
    {"id": 7, "title": "A Brief History of Time", "author_id": 7, "isbn": "978-0553380163", "genre": "Science", "year": 1988, "total_copies": 3, "available_copies": 2, "description": "From the Big Bang to Black Holes", "tags": ["physics", "cosmology"]},
    {"id": 8, "title": "The Lean Startup", "author_id": 8, "isbn": "978-0307887894", "genre": "Technology", "year": 2011, "total_copies": 4, "available_copies": 0, "description": "How constant innovation creates radically successful businesses", "tags": ["startup", "business"]},
    {"id": 9, "title": "1984", "author_id": 9, "isbn": "978-0451524935", "genre": "Fiction", "year": 1949, "total_copies": 7, "available_copies": 5, "description": "A dystopian social science fiction novel", "tags": ["dystopia", "classic"]},
    {"id": 10, "title": "Thinking, Fast and Slow", "author_id": 10, "isbn": "978-0374533557", "genre": "Science", "year": 2011, "total_copies": 3, "available_copies": 2, "description": "How we think and make choices", "tags": ["psychology", "behavioral-economics"]},
    {"id": 11, "title": "The Hitchhiker's Guide to the Galaxy", "author_id": 11, "isbn": "978-0345391803", "genre": "Fiction", "year": 1979, "total_copies": 4, "available_copies": 3, "description": "A comedy science fiction series", "tags": ["sci-fi", "humor"]},
    {"id": 12, "title": "Atomic Habits", "author_id": 12, "isbn": "978-0735211292", "genre": "Non-Fiction", "year": 2018, "total_copies": 6, "available_copies": 4, "description": "An easy and proven way to build good habits", "tags": ["self-help", "productivity"]},
    {"id": 13, "title": "The Alchemist", "author_id": 13, "isbn": "978-0062315007", "genre": "Fiction", "year": 1988, "total_copies": 5, "available_copies": 3, "description": "A philosophical novel by Paulo Coelho", "tags": ["philosophy", "inspirational"]},
    {"id": 14, "title": "Educated", "author_id": 14, "isbn": "978-0399590504", "genre": "Biography", "year": 2018, "total_copies": 3, "available_copies": 2, "description": "A memoir about a survivalist family in Idaho", "tags": ["memoir", "education"]},
    {"id": 15, "title": "The Name of the Wind", "author_id": 15, "isbn": "978-0756404079", "genre": "Fantasy", "year": 2007, "total_copies": 4, "available_copies": 1, "description": "The tale of Kvothe the legendary wizard", "tags": ["fantasy", "magic"]},
    {"id": 16, "title": "Gone Girl", "author_id": 16, "isbn": "978-0307588371", "genre": "Mystery", "year": 2012, "total_copies": 4, "available_copies": 2, "description": "A psychological thriller novel", "tags": ["thriller", "mystery"]},
    {"id": 17, "title": "The Road", "author_id": 17, "isbn": "978-0307387899", "genre": "Fiction", "year": 2006, "total_copies": 3, "available_copies": 3, "description": "A post-apocalyptic novel", "tags": ["post-apocalyptic", "literary"]},
    {"id": 18, "title": "Steve Jobs", "author_id": 18, "isbn": "978-1451648539", "genre": "Biography", "year": 2011, "total_copies": 5, "available_copies": 4, "description": "The exclusive biography of Steve Jobs", "tags": ["biography", "technology", "business"]},
    {"id": 19, "title": "The Hobbit", "author_id": 19, "isbn": "978-0547928227", "genre": "Fantasy", "year": 1937, "total_copies": 6, "available_copies": 5, "description": "A fantasy novel by J. R. R. Tolkien", "tags": ["fantasy", "classic", "adventure"]},
    {"id": 20, "title": "Data Structures and Algorithms", "author_id": 20, "isbn": "978-0262033848", "genre": "Technology", "year": 2009, "total_copies": 4, "available_copies": 2, "description": "Introduction to algorithms", "tags": ["programming", "algorithms", "cs"]},
]

AUTHORS = [
    {"id": 1, "name": "Robert C. Martin", "nationality": "American", "bio": "Software engineer and author"},
    {"id": 2, "name": "David Thomas", "nationality": "British", "bio": "Software developer and author"},
    {"id": 3, "name": "Gang of Four", "nationality": "Various", "bio": "Erich Gamma, Richard Helm, Ralph Johnson, John Vlissides"},
    {"id": 4, "name": "Frank Herbert", "nationality": "American", "bio": "Science fiction author"},
    {"id": 5, "name": "Yuval Noah Harari", "nationality": "Israeli", "bio": "Historian and author"},
    {"id": 6, "name": "F. Scott Fitzgerald", "nationality": "American", "bio": "Novelist of the Jazz Age"},
    {"id": 7, "name": "Stephen Hawking", "nationality": "British", "bio": "Theoretical physicist and cosmologist"},
    {"id": 8, "name": "Eric Ries", "nationality": "American", "bio": "Entrepreneur and author"},
    {"id": 9, "name": "George Orwell", "nationality": "British", "bio": "Novelist and essayist"},
    {"id": 10, "name": "Daniel Kahneman", "nationality": "Israeli-American", "bio": "Psychologist and Nobel laureate"},
    {"id": 11, "name": "Douglas Adams", "nationality": "British", "bio": "Author and humorist"},
    {"id": 12, "name": "James Clear", "nationality": "American", "bio": "Author and speaker"},
    {"id": 13, "name": "Paulo Coelho", "nationality": "Brazilian", "bio": "Novelist"},
    {"id": 14, "name": "Tara Westover", "nationality": "American", "bio": "Author and historian"},
    {"id": 15, "name": "Patrick Rothfuss", "nationality": "American", "bio": "Fantasy author"},
    {"id": 16, "name": "Gillian Flynn", "nationality": "American", "bio": "Author and screenwriter"},
    {"id": 17, "name": "Cormac McCarthy", "nationality": "American", "bio": "Novelist"},
    {"id": 18, "name": "Walter Isaacson", "nationality": "American", "bio": "Biographer and journalist"},
    {"id": 19, "name": "J.R.R. Tolkien", "nationality": "British", "bio": "Author and philologist"},
    {"id": 20, "name": "Thomas H. Cormen", "nationality": "American", "bio": "Computer scientist"},
]

MEMBERS = [
    {"id": 1, "name": "Nguyen Van An", "email": "an.nguyen@email.com", "phone": "0901234567", "joined_date": "2023-01-15", "membership_type": "premium"},
    {"id": 2, "name": "Tran Thi Binh", "email": "binh.tran@email.com", "phone": "0912345678", "joined_date": "2023-03-20", "membership_type": "standard"},
    {"id": 3, "name": "Le Van Cuong", "email": "cuong.le@email.com", "phone": "0923456789", "joined_date": "2022-11-10", "membership_type": "premium"},
    {"id": 4, "name": "Pham Thi Dung", "email": "dung.pham@email.com", "phone": "0934567890", "joined_date": "2024-01-05", "membership_type": "standard"},
    {"id": 5, "name": "Hoang Van Em", "email": "em.hoang@email.com", "phone": "0945678901", "joined_date": "2023-07-22", "membership_type": "student"},
]

LOANS = [
    {"id": 1, "book_id": 8, "member_id": 1, "loan_date": "2024-01-10", "due_date": "2024-01-24", "return_date": None, "status": "active"},
    {"id": 2, "book_id": 5, "member_id": 2, "loan_date": "2024-01-08", "due_date": "2024-01-22", "return_date": None, "status": "overdue"},
    {"id": 3, "book_id": 15, "member_id": 3, "loan_date": "2024-01-12", "due_date": "2024-01-26", "return_date": None, "status": "active"},
    {"id": 4, "book_id": 1, "member_id": 1, "loan_date": "2023-12-01", "due_date": "2023-12-15", "return_date": "2023-12-14", "status": "returned"},
    {"id": 5, "book_id": 4, "member_id": 4, "loan_date": "2024-01-05", "due_date": "2024-01-19", "return_date": "2024-01-18", "status": "returned"},
    {"id": 6, "book_id": 12, "member_id": 5, "loan_date": "2024-01-14", "due_date": "2024-01-28", "return_date": None, "status": "active"},
    {"id": 7, "book_id": 2, "member_id": 2, "loan_date": "2023-11-20", "due_date": "2023-12-04", "return_date": "2023-12-03", "status": "returned"},
    {"id": 8, "book_id": 9, "member_id": 3, "loan_date": "2023-12-15", "due_date": "2023-12-29", "return_date": "2023-12-28", "status": "returned"},
]

REVIEWS = [
    {"id": 1, "book_id": 1, "member_id": 1, "rating": 5, "comment": "Must-read for every developer", "created_at": "2024-01-10T10:30:00"},
    {"id": 2, "book_id": 1, "member_id": 2, "rating": 4, "comment": "Great insights on clean coding practices", "created_at": "2024-01-12T14:20:00"},
    {"id": 3, "book_id": 5, "member_id": 3, "rating": 5, "comment": "Changed my perspective on human history", "created_at": "2024-01-08T09:15:00"},
    {"id": 4, "book_id": 9, "member_id": 4, "rating": 5, "comment": "Timeless classic, still relevant today", "created_at": "2024-01-05T16:45:00"},
    {"id": 5, "book_id": 12, "member_id": 5, "rating": 4, "comment": "Practical advice for habit formation", "created_at": "2024-01-14T11:00:00"},
    {"id": 6, "book_id": 19, "member_id": 1, "rating": 5, "comment": "A journey worth taking", "created_at": "2023-12-20T13:30:00"},
]

# ============================================================
# HELPER FUNCTIONS
# ============================================================

def paginate_offset(data, page, per_page):
    """Offset/Limit Pagination"""
    total = len(data)
    total_pages = math.ceil(total / per_page)
    offset = (page - 1) * per_page
    items = data[offset:offset + per_page]
    
    return {
        "data": items,
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


def paginate_cursor(data, cursor, limit):
    """Cursor-based Pagination (dùng ID làm cursor)"""
    # Decode cursor: cursor là ID của item cuối cùng đã thấy
    start_idx = 0
    if cursor:
        try:
            cursor_id = int(base64.b64decode(cursor).decode())
            for i, item in enumerate(data):
                if item["id"] == cursor_id:
                    start_idx = i + 1
                    break
        except Exception:
            abort(400, description="Invalid cursor")

    items = data[start_idx:start_idx + limit]
    
    next_cursor = None
    if start_idx + limit < len(data):
        next_id = data[start_idx + limit - 1]["id"]
        next_cursor = base64.b64encode(str(next_id).encode()).decode()

    prev_cursor = None
    if start_idx > 0:
        prev_start = max(0, start_idx - limit)
        prev_id = data[prev_start]["id"] if prev_start > 0 else None
        prev_cursor = base64.b64encode(str(prev_id).encode()).decode() if prev_id else None

    return {
        "data": items,
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
    """Page-based Pagination (giống offset nhưng tập trung vào số trang)"""
    total = len(data)
    total_pages = math.ceil(total / page_size)
    page_number = max(1, min(page_number, total_pages or 1))
    start = (page_number - 1) * page_size
    items = data[start:start + page_size]
    
    # Tạo danh sách page numbers để hiển thị
    pages_range = list(range(max(1, page_number - 2), min(total_pages + 1, page_number + 3)))
    
    return {
        "data": items,
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


def enrich_book(book):
    """Thêm thông tin author vào book"""
    b = dict(book)
    author = next((a for a in AUTHORS if a["id"] == book["author_id"]), None)
    b["author"] = author["name"] if author else "Unknown"
    avg_rating = None
    book_reviews = [r for r in REVIEWS if r["book_id"] == book["id"]]
    if book_reviews:
        avg_rating = round(sum(r["rating"] for r in book_reviews) / len(book_reviews), 1)
    b["avg_rating"] = avg_rating
    b["review_count"] = len(book_reviews)
    return b


def filter_books(query=None, genre=None, author_name=None, available=None, year_from=None, year_to=None, tag=None):
    """Filter books theo nhiều tiêu chí"""
    results = list(BOOKS)
    
    if query:
        q = query.lower()
        results = [b for b in results if q in b["title"].lower() or q in b["description"].lower()]
    
    if genre:
        results = [b for b in results if b["genre"].lower() == genre.lower()]
    
    if author_name:
        matching_author_ids = [a["id"] for a in AUTHORS if author_name.lower() in a["name"].lower()]
        results = [b for b in results if b["author_id"] in matching_author_ids]
    
    if available is not None:
        if available:
            results = [b for b in results if b["available_copies"] > 0]
        else:
            results = [b for b in results if b["available_copies"] == 0]
    
    if year_from:
        results = [b for b in results if b["year"] >= int(year_from)]
    
    if year_to:
        results = [b for b in results if b["year"] <= int(year_to)]
    
    if tag:
        results = [b for b in results if tag.lower() in b["tags"]]
    
    return results


# ============================================================
# ROUTES: BOOKS (Resource Tree)
# ============================================================

@app.route("/api/v1/books", methods=["GET"])
def get_books():
    """
    GET /api/v1/books
    Lấy danh sách sách với 3 kiểu pagination:
    - ?pagination=offset&page=1&per_page=5
    - ?pagination=cursor&cursor=<token>&limit=5
    - ?pagination=page&page_number=1&page_size=5
    Filters: q, genre, author, available, year_from, year_to, tag
    Sort: sort_by (title|year|author), order (asc|desc)
    """
    # --- Filters ---
    q         = request.args.get("q")
    genre     = request.args.get("genre")
    author    = request.args.get("author")
    available = request.args.get("available")
    year_from = request.args.get("year_from")
    year_to   = request.args.get("year_to")
    tag       = request.args.get("tag")

    if available is not None:
        available = available.lower() in ("true", "1", "yes")

    filtered = filter_books(q, genre, author, available, year_from, year_to, tag)
    enriched = [enrich_book(b) for b in filtered]

    # --- Sort ---
    sort_by = request.args.get("sort_by", "id")
    order   = request.args.get("order", "asc")
    if sort_by in ("title", "year", "author", "id"):
        enriched.sort(key=lambda b: b.get(sort_by, ""), reverse=(order == "desc"))

    # --- Pagination ---
    pagination_type = request.args.get("pagination", "offset")
    
    if pagination_type == "cursor":
        cursor = request.args.get("cursor")
        limit  = int(request.args.get("limit", 5))
        result = paginate_cursor(enriched, cursor, limit)
    
    elif pagination_type == "page":
        page_number = int(request.args.get("page_number", 1))
        page_size   = int(request.args.get("page_size", 5))
        result = paginate_page_based(enriched, page_number, page_size)
    
    else:  # offset (default)
        page     = int(request.args.get("page", 1))
        per_page = int(request.args.get("per_page", 5))
        result   = paginate_offset(enriched, page, per_page)

    result["filters_applied"] = {
        "q": q, "genre": genre, "author": author,
        "available": available, "year_from": year_from,
        "year_to": year_to, "tag": tag,
    }
    result["sort"] = {"sort_by": sort_by, "order": order}
    return jsonify(result)


@app.route("/api/v1/books/<int:book_id>", methods=["GET"])
def get_book(book_id):
    """GET /api/v1/books/:id — Chi tiết 1 quyển sách"""
    book = next((b for b in BOOKS if b["id"] == book_id), None)
    if not book:
        abort(404, description=f"Book with id={book_id} not found")
    
    enriched = enrich_book(book)
    enriched["reviews"] = [r for r in REVIEWS if r["book_id"] == book_id]
    author = next((a for a in AUTHORS if a["id"] == book["author_id"]), None)
    enriched["author_detail"] = author
    return jsonify(enriched)


@app.route("/api/v1/books/<int:book_id>/reviews", methods=["GET"])
def get_book_reviews(book_id):
    """GET /api/v1/books/:id/reviews — Reviews của 1 quyển sách"""
    book = next((b for b in BOOKS if b["id"] == book_id), None)
    if not book:
        abort(404, description=f"Book {book_id} not found")
    
    reviews = [r for r in REVIEWS if r["book_id"] == book_id]
    page     = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 5))
    return jsonify(paginate_offset(reviews, page, per_page))


@app.route("/api/v1/books/<int:book_id>/loans", methods=["GET"])
def get_book_loans(book_id):
    """GET /api/v1/books/:id/loans — Lịch sử mượn sách"""
    book = next((b for b in BOOKS if b["id"] == book_id), None)
    if not book:
        abort(404, description=f"Book {book_id} not found")
    
    loans = [l for l in LOANS if l["book_id"] == book_id]
    for loan in loans:
        member = next((m for m in MEMBERS if m["id"] == loan["member_id"]), None)
        loan = dict(loan)
        loan["member_name"] = member["name"] if member else "Unknown"
    return jsonify({"book_id": book_id, "loan_history": loans, "total_loans": len(loans)})


# ============================================================
# ROUTES: AUTHORS
# ============================================================

@app.route("/api/v1/authors", methods=["GET"])
def get_authors():
    """GET /api/v1/authors"""
    page     = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 10))
    return jsonify(paginate_offset(AUTHORS, page, per_page))


@app.route("/api/v1/authors/<int:author_id>", methods=["GET"])
def get_author(author_id):
    """GET /api/v1/authors/:id"""
    author = next((a for a in AUTHORS if a["id"] == author_id), None)
    if not author:
        abort(404, description=f"Author {author_id} not found")
    return jsonify(author)


@app.route("/api/v1/authors/<int:author_id>/books", methods=["GET"])
def get_author_books(author_id):
    """GET /api/v1/authors/:id/books — Sách của 1 tác giả"""
    author = next((a for a in AUTHORS if a["id"] == author_id), None)
    if not author:
        abort(404, description=f"Author {author_id} not found")
    
    books = [enrich_book(b) for b in BOOKS if b["author_id"] == author_id]
    return jsonify({"author": author, "books": books, "total": len(books)})


# ============================================================
# ROUTES: MEMBERS
# ============================================================

@app.route("/api/v1/members", methods=["GET"])
def get_members():
    """GET /api/v1/members"""
    page     = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 5))
    return jsonify(paginate_offset(MEMBERS, page, per_page))


@app.route("/api/v1/members/<int:member_id>", methods=["GET"])
def get_member(member_id):
    """GET /api/v1/members/:id"""
    member = next((m for m in MEMBERS if m["id"] == member_id), None)
    if not member:
        abort(404, description=f"Member {member_id} not found")
    return jsonify(member)


@app.route("/api/v1/members/<int:member_id>/loans", methods=["GET"])
def get_member_loans(member_id):
    """GET /api/v1/members/:id/loans — Lịch sử mượn của 1 thành viên"""
    member = next((m for m in MEMBERS if m["id"] == member_id), None)
    if not member:
        abort(404, description=f"Member {member_id} not found")
    
    status_filter = request.args.get("status")  # active | overdue | returned
    loans = [l for l in LOANS if l["member_id"] == member_id]
    if status_filter:
        loans = [l for l in loans if l["status"] == status_filter]
    
    enriched_loans = []
    for loan in loans:
        l = dict(loan)
        book = next((b for b in BOOKS if b["id"] == loan["book_id"]), None)
        l["book_title"] = book["title"] if book else "Unknown"
        enriched_loans.append(l)
    
    page     = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 5))
    result   = paginate_offset(enriched_loans, page, per_page)
    result["member"] = member
    return jsonify(result)


@app.route("/api/v1/members/<int:member_id>/reviews", methods=["GET"])
def get_member_reviews(member_id):
    """GET /api/v1/members/:id/reviews — Reviews của 1 thành viên"""
    member = next((m for m in MEMBERS if m["id"] == member_id), None)
    if not member:
        abort(404, description=f"Member {member_id} not found")
    
    reviews = [r for r in REVIEWS if r["member_id"] == member_id]
    for r in reviews:
        book = next((b for b in BOOKS if b["id"] == r["book_id"]), None)
        r["book_title"] = book["title"] if book else "Unknown"
    return jsonify({"member": member, "reviews": reviews, "total": len(reviews)})


# ============================================================
# ROUTES: SEARCH (Full-text + Filters)
# ============================================================

@app.route("/api/v1/search", methods=["GET"])
def search():
    """
    GET /api/v1/search?q=python&type=books|authors|all
    Tìm kiếm toàn văn
    """
    q    = request.args.get("q", "").strip()
    type = request.args.get("type", "all")
    
    if not q:
        return jsonify({"error": "Query parameter 'q' is required"}), 400

    results = {}
    
    if type in ("books", "all"):
        matched_books = [
            enrich_book(b) for b in BOOKS
            if q.lower() in b["title"].lower()
            or q.lower() in b["description"].lower()
            or q.lower() in " ".join(b["tags"]).lower()
        ]
        results["books"] = {"items": matched_books, "total": len(matched_books)}
    
    if type in ("authors", "all"):
        matched_authors = [
            a for a in AUTHORS
            if q.lower() in a["name"].lower() or q.lower() in a["bio"].lower()
        ]
        results["authors"] = {"items": matched_authors, "total": len(matched_authors)}
    
    return jsonify({"query": q, "type": type, "results": results})


# ============================================================
# ROUTES: STATS / DASHBOARD
# ============================================================

@app.route("/api/v1/stats", methods=["GET"])
def get_stats():
    """GET /api/v1/stats — Thống kê tổng quan thư viện"""
    return jsonify({
        "books": {
            "total": len(BOOKS),
            "total_copies": sum(b["total_copies"] for b in BOOKS),
            "available_copies": sum(b["available_copies"] for b in BOOKS),
            "genres": {g: sum(1 for b in BOOKS if b["genre"] == g) for g in GENRES},
        },
        "members": {
            "total": len(MEMBERS),
            "by_type": {
                "premium":  sum(1 for m in MEMBERS if m["membership_type"] == "premium"),
                "standard": sum(1 for m in MEMBERS if m["membership_type"] == "standard"),
                "student":  sum(1 for m in MEMBERS if m["membership_type"] == "student"),
            }
        },
        "loans": {
            "total": len(LOANS),
            "active":   sum(1 for l in LOANS if l["status"] == "active"),
            "overdue":  sum(1 for l in LOANS if l["status"] == "overdue"),
            "returned": sum(1 for l in LOANS if l["status"] == "returned"),
        },
        "reviews": {
            "total": len(REVIEWS),
            "avg_rating": round(sum(r["rating"] for r in REVIEWS) / len(REVIEWS), 2),
        }
    })


# ============================================================
# ROUTES: API EXPLORER (danh sách endpoints)
# ============================================================

@app.route("/api/v1", methods=["GET"])
def api_root():
    """GET /api/v1 — Danh sách tất cả endpoints"""
    return jsonify({
        "version": "1.0",
        "description": "Library Management System API",
        "resource_tree": {
            "/api/v1/books": {
                "GET": "List books (with pagination & filters)",
                "params": {
                    "pagination": "offset|cursor|page",
                    "page/per_page": "for offset pagination",
                    "cursor/limit": "for cursor pagination",
                    "page_number/page_size": "for page-based pagination",
                    "q": "full-text search",
                    "genre": "filter by genre",
                    "author": "filter by author name",
                    "available": "true|false",
                    "year_from/year_to": "filter by year range",
                    "tag": "filter by tag",
                    "sort_by": "title|year|author|id",
                    "order": "asc|desc"
                }
            },
            "/api/v1/books/:id": {"GET": "Book detail"},
            "/api/v1/books/:id/reviews": {"GET": "Book reviews"},
            "/api/v1/books/:id/loans": {"GET": "Book loan history"},
            "/api/v1/authors": {"GET": "List authors"},
            "/api/v1/authors/:id": {"GET": "Author detail"},
            "/api/v1/authors/:id/books": {"GET": "Books by author"},
            "/api/v1/members": {"GET": "List members"},
            "/api/v1/members/:id": {"GET": "Member detail"},
            "/api/v1/members/:id/loans": {"GET": "Member loan history"},
            "/api/v1/members/:id/reviews": {"GET": "Member reviews"},
            "/api/v1/search": {"GET": "Full-text search across books & authors"},
            "/api/v1/stats": {"GET": "Library statistics"},
        }
    })


# ============================================================
# ERROR HANDLERS
# ============================================================

@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Not Found", "message": str(e)}), 404

@app.errorhandler(400)
def bad_request(e):
    return jsonify({"error": "Bad Request", "message": str(e)}), 400

@app.errorhandler(500)
def server_error(e):
    return jsonify({"error": "Internal Server Error", "message": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)
