import dataclasses

@dataclasses.dataclass
class ProviderInfo:
    uid: int | None = None
    manager_uid: int
    name: str
    is_available: bool

@dataclasses.dataclass
class ProductInfo:
    uid: int | None = None
    title: str
    description: str
    is_active: bool
    in_stock: int
    image_path: str
    categoty_uid: int

@dataclasses.dataclass
class CategoryInfo:
    uid: int | None = None
    title: str
    parent_category_uid: int

@dataclasses.dataclass
class ProductFilter:
    title_contains: str
    category: int
    price__gte: int
    price__lte: int