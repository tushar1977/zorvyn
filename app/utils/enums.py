import enum


class RecordType(enum.Enum):
    INCOME = "income"
    EXPENSE = "expense"


class CategoryType(enum.Enum):
    INCOME = "income"
    EXPENSE = "expense"


class UserStatus(enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
