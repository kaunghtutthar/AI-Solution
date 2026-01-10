from datetime import datetime
from extensions import db

class Inquiry(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20))
    company = db.Column(db.String(100))
    job_title = db.Column(db.String(100))
    country = db.Column(db.String(100))
    requirement_type = db.Column(db.String(100))
    requirement_summary = db.Column(db.String(200))
    detailed_requirements = db.Column(db.Text)
    timeline = db.Column(db.String(50))
    industry = db.Column(db.String(100))
    budget_range = db.Column(db.String(50))
    status = db.Column(
        db.String(20),
        nullable=False,
        default="Pending"
    )

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    job_title = db.Column(db.String(100))
    company = db.Column(db.String(100))
    industry = db.Column(db.String(100))
    rating = db.Column(db.Integer, nullable=False)
    feedback = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    staff_id = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    
class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    date = db.Column(db.DateTime, nullable=False)  
    location = db.Column(db.String(200))
    image = db.Column(db.String(200))  
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    
    title_es = db.Column(db.String(200))  
    title_zh = db.Column(db.String(200))  
    description_es = db.Column(db.Text)    
    description_zh = db.Column(db.Text)  
    location_es = db.Column(db.String(200))  
    location_zh = db.Column(db.String(200))  
    
    def get_translated_title(self, language='en'):
        if language == 'es' and self.title_es:
            return self.title_es
        elif language == 'zh' and self.title_zh:
            return self.title_zh
        return self.title
    
    def get_translated_description(self, language='en'):
        if language == 'es' and self.description_es:
            return self.description_es
        elif language == 'zh' and self.description_zh:
            return self.description_zh
        return self.description
    
    def get_translated_location(self, language='en'):
        if language == 'es' and self.location_es:
            return self.location_es
        elif language == 'zh' and self.location_zh:
            return self.location_zh
        return self.location
    
    def get_translated_date(self, language='en'):
        """Return date formatted for the specified language"""
        import calendar
        
        if language == 'es':
            
            spanish_months = {
                1: 'ene', 2: 'feb', 3: 'mar', 4: 'abr', 5: 'may', 6: 'jun',
                7: 'jul', 8: 'ago', 9: 'sep', 10: 'oct', 11: 'nov', 12: 'dic'
            }
            return self.date.strftime(f"%d {spanish_months[self.date.month]}, %Y")
        elif language == 'zh':
            
            return self.date.strftime("%Y年%m月%d日")
        else:
            
            return self.date.strftime("%b %d, %Y")
    
class EventRegistration(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    company = db.Column(db.String(100))
    job_title = db.Column(db.String(100))
    message = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    event = db.relationship("Event", backref=db.backref("registrations", lazy=True))


