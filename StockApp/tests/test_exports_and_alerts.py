from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from io import BytesIO
import openpyxl

from ..models import Stock, Book

User = get_user_model()

class ExportTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('admin', 'a@a.com', 'pass')
        self.user.is_staff = True
        self.user.is_superuser = True
        self.user.save()
        self.client = Client()
        self.client.login(username='admin', password='pass')

        book = Book.objects.create(title='Book A', genre='Fiction', author='Author X')
        self.stock = Stock.objects.create(book=book, quantity=5, min_quantity=10, max_quantity=100)

    def test_export_excel_action(self):
        changelist_url = reverse('admin:StockApp_stock_changelist')
        data = {'action': 'export_as_excel', '_selected_action': [str(self.stock.pk)]}
        resp = self.client.post(changelist_url, data)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp['Content-Type'], 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        wb = openpyxl.load_workbook(filename=BytesIO(resp.content))
        sheet = wb.active
        self.assertIn('Book title', [cell.value for cell in sheet[1]])