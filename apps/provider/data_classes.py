import dataclasses

@dataclasses.dataclass
class ProviderInfo:
    uid: str | None = None
    manager_uid: str
    name: str
    is_available: bool

@dataclasses.dataclass
class ProductInfo:
    uid: str | None = None
    title: str
    description: str
    is_active: bool
    in_stock: int
    image_path: str
    categoty_uid: str

@dataclasses.dataclass
class CategoryInfo:
    uid: str | None = None
    title: str
    parent_category_uid: str

@dataclasses.dataclass
class ProductFilter:
    title_contains: str
    category: int
    price__gte: int
    price__lte: int