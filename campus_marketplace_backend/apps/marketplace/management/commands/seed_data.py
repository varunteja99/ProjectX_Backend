from django.core.management.base import BaseCommand
from django.utils.text import slugify
from apps.marketplace.models import Campus, Category


class Command(BaseCommand):
    help = 'Seeds the database with initial data'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('\n' + '='*50))
        self.stdout.write(self.style.SUCCESS('SEEDING DATABASE'))
        self.stdout.write(self.style.SUCCESS('='*50 + '\n'))
        
        self.create_campuses()
        self.create_categories()
        self.create_textbook_subcategories()
        
        self.stdout.write(self.style.SUCCESS('\n' + '='*50))
        self.stdout.write(self.style.SUCCESS('SEEDING COMPLETE!'))
        self.stdout.write(self.style.SUCCESS('='*50 + '\n'))

    def create_campuses(self):
        """Create initial campus data"""
        self.stdout.write('Creating campuses...')
        
        campuses_data = [
            {
                'name': 'Purdue University Fort Wayne',
                'email_domain': '@pfw.edu',
                'city': 'Fort Wayne',
                'state': 'Indiana',
                'zip_code': '46805',
            },
            {
                'name': 'Purdue University West Lafayette',
                'email_domain': '@purdue.edu',
                'city': 'West Lafayette',
                'state': 'Indiana',
                'zip_code': '47907',
            },
            {
                'name': 'Indiana University Bloomington',
                'email_domain': '@iu.edu',
                'city': 'Bloomington',
                'state': 'Indiana',
                'zip_code': '47405',
            },
        ]
        
        for data in campuses_data:
            campus, created = Campus.objects.get_or_create(
                email_domain=data['email_domain'],
                defaults=data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'  ✓ Created campus: {campus.name}'))
            else:
                self.stdout.write(f'  - Campus already exists: {campus.name}')

    def create_categories(self):
        """Create initial category data"""
        self.stdout.write('\nCreating categories...')
        
        categories_data = [
            {'name': 'Textbooks', 'description': 'Course textbooks and academic books'},
            {'name': 'Electronics', 'description': 'Laptops, phones, tablets, and accessories'},
            {'name': 'Furniture', 'description': 'Desks, chairs, beds, and dorm furniture'},
            {'name': 'Clothing', 'description': 'Clothes, shoes, and accessories'},
            {'name': 'School Supplies', 'description': 'Notebooks, pens, and study materials'},
            {'name': 'Sports & Outdoors', 'description': 'Sports equipment and outdoor gear'},
            {'name': 'Kitchen & Appliances', 'description': 'Kitchen items and small appliances'},
            {'name': 'Other', 'description': 'Miscellaneous items'},
        ]
        
        for i, data in enumerate(categories_data):
            data['slug'] = slugify(data['name'])
            data['display_order'] = i
            
            category, created = Category.objects.get_or_create(
                slug=data['slug'],
                defaults=data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'  ✓ Created category: {category.name}'))
            else:
                self.stdout.write(f'  - Category already exists: {category.name}')

    def create_textbook_subcategories(self):
        """Create subcategories for textbooks"""
        self.stdout.write('\nCreating textbook subcategories...')
        
        textbooks_category = Category.objects.filter(slug='textbooks').first()
        
        if not textbooks_category:
            self.stdout.write(self.style.WARNING('  ! Textbooks category not found'))
            return
        
        subcategories_data = [
            'Computer Science',
            'Mathematics',
            'Engineering',
            'Business',
            'Biology',
            'Chemistry',
            'Physics',
            'Liberal Arts',
        ]
        
        for i, name in enumerate(subcategories_data):
            slug = slugify(name)
            subcategory, created = Category.objects.get_or_create(
                slug=slug,
                defaults={
                    'name': name,
                    'parent': textbooks_category,
                    'display_order': i,
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'    ✓ Created subcategory: {subcategory.name}'))
            else:
                self.stdout.write(f'    - Subcategory already exists: {subcategory.name}')