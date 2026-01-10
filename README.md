 Websiteodr,Flask web application showcasing -poweredbusnesses.etureinclude dynmi conttmagement, amindashbar, cotactoms, eve rgistrations, a customer reviews 🌟
### **Core Functionality****S**: with Flask-Babel
- **Admin Dashboard**: Comprehensive management system for inquiries, reviews, and events**C**:Solutio pes, articls, ves, and reviews**F**:Integrated inquiry system emi notifcs**Rn**: Online evetregitraion and managent**Customer **: Revew collectand dipla ys
###**Tnicl Feaures****Design**: Mobile-first SS
- **Modern UI**: Professional interface with Font Awesome icons
- **Database Integration**: PostgreSQL with SQLAlchemy ORM
- **Security**: Password hashing, session management, admin authentication
- **EO Optimized**: Meta tags, structured content, semantic HTML
- **Performance**: Optimized assets, efficient database queries

## 🚀 Quick tart#**Prerequisites**
- Python 3.8+
- PostgreSQL database
- Git

### ****. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd AI-Solution
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3****.txt
   ```

4 **Database Setup**
   ```bash
   # Create PostgreSQL database
   createdb ai_solution
   
   # Set environmen variables
   epor DATABASE_URL="postgresql://username:password@localhost/ai_solution"export SECRET_KEY="your-secret-key-here"
   5**D**-c "fom app import create_app, db; app = create_app(); app.app_cotext()ush(); db.create_all()"6****

7. **Access the website**
   - Main site: http://localhost:5000
   - Admin login: http://localhost:5000/admin/login 📁
```AISolution/
├──                   #appliction
├── run.py                    # An runer├──config.py                 # Configuration settings
├── extensions.py             # Database extensions
├──                # ├──add.py                    # Data seeding sript
├── requirements.txt          # Pyth dependencies
├── README.md                 # This le
├── static/                   # Static assets
│   ├── css/
│   ├── js/
│   └── imaes/
├── templates/                # HTML templates
│   ├── components/           # Reusable components
│   ├── admin/               # Admin pages
│   └── *html               # Page temlates
├── translations/            # Translation files
│   ├── en/
│   ├── es/
│   └── zh/
└── babel.cfg                # Babel configuration
``

##🌐 MultilanguageSupprt

The website supports three laguages with ull nternationalization:

### **Supported Lanages**
- **English (en)**: Default language
- **Spanish (es)**: Español
- **Chinese (zh)**: 中文

### **Adding New Tnslas**

1. **Extracttranlatabl srs**
   ```bah   pybabel extract -F babel.cfg o messages.pot .
   ```

2. **Update translation files**
  ``bash
   pybabel upda -i essages.ot -d translations/
   ```

3. **Edit transtions**
   - Edi `.po` fils in `translation/[lang]/LC_MESSAGES
   Addtranslatedsrings for each languag

4. **Coile transion**  ``bah
   pybabel compile -d ranslons
   ``

## 🔧 Configuration

### **EnvironmentVariables**
```bash
#Database
DATABAE_URL="postgresql://username:password@localhos/i_soluion"

# Securty
SECRET_KEY="your-seret-key-here"

# Email (optional forcontct form)
MAIL_SERVER="mtp.gmail.com"
MAIL_PORT=587
MAIL_USERNAME="your-mail@gmail.com"
MAIL_PASSWORD="your-app-password"
```

### **Daabase Model**

**Inquiry**:ontact form submissions
- Fields: name, emailcompanyndustry, esse, status, created_at

**Review**: Customer reviws and rating Fields: name,company, industry, rating, feedback, created_at

**Event**: Even infomtio
- Fields: title, decription, date, ocn, image_url

**EvetRegitration**:Event registrations
 Fields: event_id, name, email, company, created_at

**Admin**: Adminser accounts
- Fieds: username, password_hash

## 🎨 Fronend Technologes

### **CSS Framework**
 **Tailwind CSS**: Utiity-first CSS frmework
- **Font Awesome 6.5.0**: Ico library
- **Cstom animations**: Smooth transitions and effects

### **JavScript Fatures**
- **Dynamicconten loading**: AJAX fo admin dshboard
- **Form validation**: Cliet-ide vaid
-**Interactive charts**: Chart.js or analytics
- **Responsive navigation**: Mobe mnu sytem## **Design System**
- **Colors**: Primary (015486),Sondary (#EF3451)
- **Typograpy**: System fots with fallbacks
- **Cmponents**: Reusabe UI components
- **Layout**: Respnsive rid system

## 📊 Admn Dashboard Featur

### **Inquiry Management**- View all contact form submissionsiter by sttu,industry, date
- Update inquiry status ending/Contacted)
- Export inquiry data

### **Review Management**
- View customer reviews and ratings
- Filter by rating, industr, dae
- Rating distribution carts
- Review analytics

### **Event Management**
- View event registrations
- Filter by event, date
- Registration statistics
- Export registratidata

### **Analytics**
- KPI cards ith key metrics
- Intractivecharts and graphs
- Monthly trends
- Peromnce insights

## 🔒 Security Features

### **Authentication**
- Adin login systm
- Passd hashing with Werzeug
- Session management
- Protected admin routes

### **Data Protection** SQL injection prevention with
- XSS protection with template escapingCSR protection for forms
- Input validation and sanitization

### **Best Practices**
- Environment-based configuration
- Secure password storage
- Minimal data exposure
- Regur security updates

## 📱 Reponsive Design

### **Breapoints**
- **Mobile**: < 768px
 **Tblet**: 768px - 1024px
- **Desktop**: > 1024px

### **Moile Features**
- Touch-friendly navigation
- Responsive forms
- Optimized images
- Fast loading times

## 🚀 Dpoyment

### **Production Setup**

1. **Web Server**:Gunicorn or uWSG
2. **Reverse Proxy**: Nginx or Apache
3. **Database**: PostgreSQL
4. **Process Maager**: Supervisor or sysmd

### **Envioment Configur**
```bsh
# Producton environment
export FLASK_ENV=production
export DATABASE_URL="postgresql://user:pss@hos/db"
export SECRET_KEY="product-secret-key"
```

### **Docker Deployment**
```dockerfileFROM python:3.9slim
WORKDIR/pp
COPY requirements.txt .
RUN pip nstal -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["gunicorn", "--b", "0.0.0.0:5000", "run:app"]
```

## 🤝 Contributing

1. Fork the repository
2.reate a feature branch
3. Make your changes
4. Add tests if applicable
5. ubmita pull request

### **Code e**
- Follow PEP 8 for Python code
- Use semantc HTML5
- Write clea, commented code
- Test thorouhly

## 📝 License
This project is proprietarysoftwre. All rights resered by AI-Solution.

## 🆘 upport

For suppot and questions:
- **Emal**: suport@ai-solution.com
- **Documentaion**:heck inine code comments
- **Issues**: Report bugs through ntral channels

## 🔄 Updaes

### **Version History**
 **v1.0**: Initial releae wth core features
- **v1.1**: Addmulti-language support
- **v1.2**: Enhanced admin dashboard
- **v1.3**: Improved security and perormance

### **Recent Changes**
- Fixed CDN URL isses in templates
- Updated icon alignment in admin login
- Enhaed error handling
- Improved mobile responsiveness

---

**AI-Solu** - Trnsforming businesses with intelgent AI soluions.
