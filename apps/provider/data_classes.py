import dataclasses


@dataclasses.dataclass
class ProviderInfo:
    manager_uid: int
    name: str
    is_available: bool
    uid: int | None = None


@dataclasses.dataclass
class ProductInfo:
    title: str
    description: str
    is_active: bool
    in_stock: int
    image_path: str
    categoty_uid: int
    uid: int | None = None


@dataclasses.dataclass
class CategoryInfo:
    title: str
    parent_category_uid: int
    uid: int | None = None


@dataclasses.dataclass
class ProductFilter:
    title_contains: str
    category: int
    price__gte: int
    price__lte: int
