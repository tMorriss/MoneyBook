from moneybook.models import Category, Direction, Method, PeriodicData
from moneybook.tests.base import BaseTestCase


class PeriodicDataTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        # テスト用のPeriodicDataを作成
        PeriodicData.objects.create(
            day=1,
            item="テスト定期取引1",
            price=1000,
            direction=Direction.get(2),
            method=Method.get(1),
            category=Category.get(1),
            temp=False
        )
        PeriodicData.objects.create(
            day=15,
            item="テスト定期取引2",
            price=2000,
            direction=Direction.get(2),
            method=Method.get(2),
            category=Category.get(2),
            temp=True
        )

    def test_get_all(self):
        """全ての定期取引データを取得できること"""
        data = PeriodicData.get_all()
        self.assertEqual(data.count(), 2)
        # day順にソートされていること
        self.assertEqual(data[0].day, 1)
        self.assertEqual(data[1].day, 15)

    def test_get(self):
        """指定したIDの定期取引データを取得できること"""
        pd = PeriodicData.objects.first()
        retrieved = PeriodicData.get(pd.pk)
        self.assertEqual(retrieved.item, "テスト定期取引1")
        self.assertEqual(retrieved.price, 1000)
        self.assertEqual(retrieved.day, 1)

    def test_str(self):
        """__str__メソッドがitemを返すこと"""
        pd = PeriodicData.objects.first()
        self.assertEqual(str(pd), "テスト定期取引1")

    def test_fields(self):
        """全フィールドが正しく保存されること"""
        pd = PeriodicData.objects.first()
        self.assertEqual(pd.day, 1)
        self.assertEqual(pd.item, "テスト定期取引1")
        self.assertEqual(pd.price, 1000)
        self.assertEqual(pd.direction.pk, 2)
        self.assertEqual(pd.method.pk, 1)
        self.assertEqual(pd.category.pk, 1)
        self.assertEqual(pd.temp, False)

    def test_ordering(self):
        """データがday順にソートされること"""
        # 追加のデータを作成（日付が小さい順）
        PeriodicData.objects.create(
            day=5,
            item="中間",
            price=500,
            direction=Direction.get(1),
            method=Method.get(1),
            category=Category.get(1),
            temp=False
        )

        data = PeriodicData.get_all()
        self.assertEqual(data.count(), 3)
        self.assertEqual(data[0].day, 1)
        self.assertEqual(data[1].day, 5)
        self.assertEqual(data[2].day, 15)
