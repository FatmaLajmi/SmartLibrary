from django.db import models
from django.core.exceptions import ValidationError
from LivreApp.models import Livre


class Stock(models.Model):
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('out_of_stock', 'Out of Stock'),
        ('on_order', 'On Order'),
        ('low', 'Low Stock'),
    ]
    
    # ONE-TO-ONE relationship (this is the key fix!)
    book = models.OneToOneField(
        'LivreApp.Livre',
        on_delete=models.CASCADE,
        related_name='stock',
        verbose_name='Book',
        primary_key=True  # Makes book the primary key, ensuring uniqueness
    )
    
    # Quantitative fields
    quantity = models.PositiveIntegerField(
        default=0,
        verbose_name='Quantity in Stock'
    )
    min_quantity = models.PositiveIntegerField(
        default=10,
        verbose_name='Minimum Quantity',
        help_text='Threshold for low stock alert'
    )
    max_quantity = models.PositiveIntegerField(
        default=100,
        verbose_name='Maximum Quantity',
        help_text='Maximum storage capacity'
    )
    
    # Status (auto-calculated based on quantity)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='available',
        verbose_name='Status',
        editable=False  # Auto-calculated in save()
    )
    
    # Timestamps
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Creation Date'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Last Modification'
    )

    class Meta:
        verbose_name = "Stock"
        verbose_name_plural = "Stocks"
        ordering = ['-updated_at']

    def __str__(self):
        return f"Stock: {self.book.title} - {self.quantity} units"
    
    def clean(self):
        """Validate that quantity doesn't exceed max_quantity"""
        if self.quantity > self.max_quantity:
            raise ValidationError({
                'quantity': f'Quantity cannot exceed maximum quantity ({self.max_quantity})'
            })
        if self.min_quantity > self.max_quantity:
            raise ValidationError({
                'min_quantity': 'Minimum quantity cannot exceed maximum quantity'
            })
    
    def save(self, *args, **kwargs):
        # Auto-update status based on quantity
        if self.quantity == 0:
            self.status = 'out_of_stock'
        elif self.quantity <= self.min_quantity:
            self.status = 'low'
        else:
            self.status = 'available'
        
        # Run validation
        self.full_clean()
        
        super().save(*args, **kwargs)
        
    # a property to access book's ISBN easily
    @property  
    def isbn(self):
        return self.book.isbn if self.book.isbn else "N/A"
    
    @property
    def is_low_stock(self):
        """Check if stock is below minimum threshold"""
        return self.quantity <= self.min_quantity
    
    @property
    def stock_percentage(self):
        """Calculate stock level as percentage of max capacity"""
        if self.max_quantity == 0:
            return 0
        return (self.quantity / self.max_quantity) * 100
    
    def add_stock(self, amount):
        """Safely add stock with validation"""
        new_quantity = self.quantity + amount
        if new_quantity > self.max_quantity:
            raise ValidationError(
                f'Cannot add {amount} units. Would exceed maximum capacity of {self.max_quantity}'
            )
        self.quantity = new_quantity
        self.save()
    
    def remove_stock(self, amount):
        """Safely remove stock with validation"""
        if amount > self.quantity:
            raise ValidationError(
                f'Cannot remove {amount} units. Only {self.quantity} available'
            )
        self.quantity -= amount
        self.save()


# Signal to auto-create stock when a new Livre is created
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=Livre)     #the receiver listens for post_save signals from the Livre model
def create_stock_for_livre(sender, instance, created, **kwargs):
    """Automatically create a Stock entry when a new Livre is created"""
    if created:
        Stock.objects.create(
            book=instance,
            quantity=instance.quantite if hasattr(instance, 'quantite') else 0
        )