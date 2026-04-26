class DataFactoryMixin:
    def _create_data(self, **kwargs):
        from moneybook.models import Data
        defaults = {
            'date': '2000-01-01',
            'item': 'test item',
            'price': 100,
            'direction_id': 2,
            'category_id': 1,
            'method_id': 1,
            'temp': False,
            'checked': False,
        }
        defaults.update(kwargs)
        return Data.objects.create(**defaults)
