class Description:
    """字段描述"""
    __slots__ = ('text',)

    def __init__(self, text: str):
        self.text = text

    def to_dict(self):
        return {"description": self.text}


class ExampleValue:
    """字段示例"""
    __slots__ = ('value',)

    def __init__(self, value):
        self.value = value

    def to_dict(self):
        return {"example": self.value}


class Unit:
    """字段单位"""
    __slots__ = ('unit',)

    def __init__(self, unit: str):
        self.unit = unit

    def to_dict(self):
        return {"unit": self.unit}
