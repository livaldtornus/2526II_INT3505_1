from flask import Blueprint, request
from mock_data import BOOKS, AUTHORS, MEMBERS, LOANS, REVIEWS
from models import Book, Author, Member
from utils import success_response, error_response, paginate_offset, paginate_cursor, paginate_page_based

api_bp = Blueprint("api_bp", __name__)

# --- HATEOAS ENRICHERS ---

def add_hateoas_links_book(book: Book):
    b_dict = book.to_dict()
    b_dict["_links"] = {
        "self": f"/api/v1/books/{book.id}",
        "author": f"/api/v1/authors/{book.author_id}",
        "reviews": f"/api/v1/books/{book.id}/reviews",
        "loans": f"/api/v1/books/{book.id}/loans"
    }
    author = next((a for a in AUTHORS if a.id == book.author_id), None)
    b_dict["author_name"] = author.name if author else "Unknown"
    return b_dict

def add_hateoas_links_author(author: Author):
    a_dict = author.to_dict()
    a_dict["_links"] = {
        "self": f"/api/v1/authors/{author.id}",
        "books": f"/api/v1/authors/{author.id}/books"
    }
    return a_dict

def add_hateoas_links_member(member: Member):
    m_dict = member.to_dict()
    m_dict["_links"] = {
        "self": f"/api/v1/members/{member.id}",
        "loans": f"/api/v1/members/{member.id}/loans",
        "reviews": f"/api/v1/members/{member.id}/reviews"
    }
    return m_dict

# --- ROUTES: BOOKS ---

@api_bp.route("/books", methods=["GET"])
def get_books():
    """Lấy danh sách sách - Hỗ trợ cả 3 kiểu Pagination và Filters"""
    q = request.args.get("q", "").lower()
    genre = request.args.get("genre")
    
    filtered = BOOKS
    if q:
        filtered = [b for b in filtered if q in b.title.lower() or q in b.description.lower()]
    if genre:
        filtered = [b for b in filtered if b.genre.lower() == genre.lower()]

    sort_by = request.args.get("sort_by", "id")
    order = request.args.get("order", "asc")
    if hasattr(Book, sort_by):
        filtered.sort(key=lambda x: getattr(x, sort_by), reverse=(order == "desc"))
        
    pagination_type = request.args.get("pagination", "offset")
    if pagination_type == "cursor":
        items, meta = paginate_cursor(filtered, request.args.get("cursor"), int(request.args.get("limit", 5)))
    elif pagination_type == "page":
        items, meta = paginate_page_based(filtered, int(request.args.get("page_number", 1)), int(request.args.get("page_size", 5)))
    else:
        items, meta = paginate_offset(filtered, int(request.args.get("page", 1)), int(request.args.get("per_page", 5)))
        
    enriched_items = [add_hateoas_links_book(b) for b in items]
    return success_response(enriched_items, "Books fetched successfully", meta)

@api_bp.route("/books/<int:book_id>", methods=["GET"])
def get_book(book_id):
    book = next((b for b in BOOKS if b.id == book_id), None)
    if not book: return error_response(f"Book {book_id} not found", 404)
    return success_response(add_hateoas_links_book(book))

# --- ROUTES: AUTHORS ---

@api_bp.route("/authors", methods=["GET"])
def get_authors():
    items, meta = paginate_offset(AUTHORS, int(request.args.get("page", 1)), int(request.args.get("per_page", 10)))
    enriched_items = [add_hateoas_links_author(a) for a in items]
    return success_response(enriched_items, "Authors fetched successfully", meta)

@api_bp.route("/authors/<int:author_id>", methods=["GET"])
def get_author(author_id):
    author = next((a for a in AUTHORS if a.id == author_id), None)
    if not author: return error_response(f"Author {author_id} not found", 404)
    return success_response(add_hateoas_links_author(author))

@api_bp.route("/authors/<int:author_id>/books", methods=["GET"])
def get_author_books(author_id):
    author = next((a for a in AUTHORS if a.id == author_id), None)
    if not author: return error_response(f"Author {author_id} not found", 404)
    
    books = [add_hateoas_links_book(b) for b in BOOKS if b.author_id == author_id]
    return success_response({"author": add_hateoas_links_author(author), "books": books})

# --- ROUTES: MEMBERS ---

@api_bp.route("/members", methods=["GET"])
def get_members():
    items, meta = paginate_offset(MEMBERS, int(request.args.get("page", 1)), int(request.args.get("per_page", 5)))
    enriched_items = [add_hateoas_links_member(m) for m in items]
    return success_response(enriched_items, "Members fetched successfully", meta)

@api_bp.route("/members/<int:member_id>", methods=["GET"])
def get_member(member_id):
    member = next((m for m in MEMBERS if m.id == member_id), None)
    if not member: return error_response(f"Member {member_id} not found", 404)
    return success_response(add_hateoas_links_member(member))
