from models import Book, Author, Member, Loan, Review
from app_simple import (
    BOOKS as RAW_BOOKS, 
    AUTHORS as RAW_AUTHORS, 
    MEMBERS as RAW_MEMBERS, 
    LOANS as RAW_LOANS, 
    REVIEWS as RAW_REVIEWS, 
    GENRES
)

# Khởi tạo các list data giả lập được ép kiểu vào Data Modeling (Dataclasses)
AUTHORS = [Author(**a) for a in RAW_AUTHORS]
BOOKS = [Book(**b) for b in RAW_BOOKS]
MEMBERS = [Member(**m) for m in RAW_MEMBERS]
LOANS = [Loan(**l) for l in RAW_LOANS]
REVIEWS = [Review(**r) for r in RAW_REVIEWS]
