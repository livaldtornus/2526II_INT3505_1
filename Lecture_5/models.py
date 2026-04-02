from dataclasses import dataclass, field, asdict
from typing import List, Optional

@dataclass
class Author:
    id: int
    name: str
    nationality: str
    bio: str
    
    def to_dict(self):
        return asdict(self)

@dataclass
class Book:
    id: int
    title: str
    author_id: int
    isbn: str
    genre: str
    year: int
    total_copies: int
    available_copies: int
    description: str
    tags: List[str] = field(default_factory=list)
    
    def to_dict(self):
        return asdict(self)

@dataclass
class Member:
    id: int
    name: str
    email: str
    phone: str
    joined_date: str
    membership_type: str
    
    def to_dict(self):
        return asdict(self)

@dataclass
class Loan:
    id: int
    book_id: int
    member_id: int
    loan_date: str
    due_date: str
    status: str
    return_date: Optional[str] = None
    
    def to_dict(self):
        return asdict(self)

@dataclass
class Review:
    id: int
    book_id: int
    member_id: int
    rating: int
    comment: str
    created_at: str
    
    def to_dict(self):
        return asdict(self)
