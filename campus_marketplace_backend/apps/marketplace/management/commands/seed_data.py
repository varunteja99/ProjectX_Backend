import random
from decimal import Decimal
from datetime import timedelta
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from django.utils import timezone
from django.db import transaction

from apps.marketplace.models import Campus, Category, Listing, ListingImage, Textbook, Wishlist, SavedSearch
from apps.users.models import User
from apps.messaging.models import Conversation, Message
from apps.transactions.models import Offer, Transaction, MeetingLocation
from apps.reviews.models import Review
from apps.safety.models import Notification, StudyMaterial, FlaggedContent


class Command(BaseCommand):
    help = 'Seeds the database with comprehensive test data'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing data before seeding',
        )

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('\n' + '='*70))
        self.stdout.write(self.style.SUCCESS('SEEDING DATABASE WITH COMPREHENSIVE TEST DATA'))
        self.stdout.write(self.style.SUCCESS('='*70 + '\n'))

        if kwargs['clear']:
            self.clear_data()

        with transaction.atomic():
            self.create_campuses()
            self.create_categories()
            self.create_textbook_subcategories()
            self.create_users()
            self.create_meeting_locations()
            self.create_listings()
            self.create_textbook_details()
            self.create_listing_images()
            self.create_wishlist_items()
            self.create_saved_searches()
            self.create_conversations_and_messages()
            self.create_offers()
            self.create_transactions()
            self.create_reviews()
            self.create_notifications()
            self.create_study_materials()
            self.create_flagged_content()

        self.stdout.write(self.style.SUCCESS('\n' + '='*70))
        self.stdout.write(self.style.SUCCESS('SEEDING COMPLETE!'))
        self.stdout.write(self.style.SUCCESS('='*70 + '\n'))
        self.print_summary()

    def clear_data(self):
        """Clear existing data"""
        self.stdout.write(self.style.WARNING('Clearing existing data...'))

        models_to_clear = [
            Notification, StudyMaterial, FlaggedContent,
            Review, Transaction, Offer, Message, Conversation,
            SavedSearch, Wishlist, ListingImage, Textbook, Listing,
            MeetingLocation, User, Category, Campus
        ]

        for model in models_to_clear:
            count = model.objects.count()
            if count > 0:
                model.objects.all().delete()
                self.stdout.write(f'  ✓ Cleared {count} {model.__name__} records')

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

    def create_users(self):
        """Create test users"""
        self.stdout.write('\nCreating users...')

        campuses = list(Campus.objects.all())
        if not campuses:
            self.stdout.write(self.style.WARNING('  ! No campuses found'))
            return

        users_data = [
            {'email': 'john.doe@pfw.edu', 'username': 'johndoe', 'first_name': 'John', 'last_name': 'Doe'},
            {'email': 'jane.smith@pfw.edu', 'username': 'janesmith', 'first_name': 'Jane', 'last_name': 'Smith'},
            {'email': 'mike.johnson@purdue.edu', 'username': 'mikej', 'first_name': 'Mike', 'last_name': 'Johnson'},
            {'email': 'sarah.williams@iu.edu', 'username': 'sarahw', 'first_name': 'Sarah', 'last_name': 'Williams'},
            {'email': 'alex.brown@pfw.edu', 'username': 'alexb', 'first_name': 'Alex', 'last_name': 'Brown'},
            {'email': 'emily.davis@purdue.edu', 'username': 'emilyd', 'first_name': 'Emily', 'last_name': 'Davis'},
            {'email': 'chris.wilson@iu.edu', 'username': 'chrisw', 'first_name': 'Chris', 'last_name': 'Wilson'},
            {'email': 'lisa.anderson@pfw.edu', 'username': 'lisaa', 'first_name': 'Lisa', 'last_name': 'Anderson'},
            {'email': 'david.taylor@purdue.edu', 'username': 'davidt', 'first_name': 'David', 'last_name': 'Taylor'},
            {'email': 'maria.garcia@iu.edu', 'username': 'mariag', 'first_name': 'Maria', 'last_name': 'Garcia'},
            {'email': 'james.martin@pfw.edu', 'username': 'jamesm', 'first_name': 'James', 'last_name': 'Martin'},
            {'email': 'rachel.lee@purdue.edu', 'username': 'rachell', 'first_name': 'Rachel', 'last_name': 'Lee'},
            {'email': 'kevin.white@iu.edu', 'username': 'kevinw', 'first_name': 'Kevin', 'last_name': 'White'},
            {'email': 'anna.hall@pfw.edu', 'username': 'annah', 'first_name': 'Anna', 'last_name': 'Hall'},
            {'email': 'ryan.thomas@purdue.edu', 'username': 'ryant', 'first_name': 'Ryan', 'last_name': 'Thomas'},
        ]

        for data in users_data:
            # Match campus based on email domain
            domain = '@' + data['email'].split('@')[1]
            campus = next((c for c in campuses if c.email_domain == domain), campuses[0])

            user, created = User.objects.get_or_create(
                email=data['email'],
                defaults={
                    **data,
                    'password': 'pbkdf2_sha256$600000$test$dummy',  # Dummy hashed password
                    'campus': campus,
                    'is_verified': True,
                    'is_active': True,
                    'student_id': f'ST{random.randint(100000, 999999)}',
                    'phone_number': f'+1{random.randint(2000000000, 9999999999)}',
                }
            )
            if created:
                user.set_password('password123')  # Set proper password
                user.save()
                self.stdout.write(self.style.SUCCESS(f'  ✓ Created user: {user.username}'))
            else:
                self.stdout.write(f'  - User already exists: {user.username}')

    def create_meeting_locations(self):
        """Create safe meeting locations"""
        self.stdout.write('\nCreating meeting locations...')

        campuses = Campus.objects.all()

        locations_by_campus = {
            'Purdue University Fort Wayne': [
                {'name': 'Helmke Library - Main Entrance', 'type': 'library', 'building': 'Helmke Library'},
                {'name': 'Student Union - Lobby', 'type': 'student_center', 'building': 'Walb Student Union'},
                {'name': 'Safety Office', 'type': 'security_desk', 'building': 'Gates Center'},
            ],
            'Purdue University West Lafayette': [
                {'name': 'Hicks Library - Ground Floor', 'type': 'library', 'building': 'Hicks Library'},
                {'name': 'PMU - Main Lobby', 'type': 'student_center', 'building': 'Purdue Memorial Union'},
                {'name': 'PURR Safety Desk', 'type': 'security_desk', 'building': 'Stewart Center'},
            ],
            'Indiana University Bloomington': [
                {'name': 'Wells Library - Information Desk', 'type': 'library', 'building': 'Wells Library'},
                {'name': 'IMU - Atrium', 'type': 'student_center', 'building': 'Indiana Memorial Union'},
                {'name': 'Campus Security Office', 'type': 'security_desk', 'building': 'IUPD Building'},
            ],
        }

        for campus in campuses:
            locations = locations_by_campus.get(campus.name, [])
            for loc_data in locations:
                location, created = MeetingLocation.objects.get_or_create(
                    campus=campus,
                    name=loc_data['name'],
                    defaults={
                        'location_type': loc_data['type'],
                        'building': loc_data.get('building', ''),
                        'hours_of_operation': '8:00 AM - 10:00 PM',
                        'is_verified': True,
                        'is_active': True,
                    }
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f'  ✓ Created location: {location.name}'))

    def create_listings(self):
        """Create diverse listings"""
        self.stdout.write('\nCreating listings...')

        users = list(User.objects.all())
        categories = list(Category.objects.filter(parent__isnull=True))
        textbook_subcats = list(Category.objects.filter(parent__slug='textbooks'))

        if not users or not categories:
            self.stdout.write(self.style.WARNING('  ! Missing users or categories'))
            return

        listings_data = [
            # Textbooks
            {'title': 'Introduction to Algorithms Textbook (3rd Edition)', 'category': 'computer-science', 'price': 85.00, 'condition': 'good',
             'description': 'Great condition, minimal highlighting. Perfect for CS students.'},
            {'title': 'Calculus Early Transcendentals 8th Edition', 'category': 'mathematics', 'price': 120.00, 'condition': 'like_new',
             'description': 'Barely used, no writing inside. Includes access code.'},
            {'title': 'Organic Chemistry by David Klein', 'category': 'chemistry', 'price': 95.00, 'condition': 'good',
             'description': 'Some highlighting but in great shape overall.'},
            {'title': 'Fundamentals of Physics 11th Edition', 'category': 'physics', 'price': 110.00, 'condition': 'fair',
             'description': 'Used but functional. Some wear on cover.'},
            {'title': 'Campbell Biology 12th Edition', 'category': 'biology', 'price': 150.00, 'condition': 'like_new',
             'description': 'Like new! Used for one semester only.'},

            # Electronics
            {'title': 'MacBook Pro 13" 2020 M1', 'category': 'electronics', 'price': 850.00, 'condition': 'like_new',
             'description': '8GB RAM, 256GB SSD. Excellent condition, comes with charger.'},
            {'title': 'iPad Air 4th Gen with Apple Pencil', 'category': 'electronics', 'price': 450.00, 'condition': 'good',
             'description': '64GB, WiFi only. Perfect for note-taking. Includes case.'},
            {'title': 'Dell XPS 15 Laptop', 'category': 'electronics', 'price': 900.00, 'condition': 'good',
             'description': 'i7 processor, 16GB RAM, 512GB SSD. Great for programming.'},
            {'title': 'AirPods Pro 2nd Generation', 'category': 'electronics', 'price': 180.00, 'condition': 'like_new',
             'description': 'Barely used, all accessories included.'},
            {'title': 'Gaming Monitor 27" 144Hz', 'category': 'electronics', 'price': 250.00, 'condition': 'good',
             'description': '2560x1440, perfect for gaming and productivity.'},

            # Furniture
            {'title': 'IKEA Desk with Drawers', 'category': 'furniture', 'price': 60.00, 'condition': 'good',
             'description': 'Solid desk, perfect for dorm room. Easy to assemble.'},
            {'title': 'Comfortable Office Chair', 'category': 'furniture', 'price': 75.00, 'condition': 'good',
             'description': 'Ergonomic chair with lumbar support. Very comfortable.'},
            {'title': 'Twin Bed Frame with Mattress', 'category': 'furniture', 'price': 150.00, 'condition': 'fair',
             'description': 'Sturdy bed frame, mattress in decent condition.'},
            {'title': 'Bookshelf 5-Tier', 'category': 'furniture', 'price': 40.00, 'condition': 'good',
             'description': 'Perfect for textbooks and decor. Solid wood.'},
            {'title': 'Mini Fridge for Dorm', 'category': 'furniture', 'price': 80.00, 'condition': 'like_new',
             'description': 'Compact fridge, works perfectly. Great for dorms.'},

            # Clothing
            {'title': 'North Face Winter Jacket', 'category': 'clothing', 'price': 120.00, 'condition': 'good',
             'description': 'Warm and comfortable. Size Medium. Barely worn.'},
            {'title': 'Nike Running Shoes Size 10', 'category': 'clothing', 'price': 65.00, 'condition': 'good',
             'description': 'Lightly used, great condition. Perfect for jogging.'},
            {'title': 'Business Professional Suit', 'category': 'clothing', 'price': 150.00, 'condition': 'like_new',
             'description': 'Size 40R. Perfect for interviews and presentations.'},

            # School Supplies
            {'title': 'Scientific Calculator TI-84 Plus', 'category': 'school-supplies', 'price': 85.00, 'condition': 'good',
             'description': 'Works perfectly. Great for math and engineering courses.'},
            {'title': 'Graphing Calculator TI-Nspire CX', 'category': 'school-supplies', 'price': 95.00, 'condition': 'like_new',
             'description': 'Barely used, includes USB cable and software.'},
            {'title': 'HP Printer with Scanner', 'category': 'school-supplies', 'price': 60.00, 'condition': 'good',
             'description': 'Works great for printing assignments and scanning.'},

            # Sports & Outdoors
            {'title': 'Mountain Bike 21-Speed', 'category': 'sports-outdoors', 'price': 200.00, 'condition': 'good',
             'description': 'Great for campus commuting. Well maintained.'},
            {'title': 'Camping Tent 4-Person', 'category': 'sports-outdoors', 'price': 80.00, 'condition': 'good',
             'description': 'Used twice. Perfect for weekend trips.'},
            {'title': 'Yoga Mat with Bag', 'category': 'sports-outdoors', 'price': 25.00, 'condition': 'like_new',
             'description': 'Eco-friendly mat, comes with carrying bag.'},

            # Kitchen
            {'title': 'Keurig Coffee Maker', 'category': 'kitchen-appliances', 'price': 45.00, 'condition': 'good',
             'description': 'Perfect for dorm or apartment. Works great.'},
            {'title': 'Blender NutriBullet', 'category': 'kitchen-appliances', 'price': 40.00, 'condition': 'good',
             'description': 'Great for smoothies. Includes all cups and lids.'},
            {'title': 'Air Fryer 5.8 Qt', 'category': 'kitchen-appliances', 'price': 70.00, 'condition': 'like_new',
             'description': 'Used only a few times. Cooks food perfectly.'},

            # More textbooks
            {'title': 'Data Structures and Algorithms in Java', 'category': 'computer-science', 'price': 75.00, 'condition': 'good',
             'description': 'Essential CS textbook. Good condition with some notes.'},
            {'title': 'Linear Algebra and Its Applications', 'category': 'mathematics', 'price': 90.00, 'condition': 'like_new',
             'description': 'Almost new condition. Great resource.'},
            {'title': 'Microeconomics Principles', 'category': 'business', 'price': 80.00, 'condition': 'good',
             'description': 'Used for ECON 101. Solid condition.'},
            {'title': 'Engineering Mechanics Dynamics', 'category': 'engineering', 'price': 100.00, 'condition': 'fair',
             'description': 'Well-used but all pages intact. Functional.'},
        ]

        created_count = 0
        for data in listings_data:
            seller = random.choice(users)

            # Find the category
            cat_slug = data['category']
            category = next((c for c in categories if c.slug == cat_slug), None)
            if not category and cat_slug in ['computer-science', 'mathematics', 'chemistry', 'physics', 'biology', 'business', 'engineering']:
                category = next((c for c in textbook_subcats if slugify(cat_slug) in c.slug), None)
            if not category:
                category = random.choice(categories)

            listing, created = Listing.objects.get_or_create(
                title=data['title'],
                seller=seller,
                defaults={
                    'category': category,
                    'campus': seller.campus,
                    'description': data['description'],
                    'price': Decimal(str(data['price'])),
                    'condition': data['condition'],
                    'status': random.choice(['active', 'active', 'active', 'sold']),
                    'location': random.choice(['Main Campus', 'North Campus', 'Student Center', 'Library']),
                    'view_count': random.randint(5, 150),
                    'is_negotiable': random.choice([True, True, False]),
                    'created_at': timezone.now() - timedelta(days=random.randint(1, 60)),
                }
            )
            if created:
                created_count += 1

        self.stdout.write(self.style.SUCCESS(f'  ✓ Created {created_count} listings'))

    def create_textbook_details(self):
        """Create textbook-specific details for textbook listings"""
        self.stdout.write('\nCreating textbook details...')

        textbook_category = Category.objects.filter(slug='textbooks').first()
        if not textbook_category:
            return

        textbook_listings = Listing.objects.filter(category__parent=textbook_category)

        textbook_data = {
            'Introduction to Algorithms': {
                'isbn_13': '9780262033848',
                'author': 'Thomas H. Cormen',
                'edition': '3rd',
                'publisher': 'MIT Press',
                'course_code': 'CS 401',
                'course_name': 'Algorithms',
                'department': 'Computer Science',
            },
            'Calculus Early Transcendentals': {
                'isbn_13': '9781285741550',
                'author': 'James Stewart',
                'edition': '8th',
                'publisher': 'Cengage',
                'course_code': 'MATH 161',
                'course_name': 'Calculus I',
                'department': 'Mathematics',
            },
            'Organic Chemistry': {
                'isbn_13': '9781119349471',
                'author': 'David Klein',
                'edition': '3rd',
                'publisher': 'Wiley',
                'course_code': 'CHEM 261',
                'course_name': 'Organic Chemistry I',
                'department': 'Chemistry',
            },
            'Fundamentals of Physics': {
                'isbn_13': '9781119460749',
                'author': 'David Halliday',
                'edition': '11th',
                'publisher': 'Wiley',
                'course_code': 'PHYS 152',
                'course_name': 'General Physics II',
                'department': 'Physics',
            },
            'Campbell Biology': {
                'isbn_13': '9780135188743',
                'author': 'Jane B. Reece',
                'edition': '12th',
                'publisher': 'Pearson',
                'course_code': 'BIOL 121',
                'course_name': 'Principles of Biology',
                'department': 'Biology',
            },
            'Data Structures and Algorithms': {
                'isbn_13': '9780672324536',
                'author': 'Michael Goodrich',
                'edition': '6th',
                'publisher': 'Wiley',
                'course_code': 'CS 260',
                'course_name': 'Data Structures',
                'department': 'Computer Science',
            },
            'Linear Algebra': {
                'isbn_13': '9780321982384',
                'author': 'David C. Lay',
                'edition': '5th',
                'publisher': 'Pearson',
                'course_code': 'MATH 262',
                'course_name': 'Linear Algebra',
                'department': 'Mathematics',
            },
            'Microeconomics': {
                'isbn_13': '9780134744476',
                'author': 'Robert Pindyck',
                'edition': '9th',
                'publisher': 'Pearson',
                'course_code': 'ECON 201',
                'course_name': 'Microeconomics',
                'department': 'Economics',
            },
        }

        created_count = 0
        for listing in textbook_listings:
            # Match textbook data by title
            matching_key = next((key for key in textbook_data.keys() if key.lower() in listing.title.lower()), None)
            if matching_key:
                data = textbook_data[matching_key]
                textbook, created = Textbook.objects.get_or_create(
                    listing=listing,
                    defaults={
                        'title': listing.title,
                        'isbn_13': data['isbn_13'],
                        'author': data['author'],
                        'edition': data['edition'],
                        'publisher': data['publisher'],
                        'course_code': data['course_code'],
                        'course_name': data['course_name'],
                        'department': data['department'],
                        'is_required': True,
                        'publication_year': 2018 + random.randint(0, 5),
                    }
                )
                if created:
                    created_count += 1

        self.stdout.write(self.style.SUCCESS(f'  ✓ Created {created_count} textbook details'))

    def create_listing_images(self):
        """Create placeholder images for listings"""
        self.stdout.write('\nCreating listing images...')

        listings = Listing.objects.all()

        # Category-specific image mappings with Unsplash
        category_images = {
            'textbooks': 'https://images.unsplash.com/photo-1543002588-bfa74002ed7e?w=800&h=600&fit=crop',
            'computer-science': 'https://images.unsplash.com/photo-1532012197267-da84d127e765?w=800&h=600&fit=crop',
            'mathematics': 'https://images.unsplash.com/photo-1635070041078-e363dbe005cb?w=800&h=600&fit=crop',
            'electronics': 'https://images.unsplash.com/photo-1498049794561-7780e7231661?w=800&h=600&fit=crop',
            'laptop': 'https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=800&h=600&fit=crop',
            'macbook': 'https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=800&h=600&fit=crop',
            'ipad': 'https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?w=800&h=600&fit=crop',
            'airpods': 'https://images.unsplash.com/photo-1606841837239-c5a1a4a07af7?w=800&h=600&fit=crop',
            'monitor': 'https://images.unsplash.com/photo-1527443224154-c4a3942d3acf?w=800&h=600&fit=crop',
            'furniture': 'https://images.unsplash.com/photo-1555041469-a586c61ea9bc?w=800&h=600&fit=crop',
            'desk': 'https://images.unsplash.com/photo-1518455027359-f3f8164ba6bd?w=800&h=600&fit=crop',
            'chair': 'https://images.unsplash.com/photo-1580480055273-228ff5388ef8?w=800&h=600&fit=crop',
            'bed': 'https://images.unsplash.com/photo-1505693416388-ac5ce068fe85?w=800&h=600&fit=crop',
            'bookshelf': 'https://images.unsplash.com/photo-1594620302200-9a762244a156?w=800&h=600&fit=crop',
            'fridge': 'https://images.unsplash.com/photo-1571175443880-49e1d25b2bc5?w=800&h=600&fit=crop',
            'clothing': 'https://images.unsplash.com/photo-1523381210434-271e8be1f52b?w=800&h=600&fit=crop',
            'jacket': 'https://images.unsplash.com/photo-1551028719-00167b16eac5?w=800&h=600&fit=crop',
            'shoes': 'https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=800&h=600&fit=crop',
            'suit': 'https://images.unsplash.com/photo-1594938298603-c8148c4dae35?w=800&h=600&fit=crop',
            'calculator': 'https://images.unsplash.com/photo-1587145820266-a5951ee6f620?w=800&h=600&fit=crop',
            'printer': 'https://images.unsplash.com/photo-1612815154858-60aa4c59eaa6?w=800&h=600&fit=crop',
            'bike': 'https://images.unsplash.com/photo-1576435728678-68d0fbf94e91?w=800&h=600&fit=crop',
            'tent': 'https://images.unsplash.com/photo-1504280390367-361c6d9f38f4?w=800&h=600&fit=crop',
            'yoga': 'https://images.unsplash.com/photo-1601925260368-ae2f83cf8b7f?w=800&h=600&fit=crop',
            'coffee': 'https://images.unsplash.com/photo-1517668808822-9ebb02f2a0e6?w=800&h=600&fit=crop',
            'blender': 'https://images.unsplash.com/photo-1585515320310-259814833f62?w=800&h=600&fit=crop',
            'airfryer': 'https://images.unsplash.com/photo-1585515320310-259814833f62?w=800&h=600&fit=crop',
        }

        def get_image_url(listing_title, listing_category):
            """Get appropriate image URL based on listing title and category"""
            title_lower = listing_title.lower()

            # Match specific items
            if 'macbook' in title_lower:
                return category_images['macbook']
            elif 'ipad' in title_lower:
                return category_images['ipad']
            elif 'airpods' in title_lower:
                return category_images['airpods']
            elif 'dell' in title_lower or 'laptop' in title_lower:
                return category_images['laptop']
            elif 'monitor' in title_lower:
                return category_images['monitor']
            elif 'desk' in title_lower:
                return category_images['desk']
            elif 'chair' in title_lower:
                return category_images['chair']
            elif 'bed' in title_lower:
                return category_images['bed']
            elif 'bookshelf' in title_lower:
                return category_images['bookshelf']
            elif 'fridge' in title_lower:
                return category_images['fridge']
            elif 'jacket' in title_lower:
                return category_images['jacket']
            elif 'shoes' in title_lower or 'nike' in title_lower:
                return category_images['shoes']
            elif 'suit' in title_lower:
                return category_images['suit']
            elif 'calculator' in title_lower:
                return category_images['calculator']
            elif 'printer' in title_lower:
                return category_images['printer']
            elif 'bike' in title_lower:
                return category_images['bike']
            elif 'tent' in title_lower:
                return category_images['tent']
            elif 'yoga' in title_lower:
                return category_images['yoga']
            elif 'coffee' in title_lower or 'keurig' in title_lower:
                return category_images['coffee']
            elif 'blender' in title_lower:
                return category_images['blender']
            elif 'air fryer' in title_lower or 'airfryer' in title_lower:
                return category_images['airfryer']
            elif 'algorithm' in title_lower or 'data structure' in title_lower:
                return category_images['computer-science']
            elif 'calculus' in title_lower or 'linear algebra' in title_lower:
                return category_images['mathematics']
            elif 'textbook' in title_lower or listing_category.parent and listing_category.parent.slug == 'textbooks':
                return category_images['textbooks']
            elif listing_category.slug == 'electronics':
                return category_images['electronics']
            elif listing_category.slug == 'furniture':
                return category_images['furniture']
            elif listing_category.slug == 'clothing':
                return category_images['clothing']
            else:
                return category_images.get(listing_category.slug, 'https://images.unsplash.com/photo-1560393464-5c69a73c5770?w=800&h=600&fit=crop')

        created_count = 0
        for listing in listings:
            num_images = random.randint(1, 3)
            base_image_url = get_image_url(listing.title, listing.category)

            for i in range(num_images):
                # Add slight variation to image URL for multiple images
                image_url = base_image_url
                if i > 0:
                    image_url = base_image_url.replace('?w=800', f'?w=800&q={80+i*5}')

                image, created = ListingImage.objects.get_or_create(
                    listing=listing,
                    display_order=i,
                    defaults={
                        'image_url': image_url,
                        'is_primary': i == 0,
                    }
                )
                if created:
                    created_count += 1

        self.stdout.write(self.style.SUCCESS(f'  ✓ Created {created_count} listing images'))

    def create_wishlist_items(self):
        """Create wishlist items"""
        self.stdout.write('\nCreating wishlist items...')

        users = list(User.objects.all())
        listings = list(Listing.objects.filter(status='active'))

        created_count = 0
        for user in users:
            # Each user wishlists 2-5 items
            num_items = random.randint(2, 5)
            selected_listings = random.sample(listings, min(num_items, len(listings)))

            for listing in selected_listings:
                if listing.seller != user:  # Don't wishlist own items
                    wishlist, created = Wishlist.objects.get_or_create(
                        user=user,
                        listing=listing
                    )
                    if created:
                        created_count += 1

        self.stdout.write(self.style.SUCCESS(f'  ✓ Created {created_count} wishlist items'))

    def create_saved_searches(self):
        """Create saved searches"""
        self.stdout.write('\nCreating saved searches...')

        users = list(User.objects.all())
        categories = list(Category.objects.all())

        search_names = [
            'Affordable Textbooks',
            'Electronics Under $500',
            'Furniture Deals',
            'CS Textbooks',
            'Dorm Essentials',
            'Math Books',
        ]

        created_count = 0
        for user in users[:8]:  # First 8 users have saved searches
            num_searches = random.randint(1, 3)
            for _ in range(num_searches):
                search, created = SavedSearch.objects.get_or_create(
                    user=user,
                    search_name=random.choice(search_names),
                    defaults={
                        'search_query': random.choice(['laptop', 'textbook', 'desk', 'phone', '']),
                        'category': random.choice(categories) if random.random() > 0.5 else None,
                        'min_price': Decimal('10.00') if random.random() > 0.5 else None,
                        'max_price': Decimal('500.00') if random.random() > 0.5 else None,
                        'campus': user.campus,
                        'notification_enabled': True,
                    }
                )
                if created:
                    created_count += 1

        self.stdout.write(self.style.SUCCESS(f'  ✓ Created {created_count} saved searches'))

    def create_conversations_and_messages(self):
        """Create conversations and messages"""
        self.stdout.write('\nCreating conversations and messages...')

        users = list(User.objects.all())
        listings = list(Listing.objects.all())

        message_templates = [
            "Hi! Is this item still available?",
            "Would you be willing to negotiate on the price?",
            "Yes, it's still available!",
            "Sure! What price did you have in mind?",
            "Could I see more pictures?",
            "When would be a good time to meet?",
            "How about the library tomorrow at 3pm?",
            "Sounds good! See you then.",
            "Is this in good working condition?",
            "Yes, works perfectly! No issues at all.",
        ]

        conv_count = 0
        msg_count = 0

        # Create 20 conversations
        for _ in range(20):
            user1, user2 = random.sample(users, 2)
            listing = random.choice(listings)

            conversation, created = Conversation.objects.get_or_create(
                participant_1=user1,
                participant_2=user2,
                defaults={
                    'listing': listing,
                    'created_at': timezone.now() - timedelta(days=random.randint(1, 30)),
                }
            )

            if created:
                conv_count += 1

                # Add 3-8 messages per conversation
                num_messages = random.randint(3, 8)
                for i in range(num_messages):
                    sender = user1 if i % 2 == 0 else user2
                    receiver = user2 if i % 2 == 0 else user1

                    message = Message.objects.create(
                        conversation=conversation,
                        sender=sender,
                        receiver=receiver,
                        message_text=random.choice(message_templates),
                        is_read=i < num_messages - random.randint(0, 2),
                        created_at=conversation.created_at + timedelta(minutes=i * 15),
                    )
                    msg_count += 1

                    conversation.last_message_at = message.created_at

                conversation.save()

        self.stdout.write(self.style.SUCCESS(f'  ✓ Created {conv_count} conversations and {msg_count} messages'))

    def create_offers(self):
        """Create price negotiation offers"""
        self.stdout.write('\nCreating offers...')

        users = list(User.objects.all())
        listings = list(Listing.objects.filter(is_negotiable=True))

        created_count = 0
        for listing in listings[:15]:  # Create offers for 15 listings
            num_offers = random.randint(1, 3)
            for _ in range(num_offers):
                buyer = random.choice([u for u in users if u != listing.seller])
                offer_amount = listing.price * Decimal(str(random.uniform(0.7, 0.95)))

                offer, created = Offer.objects.get_or_create(
                    listing=listing,
                    buyer=buyer,
                    seller=listing.seller,
                    defaults={
                        'offer_amount': offer_amount.quantize(Decimal('0.01')),
                        'message': 'Would you accept this price?',
                        'status': random.choice(['pending', 'accepted', 'rejected', 'countered']),
                        'created_at': timezone.now() - timedelta(days=random.randint(1, 15)),
                    }
                )
                if created:
                    created_count += 1

        self.stdout.write(self.style.SUCCESS(f'  ✓ Created {created_count} offers'))

    def create_transactions(self):
        """Create transaction records"""
        self.stdout.write('\nCreating transactions...')

        sold_listings = Listing.objects.filter(status='sold')
        users = list(User.objects.all())
        meeting_locations = list(MeetingLocation.objects.all())

        created_count = 0
        for listing in sold_listings:
            buyer = random.choice([u for u in users if u != listing.seller])

            transaction, created = Transaction.objects.get_or_create(
                listing=listing,
                buyer=buyer,
                seller=listing.seller,
                defaults={
                    'final_price': listing.price * Decimal(str(random.uniform(0.85, 1.0))),
                    'status': random.choice(['completed', 'completed', 'sold']),
                    'meeting_location': random.choice(meeting_locations).name if meeting_locations else 'Library',
                    'payment_method': random.choice(['Cash', 'Venmo', 'Cash App']),
                    'notes': 'Great transaction!',
                    'created_at': timezone.now() - timedelta(days=random.randint(1, 45)),
                    'completed_at': timezone.now() - timedelta(days=random.randint(1, 40)),
                }
            )
            if created:
                created_count += 1
                self.transactions_created = getattr(self, 'transactions_created', [])
                self.transactions_created.append(transaction)

        self.stdout.write(self.style.SUCCESS(f'  ✓ Created {created_count} transactions'))

    def create_reviews(self):
        """Create user reviews"""
        self.stdout.write('\nCreating reviews...')

        transactions = getattr(self, 'transactions_created', [])
        if not transactions:
            transactions = list(Transaction.objects.filter(status='completed')[:10])

        review_texts = [
            'Great seller! Item was exactly as described.',
            'Fast and easy transaction. Highly recommend!',
            'Good experience overall. Item in good condition.',
            'Very responsive and professional. Would buy again!',
            'Item was perfect. Thanks!',
            'Smooth transaction. No issues.',
            'Excellent condition, better than expected!',
            'Good buyer, easy to work with.',
        ]

        created_count = 0
        for transaction in transactions:
            # Buyer reviews seller
            if random.random() > 0.3:  # 70% chance
                review, created = Review.objects.get_or_create(
                    transaction=transaction,
                    reviewer=transaction.buyer,
                    reviewee=transaction.seller,
                    defaults={
                        'rating': random.randint(4, 5),
                        'review_text': random.choice(review_texts),
                        'is_buyer_review': True,
                        'created_at': transaction.completed_at + timedelta(days=1) if transaction.completed_at else timezone.now(),
                    }
                )
                if created:
                    created_count += 1

        self.stdout.write(self.style.SUCCESS(f'  ✓ Created {created_count} reviews'))

    def create_notifications(self):
        """Create user notifications"""
        self.stdout.write('\nCreating notifications...')

        users = list(User.objects.all())

        notification_data = [
            {'type': 'message', 'title': 'New Message', 'message': 'You have a new message about your listing.'},
            {'type': 'offer', 'title': 'New Offer Received', 'message': 'Someone made an offer on your item.'},
            {'type': 'status_change', 'title': 'Listing Status Changed', 'message': 'Your listing status has been updated.'},
            {'type': 'price_drop', 'title': 'Price Drop Alert', 'message': 'An item on your wishlist has dropped in price!'},
            {'type': 'review', 'title': 'New Review', 'message': 'Someone left you a review.'},
        ]

        created_count = 0
        for user in users:
            num_notifications = random.randint(3, 8)
            for i in range(num_notifications):
                notif_data = random.choice(notification_data)
                notification = Notification.objects.create(
                    user=user,
                    notification_type=notif_data['type'],
                    title=notif_data['title'],
                    message=notif_data['message'],
                    is_read=random.choice([True, True, False]),
                    created_at=timezone.now() - timedelta(days=random.randint(0, 20)),
                )
                created_count += 1

        self.stdout.write(self.style.SUCCESS(f'  ✓ Created {created_count} notifications'))

    def create_study_materials(self):
        """Create study materials"""
        self.stdout.write('\nCreating study materials...')

        users = list(User.objects.all())
        campuses = list(Campus.objects.all())

        materials_data = [
            {'title': 'CS 101 Final Exam Study Guide', 'course': 'CS 101', 'type': 'study_guide', 'course_name': 'Intro to CS'},
            {'title': 'MATH 161 Calculus Notes', 'course': 'MATH 161', 'type': 'notes', 'course_name': 'Calculus I'},
            {'title': 'PHYS 152 Practice Problems', 'course': 'PHYS 152', 'type': 'practice_exam', 'course_name': 'Physics II'},
            {'title': 'CHEM 115 Lab Reports', 'course': 'CHEM 115', 'type': 'notes', 'course_name': 'General Chemistry'},
            {'title': 'ECON 201 Midterm Review', 'course': 'ECON 201', 'type': 'study_guide', 'course_name': 'Microeconomics'},
        ]

        created_count = 0
        for data in materials_data:
            for _ in range(2):  # Create 2 of each
                uploader = random.choice(users)
                campus = random.choice(campuses)

                material = StudyMaterial.objects.create(
                    uploader=uploader,
                    campus=campus,
                    title=data['title'],
                    description=f"Helpful {data['type'].replace('_', ' ')} for {data['course_name']}",
                    course_code=data['course'],
                    course_name=data['course_name'],
                    material_type=data['type'],
                    file_url=f'https://example.com/materials/{data["course"].lower()}.pdf',
                    file_type='application/pdf',
                    download_count=random.randint(5, 50),
                    rating=Decimal(str(random.uniform(4.0, 5.0))),
                    is_approved=True,
                    created_at=timezone.now() - timedelta(days=random.randint(1, 90)),
                )
                created_count += 1

        self.stdout.write(self.style.SUCCESS(f'  ✓ Created {created_count} study materials'))

    def create_flagged_content(self):
        """Create some flagged content reports"""
        self.stdout.write('\nCreating flagged content...')

        users = list(User.objects.all())
        listings = list(Listing.objects.all())

        created_count = 0
        for _ in range(5):  # Create 5 reports
            reporter = random.choice(users)
            listing = random.choice(listings)

            flag = FlaggedContent.objects.create(
                reporter=reporter,
                content_type='listing',
                content_id=listing.id,
                reason=random.choice(['spam', 'inappropriate', 'scam']),
                description='This listing seems suspicious.',
                status=random.choice(['pending', 'reviewed']),
                created_at=timezone.now() - timedelta(days=random.randint(1, 15)),
            )
            created_count += 1

        self.stdout.write(self.style.SUCCESS(f'  ✓ Created {created_count} flagged content reports'))

    def print_summary(self):
        """Print summary of seeded data"""
        self.stdout.write('\n' + '='*70)
        self.stdout.write(self.style.SUCCESS('DATABASE SEEDING SUMMARY'))
        self.stdout.write('='*70)

        summary_data = [
            ('Campuses', Campus.objects.count()),
            ('Categories', Category.objects.count()),
            ('Users', User.objects.count()),
            ('Listings', Listing.objects.count()),
            ('Textbooks', Textbook.objects.count()),
            ('Listing Images', ListingImage.objects.count()),
            ('Wishlist Items', Wishlist.objects.count()),
            ('Saved Searches', SavedSearch.objects.count()),
            ('Conversations', Conversation.objects.count()),
            ('Messages', Message.objects.count()),
            ('Offers', Offer.objects.count()),
            ('Transactions', Transaction.objects.count()),
            ('Reviews', Review.objects.count()),
            ('Meeting Locations', MeetingLocation.objects.count()),
            ('Notifications', Notification.objects.count()),
            ('Study Materials', StudyMaterial.objects.count()),
            ('Flagged Content', FlaggedContent.objects.count()),
        ]

        for label, count in summary_data:
            self.stdout.write(f'  {label:.<50} {count:>5}')

        self.stdout.write('='*70 + '\n')