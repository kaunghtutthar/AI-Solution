import datetime
import email
from functools import wraps
from os import name
import re
from functools import wraps
from datetime import datetime, timezone
from tracemalloc import start
from arrow import now
from flask import Flask, app, render_template, request, redirect, url_for, session, flash, jsonify
from flask_babel import Babel, gettext, ngettext
from sqlalchemy import asc, desc, func
from werkzeug.security import check_password_hash, generate_password_hash
from extensions import db
from config import Config
from dateutil.relativedelta import relativedelta
from models import Event, EventRegistration, Inquiry, Review, Admin

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    
    app.config['JSON_AS_ASCII'] = False
    app.config['JSON_SORT_KEYS'] = False
    
    db.init_app(app)

    
    babel = Babel()

    @app.context_processor
    def inject_get_locale():
        return dict(get_locale=get_locale, _=gettext)

    def get_locale():
        
        if request.args.get('lang'):
            session['language'] = request.args.get('lang')
        
        if 'language' in session:
            return session['language']
        
        return request.accept_languages.best_match(['en', 'es', 'zh']) or 'en'

    
    babel.init_app(app, locale_selector=get_locale)

    with app.app_context():
        db.create_all()

    def inquiry_to_dict(q):
        return {
            'id': q.id,
            'name': q.name or '-',
            'email': q.email or '-',
            'phone': q.phone or '-',
            'company': q.company or '-',
            'job_title': q.job_title or '-',
            'country': q.country or '-',
            'requirement_type': q.requirement_type or '-',
            'requirement_summary': q.requirement_summary or '-',
            'detailed_requirements': q.detailed_requirements or '-',
            'timeline': q.timeline or '-',
            'industry': q.industry or '-',
            'budget_range': q.budget_range or '-',
            'status': q.status or '-',
            'created_at': q.created_at.strftime('%b %d, %Y') if q.created_at else '-'
        }
        
    def review_to_dict(r):
        return {
            'id': r.id,
            'name': r.name or '-',
            'job_title': r.job_title or '-',
            'company': r.company or '-',
            'industry': r.industry or '-',
            'rating': r.rating or '-',
            'feedback': r.feedback or '-',
            'created_at': r.created_at.strftime('%b %d, %Y') if r.created_at else '-'
        }
        
    def event_to_dict(e):
        return {
            'id': e.id,
            'name': e.name or '-',
            'job_title': e.job_title or '-',
            'company': e.company or '-',
            'email': e.email or '-',
            'event': {'title': e.event.title} if e.event else {'title': '-'},
            'message': e.message or '-',
            'created_at': e.created_at.strftime('%b %d, %Y') if e.created_at else '-'
        }

    def admin_login_required(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not session.get("admin_logged_in"):
                return redirect(url_for("admin_login"))  
            return f(*args, **kwargs)
        return decorated_function

    

    @app.route("/test-translation")
    def test_translation():
        return {
            'english': gettext('Hello World'),
            'current_locale': get_locale(),
            'session_language': session.get('language', 'Not set')
        }

    @app.route("/set_language/<language>")
    def set_language(language):
        if language in ['en', 'es', 'zh']:
            session['language'] = language
        return redirect(request.referrer or url_for('home'))

    @app.route("/")
    def home():
        return render_template("home.html")

    @app.route("/solutions")
    def solutions():
        return render_template("solutions.html")

    @app.route("/solutions/smart-assistant")
    def smart_assistant():
        return render_template("smart-assistant.html")

    @app.route("/solutions/virtual-work")
    def virtual_work():
        return render_template("virtual-work.html")
    
    @app.route("/solutions/task-automation")
    def task_automation():
        return render_template("task-automation.html")

    @app.route("/articles")
    def articles():
        return render_template("articles.html")

    @app.route("/articles/article-1")
    def article_1():
        return render_template("article-1.html")

    @app.route("/articles/article-2")
    def article_2():
        return render_template("article-2.html")

    @app.route("/articles/news-1")
    def news_1():
        return render_template("news-1.html")
    
    @app.route("/articles/news-2")
    def news_2():
        return render_template("news-2.html")

    @app.route("/reviews")
    def reviews_page():
        return render_template("reviews.html")
    
    @app.route("/privacy-policy")
    def privacy_policy():
        return render_template("privacy-policy.html")

    @app.route("/events")
    def events():
        return render_template("events.html")
    
    @app.route("/register")
    def register():
        event_id = request.args.get("event_id")
        event = None
        
        
        current_lang = session.get('language', 'en')

        
        events = {
            "1": {
                "en": {
                    "title": "AI Transforming Workplaces",
                    "date": "Jan 21, 2026",
                    "location": "INNSiDE By Melia Newcastle Venue Hire | Newcastle upon Tyne"
                },
                "es": {
                    "title": "IA Transformando Lugares de Trabajo",
                    "date": "21 de enero, 2026",
                    "location": "INNSiDE By Melia Contratación del Local | Newcastle upon Tyne"
                },
                "zh": {
                    "title": "AI改造工作场所",
                    "date": "2026年1月21日",
                    "location": "INNSiDE By Melia Newcastle 场地租赁 | 泰恩河畔纽卡斯尔"
                }
            },
            "2": {
                "en": {
                    "title": "Corporate AI Summit",
                    "date": "Feb 6, 2026",
                    "location": "Manchester Conference Centre | Manchester"
                },
                "es": {
                    "title": "Cumbre Corporativa de IA",
                    "date": "6 de febrero, 2026",
                    "location": "Centro de Conferencias de Manchester | Manchester"
                },
                "zh": {
                    "title": "企业AI峰会",
                    "date": "2026年2月6日",
                    "location": "曼彻斯特会议中心 | 曼彻斯特"
                }
            }
        }

        
        if event_id in events:
            event = events[event_id][current_lang]

        
        return render_template("register.html", event=event)

    @app.route("/contact")
    def contact():
        return render_template("contact.html")

    @app.route("/about")
    def about():
        return render_template("about.html")

    

    @app.route("/submit-contact", methods=["POST"])
    def submit_contact():
        
        name = request.form.get("name")
        email = request.form.get("email")
        phone = request.form.get("phone")
        company = request.form.get("company")
        job_title = request.form.get("job_title")
        country = request.form.get("country")
        requirement_type = request.form.get("requirement_type")
        other_requirement = request.form.get("other_requirement", "").strip()
        requirement_summary = request.form.get("requirement_summary")
        detailed_requirements = request.form.get("detailed_requirements")
        timeline = request.form.get("timeline")
        industry = request.form.get("industry")
        other_industry = request.form.get("other_industry", "").strip()
        budget_range = request.form.get("budget_range")

        
        if requirement_type == "Other" and not other_requirement:
            flash(gettext("Please specify your requirement."), "error")
            return redirect(url_for("contact"))

        
        if industry == "Other" and not other_industry:
            flash(gettext("Please specify your industry."), "error")
            return redirect(url_for("contact"))

        
        final_requirement = other_requirement if requirement_type == "Other" else requirement_type
        final_industry = other_industry if industry == "Other" else industry

        
        inquiry = Inquiry(
            name=name,
            email=email,
            phone=phone,
            company=company,
            job_title=job_title,
            country=country,
            requirement_type=final_requirement,
            requirement_summary=requirement_summary,
            detailed_requirements=detailed_requirements,
            timeline=timeline,
            industry=final_industry,
            budget_range=budget_range
        )
        
        db.session.add(inquiry)
        db.session.commit()

        flash(gettext("Thanks for your inquiry! We will get back to you within 4 working days."), "success")
        return redirect(url_for("contact"))

    

    @app.route("/api/submit-review", methods=["POST"])
    def submit_review():
        data = request.get_json()

        
        review_mode = data.get("review_mode", "normal")
        
        industry = data.get("industry", "").strip()
        feedback = data.get("feedback", "").strip()
        rating = data.get("rating")

        
        if review_mode == "anonymous":
            name = "Anonymous"
            job_title = "Someone"
            company = "A certain company"
        else:
            name = data.get("name", "").strip()
            job_title = data.get("job_title", "").strip()
            company = data.get("company", "").strip()

            if not name or not job_title or not company:
                return jsonify({
                    "error": "Name, job title, and company are required."
                }), 400 

        
        if not industry or not feedback:
            return jsonify({
                "error": "Industry and feedback are required."
            }), 400

        if not rating:
            return jsonify({"error": "Rating is required."}), 400

        try:
            rating = int(rating)
        except ValueError:
            return jsonify({"error": "Invalid rating value."}), 400

        if rating < 1 or rating > 5:
            return jsonify({"error": "Rating must be between 1 and 5."}), 400

        if len(feedback) < 30:
            return jsonify({
                "error": "Feedback must be at least 30 characters long."
            }), 400

        
        review = Review(
            name=name,
            job_title=job_title,
            company=company,
            industry=industry,
            rating=rating,
            feedback=feedback
        )
        
        try:
            db.session.add(review)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Database error saving review: {e}")
            return jsonify({"error": f"Failed to save review: {str(e)}"}), 500

        return jsonify({"message": "Review submitted successfully."}), 200

    

    @app.route("/admin-login", methods=["GET", "POST"])
    def admin_login():
        if request.method == "POST":
            staff_id = request.form.get("staff_id")
            password = request.form.get("password")
            admin = Admin.query.filter_by(staff_id=staff_id).first()
            if admin and check_password_hash(admin.password_hash, password):
                session["admin_logged_in"] = True
                session.permanent = True  
                return redirect(url_for("admin_dashboard"))
            flash("Invalid staff ID or password.", "danger")
        return render_template("admin-login.html")

    @app.route("/admin-dashboard")
    def admin_dashboard():
        inquiries = Inquiry.query.order_by(Inquiry.created_at.desc()).all()
        reviews = Review.query.order_by(Review.created_at.desc()).all()
        event_registrations = EventRegistration.query.order_by(EventRegistration.created_at.desc()).all()

        
        today = datetime.utcnow()
        inquiries_per_month = []
        for i in range(5, -1, -1):
            start = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0) - relativedelta(months=i)
            end = start + relativedelta(months=1)
            count = Inquiry.query.filter(Inquiry.created_at >= start, Inquiry.created_at < end).count()
            inquiries_per_month.append({'month': start.strftime('%b'), 'count': count})
            total_events = len(event_registrations)
            
        nearest_event = (
            Event.query
            .filter(Event.date >= today)
            .order_by(asc(Event.date))
            .first()
        )

        if nearest_event:
            registration_count = EventRegistration.query.filter_by(event_id=nearest_event.id).count()
            upcoming_event_info = {
                "title": nearest_event.title,
                "date": nearest_event.date.strftime("%b %d, %Y"),
                "location": nearest_event.location,
                "registrations": registration_count
            }
        else:
            upcoming_event_info = None
    
        return render_template(
            "admin-dashboard.html",
            total_inquiries=len(inquiries),
            total_reviews=len(reviews),
            total_events=total_events,

            pending_inquiries=sum(1 for q in inquiries if q.status == 'Pending'),
            contacted_inquiries=sum(1 for q in inquiries if q.status == 'Contacted'),
            recent_inquiries=[inquiry_to_dict(q) for q in inquiries[:10]],
            reviews=[review_to_dict(r) for r in reviews[:10]],
            event_registrations=[event_to_dict(e) for e in event_registrations[:10]],

            inquiries_per_month=inquiries_per_month,
            avg_rating=round(db.session.query(func.avg(Review.rating)).scalar() or 0, 1),
            upcoming_event=upcoming_event_info,
            current_year=datetime.utcnow().year
        )
        
    @app.route("/admin/inquiries")
    def admin_all_inquiries():
        all_inquiries = Inquiry.query.order_by(Inquiry.created_at.desc()).all()
        all_inquiries_dict = [inquiry_to_dict(q) for q in all_inquiries]
    
        total_inquiries = len(all_inquiries)
        pending_inquiries = sum(1 for q in all_inquiries if q.status == 'Pending')
        contacted_inquiries = sum(1 for q in all_inquiries if q.status == 'Contacted')

        return render_template(
            "admin-inquiries.html",
            all_inquiries=all_inquiries_dict,
            total_inquiries=total_inquiries,
            pending_inquiries=pending_inquiries,
            contacted_inquiries=contacted_inquiries,
            current_year=datetime.utcnow().year
        )

    @app.route("/admin/inquiry/<int:inquiry_id>/status", methods=["POST"])
    def update_inquiry_status(inquiry_id):
        inquiry = Inquiry.query.get_or_404(inquiry_id)
        new_status = request.form.get("status")
        if new_status not in ("Pending", "Contacted"):
            flash("Invalid status value.", "danger")
            return redirect(url_for("admin_dashboard"))

        inquiry.status = new_status
        db.session.commit()

        flash("Inquiry status updated.", "success")
        return redirect(url_for("admin_dashboard"))

    @app.route("/admin-logout")
    def admin_logout():
        session.clear()  
        session.pop("admin_logged_in", None)  
        return redirect(url_for("admin_login"))
    
    @app.route("/api/reviews-summary")
    def api_reviews_summary():
        from sqlalchemy import func

        
        avg_rating = db.session.query(func.avg(Review.rating)).scalar()
        avg_rating = round(avg_rating or 0, 1)  

        
        total_reviews = db.session.query(func.count(Review.id)).scalar()
    
        
        testimonials = Review.query.order_by(Review.created_at.desc()).limit(4).all()
        testimonials_data = [
            {
                "text": r.feedback,
                "author": f"{r.job_title}, {r.industry}"
            } for r in testimonials
        ]

        return {
            "average_rating": avg_rating,
            "total_reviews": total_reviews,
            "testimonials": testimonials_data
        }
        
    @app.route("/events/event-<int:event_id>")
    def event_detail(event_id):
        return render_template(f"event-{event_id}.html")
    
    @app.route("/api/inquiries")
    def api_inquiries():
        offset = int(request.args.get("offset", 0))
        limit = int(request.args.get("limit", 10))

        inquiries = Inquiry.query.order_by(Inquiry.created_at.desc()).offset(offset).limit(limit).all()
        total = Inquiry.query.count()
        return jsonify({
            "inquiries": [inquiry_to_dict(q) for q in inquiries],
            "total": total
        })

    @app.route("/api/reviews")
    def api_reviews():
        offset = int(request.args.get("offset", 0))
        limit = int(request.args.get("limit", 10))
        reviews = Review.query.order_by(Review.created_at.desc()).offset(offset).limit(limit).all()
        total = Review.query.count()

        return jsonify({
            "reviews": [review_to_dict(r) for r in reviews],
            "total": total
        })

    @app.route("/api/industries")
    def api_industries():
        """Get all unique industries from inquiries and reviews"""
        from sqlalchemy import distinct
        
        
        inquiry_industries = db.session.query(distinct(Inquiry.industry)).filter(Inquiry.industry.isnot(None)).all()
        inquiry_list = [industry[0] for industry in inquiry_industries if industry[0]]
        
        
        review_industries = db.session.query(distinct(Review.industry)).filter(Review.industry.isnot(None)).all()
        review_list = [industry[0] for industry in review_industries if industry[0]]
        
        
        all_industries = sorted(set(inquiry_list + review_list))
        
        return jsonify({
            "industries": all_industries,
            "total": len(all_industries)
        })

    @app.route("/api/inquiry-industries")
    def api_inquiry_industries():
        """Get industries from inquiries only"""
        from sqlalchemy import distinct
        
        industries = db.session.query(distinct(Inquiry.industry)).filter(Inquiry.industry.isnot(None)).all()
        industry_list = [industry[0] for industry in industries if industry[0]]
        
        return jsonify({
            "industries": sorted(industry_list),
            "total": len(industry_list)
        })

    @app.route("/api/review-industries")
    def api_review_industries():
        """Get industries from reviews only"""
        from sqlalchemy import distinct
        
        industries = db.session.query(distinct(Review.industry)).filter(Review.industry.isnot(None)).all()
        industry_list = [industry[0] for industry in industries if industry[0]]
        
        return jsonify({
            "industries": sorted(industry_list),
            "total": len(industry_list)
        })

    @app.route("/api/registered-events")
    def api_registered_events():
        """Get events that have registrations (only events with actual registrations)"""
        from sqlalchemy import distinct
        
        
        registered_events = (
            db.session.query(Event.title)
            .join(EventRegistration, Event.id == EventRegistration.event_id)
            .filter(Event.title.isnot(None))
            .distinct()
            .all()
        )
        
        event_list = [event[0] for event in registered_events if event[0]]
        
        return jsonify({
            "events": sorted(event_list),
            "total": len(event_list)
        })

    @app.route("/api/public-reviews")
    def api_public_reviews():
        """Public API endpoint for reviews - no authentication required"""
        offset = int(request.args.get("offset", 0))
        limit = int(request.args.get("limit", 10))
        reviews = Review.query.order_by(Review.created_at.desc()).offset(offset).limit(limit).all()
        total = Review.query.count()

        return jsonify({
            "reviews": [review_to_dict(r) for r in reviews],
            "total": total
        })

    @app.route("/api/admin/events")
    def api_admin_events():
        offset = int(request.args.get("offset", 0))
        limit = int(request.args.get("limit", 10))
        registrations = (
            EventRegistration.query
            .order_by(EventRegistration.created_at.desc())
            .offset(offset)
            .limit(limit)
            .all()
        )
        total = EventRegistration.query.count()

        return jsonify({
            "events": [event_to_dict(r) for r in registrations],
            "total": total
        })
  
    @app.route("/api/events")
    def api_get_events():
        filter_type = request.args.get("filter", "upcoming")
        language = request.args.get("language", "en")  
        try:
            offset = int(request.args.get("offset", 0))
            limit = int(request.args.get("limit", 6))
        except ValueError:
            offset = 0
            limit = 6
        now = datetime.utcnow()

        query = Event.query
        if filter_type == "upcoming":
            query = query.filter(Event.date >= now).order_by(asc(Event.date))
        elif filter_type == "past":
            query = query.filter(Event.date < now).order_by(desc(Event.date))
        else:
            query = query.order_by(asc(Event.date))
        total_events = query.count()
        events = query.offset(offset).limit(limit).all()

        events_data = [
            {
                "id": e.id,
                "title": e.get_translated_title(language),
                "description": e.get_translated_description(language),
                "date": e.get_translated_date(language),
                "location": e.get_translated_location(language),
                "image": e.image,
                "detail_url": f"/events/event-{e.id}"  
            }
            for e in events
        ]
        return {"events": events_data, "total": total_events}
    
    @app.route("/api/events/featured")
    def api_featured_event():
        language = request.args.get("language", "en")  
        now = datetime.utcnow()

        event = (
            Event.query
            .filter(Event.date >= now)
            .order_by(asc(Event.date))
            .first()
        )

        if not event:
            return {"event": None}
        return {
            "event": {
                "id": event.id,
                "title": event.get_translated_title(language),
                "description": event.get_translated_description(language),
                "date": event.get_translated_date(language),
                "location": event.get_translated_location(language),
                "image": event.image,
                "detail_url": f"/events/event-{event.id}"  
            }
        }
        
    @app.route("/submit-event-registration", methods=["POST"])
    def submit_event_registration():
        try:
            
            event_id = request.form.get("event_id")
            name = request.form.get("name")
            email = request.form.get("email")
            company = request.form.get("company")
            job_title = request.form.get("job_title")
            message = request.form.get("message")

            
            registration = EventRegistration(
                event_id=event_id,
                name=name,
                email=email,
                company=company,
                job_title=job_title,
                message=message
            )
            db.session.add(registration)
            db.session.commit()
            
            flash(gettext("Registration successful! You will be informed with event details in your email. Thank you."), "success")
        except Exception as e:
            db.session.rollback()
            flash(gettext("Oops! Something went wrong. Please try again later."), "error")

        
        return redirect(url_for("register", event_id=event_id))
    
    @app.route("/api/articles-latest")
    def latest_articles():
        
        articles = {
            'en': [
                {
                    "title": "AI Transforming Digital Workplaces",
                    "image": "/static/images/article-image-1.jpg",
                    "snippet": "How AI-driven tools enhance productivity and streamline operations.",
                    "link": "/articles/article-1"
                },
                {
                    "title": "Proactive AI Issue Resolution",
                    "image": "/static/images/article-image-2.jpg",
                    "snippet": "Reducing downtime and optimizing workflow with intelligent AI solutions.",
                    "link": "/articles/article-2"
                },
                {
                    "title": "Industry-Specific AI Solutions",
                    "image": "/static/images/article-image-3.jpg",
                    "snippet": "Tailored AI software solutions for healthcare, finance, and IT sectors.",
                    "link": "/articles/article-3"
                }
            ],
            'es': [
                {
                    "title": "IA Transformando Lugares de Trabajo Digitales",
                    "image": "/static/images/article-image-1.jpg",
                    "snippet": "Cómo las herramientas impulsadas por IA mejoran la productividad y optimizan operaciones.",
                    "link": "/articles/article-1"
                },
                {
                    "title": "Resolución Proactiva de Problemas con IA",
                    "image": "/static/images/article-image-2.jpg",
                    "snippet": "Reduciendo el tiempo de inactividad y optimizando flujos de trabajo con soluciones de IA inteligentes.",
                    "link": "/articles/article-2"
                },
                {
                    "title": "Soluciones de IA Específicas por Industria",
                    "image": "/static/images/article-image-3.jpg",
                    "snippet": "Soluciones de software de IA personalizadas para sectores de salud, finanzas y TI.",
                    "link": "/articles/article-3"
                }
            ],
            'zh': [
                {
                    "title": "AI转型数字工作场所",
                    "image": "/static/images/article-image-1.jpg",
                    "snippet": "AI驱动的工具如何提高生产力并简化操作。",
                    "link": "/articles/article-1"
                },
                {
                    "title": "主动AI问题解决",
                    "image": "/static/images/article-image-2.jpg",
                    "snippet": "通过智能AI解决方案减少停机时间并优化工作流程。",
                    "link": "/articles/article-2"
                },
                {
                    "title": "行业特定AI解决方案",
                    "image": "/static/images/article-image-3.jpg",
                    "snippet": "为医疗保健、金融和IT行业量身定制的AI软件解决方案。",
                    "link": "/articles/article-3"
                }
            ]
        }
        
        
        current_lang = get_locale()
        
        
        return jsonify(articles.get(current_lang, articles['en']))
    
    @app.route("/api/chatbot", methods=["POST"])
    def chatbot_response():
        """Multi-language AI Chatbot API endpoint"""
        try:
            data = request.get_json()
            user_message = data.get("message", "").strip()
            language = data.get("language", "en")  
            
            if not user_message:
                return jsonify({"response": get_response("no_message", language)})
            
            
            detected_language = detect_language(user_message)
            if detected_language != language:
                language = detected_language
            
            
            response = get_chatbot_response(user_message.lower(), language)
            return jsonify({"response": response, "language": language})
            
        except Exception as e:
            return jsonify({"response": "I apologize, but I'm experiencing technical difficulties. Please try again later or contact us directly."})
    
    def detect_language(message):
        """Simple language detection based on keywords"""
        message_lower = message.lower()
        
        
        spanish_keywords = ["hola", "gracias", "adiós", "por favor", "qué", "cómo", "dónde", "cuándo", "soluciones", "servicios", "contacto"]
        if any(keyword in message_lower for keyword in spanish_keywords):
            return "es"
        
        
        chinese_keywords = ["你好", "谢谢", "再见", "请问", "什么", "如何", "哪里", "何时", "解决方案", "服务", "联系"]
        if any(keyword in message_lower for keyword in chinese_keywords):
            return "zh"
        
        
        return "en"
    
    def get_chatbot_response(user_message, language):
        """Get chatbot response in the specified language"""
        
        
        knowledge_base = {
            "en": {
                "greetings": ["hello", "hi", "hey", "good morning", "good afternoon"],
                "thanks": ["thank", "thanks", "appreciate"],
                "goodbye": ["bye", "goodbye", "farewell"],
                "what_is_ai_solution": ["what is ai-solution", "what is ai solution", "tell me about ai-solution"],
                "who_are_you": ["who are you", "what are you"],
                "about_company": ["about company", "about ai-solution", "company information"],
                "solutions": ["solutions", "what solutions", "what do you offer"],
                "smart_assistant": ["smart assistant", "smart assistants"],
                "task_automation": ["task automation", "automation"],
                "virtual_work": ["virtual work", "virtual assistant"],
                "virtual_work_summary": ["tell me about virtual work assistant", "virtual work assistant summary", "explain virtual work assistant"],
                "task_automation_summary": ["tell me about task automation", "task automation summary", "explain task automation"],
                "virtual_work_features": ["virtual work assistant features", "what does virtual work assistant do"],
                "task_automation_features": ["task automation features", "what does task automation do"],
                "workflow_automation": ["workflow automation", "automate workflows"],
                "system_integration": ["system integration", "integrate systems"],
                "task_management": ["task management", "manage tasks"],
                "scheduling": ["scheduling", "schedule meetings"],
                "knowledge_retrieval": ["knowledge retrieval", "retrieve documents"],
                "intelligent_rule_engine": ["intelligent rule engine", "business rules"],
                "virtual_work": ["virtual work", "virtual assistant"],
                "industries": ["industries", "what industries", "which industries"],
                "services": ["services", "what services"],
                "contact": ["contact", "how to contact", "reach you"],
                "events": ["events", "workshops", "conferences"],
                "pricing": ["pricing", "cost", "price"],
                "process": ["process", "how does it work", "implementation"],
                "vision": ["vision", "what is your vision", "company vision"],
                "mission": ["mission", "what is your mission", "company mission"],
                "values": ["values", "core values", "what are your values"],
                "location": ["location", "where are you located", "address", "office"],
                "headquarters": ["headquarters", "main office", "where is your headquarters"],
                "office_hours": ["office hours", "working hours", "when are you open"],
                "sunderland": ["sunderland", "where is sunderland", "sunderland uk"]
            },
            "es": {
                "greetings": ["hola", "buenos días", "buenas tardes", "buenas noches"],
                "thanks": ["gracias", "agradecido", "agradecida"],
                "goodbye": ["adiós", "chao", "hasta luego", "hasta pronto"],
                "what_is_ai_solution": ["qué es ai-solution", "qué es ai solution", "dime sobre ai-solution"],
                "who_are_you": ["quién eres", "qué eres"],
                "about_company": ["sobre la empresa", "sobre ai-solution", "información de la empresa"],
                "solutions": ["soluciones", "qué soluciones", "qué ofrecen"],
                "smart_assistant": ["asistente inteligente", "asistentes inteligentes"],
                "task_automation": ["automatización de tareas", "automatización"],
                "virtual_work": ["trabajo virtual", "asistente virtual"],
                "virtual_work_summary": ["dime sobre asistente virtual", "resumen asistente virtual", "explica asistente virtual"],
                "task_automation_summary": ["dime sobre automatización de tareas", "resumen automatización de tareas", "explica automatización de tareas"],
                "virtual_work_features": ["características asistente virtual", "qué hace asistente virtual"],
                "task_automation_features": ["características automatización de tareas", "qué hace automatización de tareas"],
                "workflow_automation": ["automatización de flujos de trabajo", "automatizar flujos"],
                "system_integration": ["integración de sistemas", "integrar sistemas"],
                "task_management": ["gestión de tareas", "gestionar tareas"],
                "scheduling": ["programación", "programar reuniones"],
                "knowledge_retrieval": ["recuperación de conocimiento", "recuperar documentos"],
                "intelligent_rule_engine": ["motor de reglas inteligente", "reglas de negocio"],
                "industries": ["industrias", "qué industrias", "cuáles industrias"],
                "services": ["servicios", "qué servicios"],
                "contact": ["contacto", "cómo contactar", "contactar"],
                "events": ["eventos", "talleres", "conferencias"],
                "pricing": ["precios", "costo", "precio"],
                "process": ["proceso", "cómo funciona", "implementación"],
                "vision": ["visión", "cuál es su visión", "visión de la empresa"],
                "mission": ["misión", "cuál es su misión", "misión de la empresa"],
                "values": ["valores", "valores fundamentales", "cuáles son sus valores"],
                "location": ["ubicación", "dónde están ubicados", "dirección", "oficina"],
                "headquarters": ["sede principal", "oficina principal", "dónde está la sede"],
                "office_hours": ["horario de oficina", "horario laboral", "cuándo están abiertos"],
                "sunderland": ["sunderland", "dónde está sunderland", "sunderland reino unido"]
            },
            "zh": {
                "greetings": ["你好", "您好", "早上好", "下午好", "晚上好"],
                "thanks": ["谢谢", "感谢"],
                "goodbye": ["再见", "拜拜", "下次见"],
                "what_is_ai_solution": ["ai-solution是什么", "ai solution是什么", "告诉我ai-solution"],
                "who_are_you": ["你是谁", "你是什么"],
                "about_company": ["关于公司", "关于ai-solution", "公司信息"],
                "solutions": ["解决方案", "什么解决方案", "你们提供什么"],
                "smart_assistant": ["智能助手", "智能助理"],
                "task_automation": ["任务自动化", "自动化"],
                "virtual_work": ["虚拟工作", "虚拟助理"],
                "virtual_work_summary": ["告诉我虚拟工作助理", "虚拟工作助理总结", "解释虚拟工作助理"],
                "task_automation_summary": ["告诉我任务自动化", "任务自动化总结", "解释任务自动化"],
                "virtual_work_features": ["虚拟工作助理功能", "虚拟工作助理做什么"],
                "task_automation_features": ["任务自动化功能", "任务自动化做什么"],
                "workflow_automation": ["工作流程自动化", "自动化工作流程"],
                "system_integration": ["系统集成", "集成系统"],
                "task_management": ["任务管理", "管理任务"],
                "scheduling": ["日程安排", "安排会议"],
                "knowledge_retrieval": ["知识检索", "检索文档"],
                "intelligent_rule_engine": ["智能规则引擎", "业务规则"],
                "industries": ["行业", "什么行业", "哪些行业"],
                "services": ["服务", "什么服务"],
                "contact": ["联系", "如何联系", "联系方式"],
                "events": ["活动", "研讨会", "会议"],
                "pricing": ["价格", "费用", "成本"],
                "process": ["流程", "如何工作", "实施"],
                "vision": ["愿景", "你们的愿景", "公司愿景"],
                "mission": ["使命", "你们的使命", "公司使命"],
                "values": ["价值观", "核心价值观", "你们的价值观"],
                "location": ["位置", "你们在哪里", "地址", "办公室"],
                "headquarters": ["总部", "主办公室", "总部在哪里"],
                "office_hours": ["办公时间", "工作时间", "什么时候开放"],
                "sunderland": ["桑德兰", "桑德兰在哪里", "桑德兰英国"]
            }
        }
        
        
        responses = {
            "en": {
                "no_message": "I didn't receive a message. How can I help you?",
                "greeting": "Hello! I'm the AI-Solution assistant. How can I help you today?",
                "thanks": "You're welcome! Is there anything else I can help you with?",
                "goodbye": "Goodbye! Feel free to come back anytime you have questions about AI-Solution. Have a great day!",
                "what_is_ai_solution": "AI-Solution is a leading provider of AI-powered digital workplace solutions. We specialize in creating intelligent systems that help businesses automate workflows, enhance employee experiences, and drive digital transformation.",
                "who_are_you": "I'm the AI-Solution assistant, here to help you learn about our AI-powered digital workplace solutions. Feel free to ask me anything about our services, solutions, or company!",
                "about_company": "AI-Solution innovates the future of digital employee experiences with AI-powered solutions. We help businesses transform their digital workplaces through intelligent automation, smart assistants, and data-driven insights.",
                "solutions": "We offer comprehensive AI solutions including:\n• Smart Assistant Solutions\n• Task Automation\n• Virtual Work Assistants\n• Predictive Analytics\n• AI Chatbots\n• Computer Vision\n• Custom AI Solutions\n\nEach solution is tailored to your specific industry needs.",
                "smart_assistant": "Our Smart Assistant solutions use AI to proactively support employees in their daily workflows. These tools reduce manual effort, streamline communication, and enhance the overall digital employee experience.",
                "task_automation": "Our Task Automation solution helps you automate repetitive workflows and operational tasks with intelligent AI agents. This increases efficiency and allows your team to focus on high-value activities.",
                "virtual_work": "Our Virtual Work Assistant streamlines tasks, schedules, and queries with an AI-powered virtual assistant. It's designed to help remote and hybrid teams work more efficiently.",
                "virtual_work_summary": "The Virtual Work Assistant is a comprehensive AI-powered solution that helps employees manage their daily tasks, schedule meetings, and retrieve company knowledge efficiently. It increases productivity, reduces errors, and automates repetitive tasks to free up valuable time for strategic work.",
                "task_automation_summary": "The Task Automation Assistant is designed to eliminate manual, repetitive work by automating routine business processes across departments. From approvals and data entry to workflow orchestration, it enables teams to operate faster, reduce errors, and focus on high-value initiatives.",
                "virtual_work_features": "The Virtual Work Assistant includes these key features:\n• Task Management - Automates daily task assignments and tracking to save time and improve efficiency\n• Scheduling - Optimizes meetings and appointments, integrating with calendars automatically\n• Knowledge Retrieval - Instantly retrieves company documentation and guidelines using AI search",
                "task_automation_features": "The Task Automation Assistant provides these powerful features:\n• Workflow Automation - Automates end-to-end workflows including approvals, escalations, and notifications\n• System Integration - Seamlessly integrates with enterprise systems, CRMs, ERPs, and internal tools\n• Intelligent Rule Engine - Executes business rules dynamically based on conditions, priorities, and data inputs",
                "workflow_automation": "Our workflow automation feature handles end-to-end business processes including approvals, escalations, and notifications. It streamlines complex workflows to reduce manual intervention and improve process efficiency.",
                "system_integration": "Our system integration capability seamlessly connects with enterprise systems, CRMs, ERPs, and internal tools. This ensures smooth data flow and eliminates silos between different business applications.",
                "task_management": "Our task management feature automates daily task assignments and tracking to save time and improve efficiency. It helps teams stay organized and focused on priority activities.",
                "scheduling": "Our scheduling feature optimizes meetings and appointments, integrating with calendars automatically. It reduces scheduling conflicts and ensures efficient time management.",
                "knowledge_retrieval": "Our knowledge retrieval feature instantly retrieves company documentation and guidelines using AI search. Employees can quickly find the information they need without manual searching.",
                "intelligent_rule_engine": "Our intelligent rule engine executes business rules dynamically based on conditions, priorities, and data inputs. It enables automated decision-making and process execution without human intervention.",
                "industries": "We serve multiple industries including:\n• Healthcare\n• Finance\n• Retail & E-commerce\n• Education & EdTech\n• Manufacturing\n• Logistics & Supply Chain\n• Technology & AI Startups\n\nOur solutions are customized for each industry's unique challenges.",
                "healthcare": "In healthcare, we provide AI solutions for patient care automation, medical imaging analysis, administrative workflow optimization, and predictive health analytics.",
                "finance": "For the finance sector, we offer fraud detection, automated trading systems, customer service chatbots, risk assessment tools, and regulatory compliance automation.",
                "services": "Our services include:\n• AI Solution Development\n• Digital Transformation Consulting\n• Workflow Automation\n• Employee Experience Enhancement\n• Data Analytics & Insights\n• Custom AI Integration\n• Training & Support",
                "contact": "You can reach us through:\n• Contact Form: /contact\n• Email: info@ai-solution.com\n• Phone: +1 (555) 123-4567\n\nWe typically respond within 4 working days.",
                "support": "For support, please visit our contact page or call our support team. We're here to help you get the most out of your AI solutions.",
                "events": "We regularly host events including workshops, summits, and conferences. Check our /events page for upcoming AI Innovation Workshops, Corporate AI Summits, and industry-specific meetups.",
                "workshop": "We offer hands-on AI workshops covering innovation strategies, implementation best practices, and industry-specific use cases. Visit our events page to see upcoming workshops.",
                "pricing": "Our pricing is customized based on your specific needs, solution complexity, and implementation requirements. Contact us for a personalized quote and consultation.",
                "process": "Our process typically involves:\n1. Discovery & Consultation\n2. Solution Design\n3. Rapid Prototyping\n4. Implementation\n5. Training & Support\n6. Ongoing Optimization",
                "vision": "Our vision is to shape the future of digital employee experience by enabling organizations worldwide to work smarter, faster, and more efficiently through AI-driven innovation.",
                "mission": "Our mission is to design and deliver AI-powered solutions that proactively support people at work, enhance productivity, and accelerate innovation across industries.",
                "values": "Our core values are:\n• Innovation - Continuously pushing boundaries to deliver intelligent, forward-thinking AI solutions\n• Trust & Security - Building secure, reliable solutions with transparency at every stage\n• People First - Designing AI that empowers people, enhances work, and supports collaboration\n• AI Excellence - Applying deep AI expertise to deliver measurable, real-world impact",
                "location": "Our headquarters is located in Sunderland, United Kingdom. We're strategically positioned in the heart of Sunderland's innovation district.",
                "headquarters": "AI-Solution's headquarters is in Sunderland, United Kingdom. Our modern office space is designed to foster collaboration and innovation.",
                "office_hours": "Our office hours are:\n• Monday - Friday: 9:00 AM - 6:00 PM\n• Saturday: 10:00 AM - 2:00 PM\n• Sunday: Closed",
                "sunderland": "AI-Solution is proud to be based in Sunderland, United Kingdom. Visit us to see how innovation meets excellence in our modern office space.",
                "default_responses": [
                    "I'm not sure about that specific question, but I'd be happy to tell you about our AI solutions, services, or company. What interests you most?",
                    "That's an interesting question! While I may not have specific information on that, I can help you learn about our smart assistants, automation solutions, or industry-specific offerings.",
                    "I might not have the answer to that, but I can definitely help you understand how AI-Solution can transform your digital workplace. What would you like to explore?",
                    "Great question! Let me direct you to what I know best - our AI solutions, services, and how we help businesses like yours. What area interests you?"
                ]
            },
            "es": {
                "no_message": "No recibí un mensaje. ¿Cómo puedo ayudarte?",
                "greeting": "¡Hola! Soy el asistente de AI-Solution. ¿Cómo puedo ayudarte hoy?",
                "thanks": "¡De nada! ¿Hay algo más en lo que pueda ayudarte?",
                "goodbye": "¡Adiós! No dudes en volver cuando tengas preguntas sobre AI-Solution. ¡Que tengas un gran día!",
                "what_is_ai_solution": "AI-Solution es un proveedor líder de soluciones digitales de lugar de trabajo impulsadas por IA. Nos especializamos en crear sistemas inteligentes que ayudan a las empresas a automatizar flujos de trabajo, mejorar las experiencias de los empleados e impulsar la transformación digital.",
                "who_are_you": "Soy el asistente de AI-Solution, aquí para ayudarte a conocer nuestras soluciones digitales de lugar de trabajo impulsadas por IA. No dudes en preguntarme cualquier cosa sobre nuestros servicios, soluciones o empresa.",
                "about_company": "AI-Solution innova el futuro de las experiencias digitales de los empleados con soluciones impulsadas por IA. Ayudamos a las empresas a transformar sus lugares de trabajo digitales a través de automatización inteligente, asistentes inteligentes e información basada en datos.",
                "solutions": "Ofrecemos soluciones integrales de IA que incluyen:\n• Soluciones de Asistente Inteligente\n• Automatización de Tareas\n• Asistentes de Trabajo Virtual\n• Análisis Predictivo\n• Chatbots de IA\n• Visión por Computadora\n• Soluciones de IA Personalizadas\n\nCada solución está adaptada a las necesidades específicas de tu industria.",
                "smart_assistant": "Nuestras soluciones de Asistente Inteligente utilizan IA para apoyar proactivamente a los empleados en sus flujos de trabajo diarios. Estas herramientas reducen el esfuerzo manual, agilizan la comunicación y mejoran la experiencia digital general del empleado.",
                "task_automation": "Nuestra solución de Automatización de Tareas te ayuda a automatizar flujos de trabajo repetitivos y tareas operativas con agentes de IA inteligentes. Esto aumenta la eficiencia y permite que tu equipo se centre en actividades de alto valor.",
                "virtual_work": "Nuestro Asistente de Trabajo Virtual agiliza tareas, horarios y consultas con un asistente virtual impulsado por IA. Está diseñado para ayudar a los equipos remotos e híbridos a trabajar más eficientemente.",
                "virtual_work_summary": "El Asistente de Trabajo Virtual es una solución integral impulsada por IA que ayuda a los empleados a gestionar sus tareas diarias, programar reuniones y recuperar conocimiento de la empresa eficientemente. Aumenta la productividad, reduce errores y automatiza tareas repetitivas para liberar tiempo valioso para trabajo estratégico.",
                "task_automation_summary": "El Asistente de Automatización de Tareas está diseñado para eliminar el trabajo manual y repetitivo automatizando procesos comerciales rutinarios en todos los departamentos. Desde aprobaciones y entrada de datos hasta orquestación de flujos de trabajo, permite a los equipos operar más rápido, reducir errores y enfocarse en iniciativas de alto valor.",
                "virtual_work_features": "El Asistente de Trabajo Virtual incluye estas características clave:\n• Gestión de Tareas - Automata asignaciones y seguimiento de tareas diarias para ahorrar tiempo y mejorar la eficiencia\n• Programación - Optimiza reuniones y citas, integrándose con calendarios automáticamente\n• Recuperación de Conocimiento - Recupera instantáneamente documentación y directrices de la empresa usando búsqueda de IA",
                "task_automation_features": "El Asistente de Automatización de Tareas proporciona estas características poderosas:\n• Automatización de Flujos de Trabajo - Automata flujos de trabajo de extremo a extremo incluyendo aprobaciones, escalaciones y notificaciones\n• Integración de Sistemas - Se integra perfectamente con sistemas empresariales, CRMs, ERPs y herramientas internas\n• Motor de Reglas Inteligente - Ejecuta reglas comerciales dinámicamente basado en condiciones, prioridades y entradas de datos",
                "workflow_automation": "Nuestra característica de automatización de flujos de trabajo maneja procesos comerciales de extremo a extremo incluyendo aprobaciones, escalaciones y notificaciones. Optimiza flujos de trabajo complejos para reducir la intervención manual y mejorar la eficiencia del proceso.",
                "system_integration": "Nuestra capacidad de integración de sistemas se conecta perfectamente con sistemas empresariales, CRMs, ERPs y herramientas internas. Esto asegura un flujo de datos suave y elimina silos entre diferentes aplicaciones comerciales.",
                "task_management": "Nuestra característica de gestión de tareas automatiza asignaciones y seguimiento de tareas diarias para ahorrar tiempo y mejorar la eficiencia. Ayuda a los equipos a mantenerse organizados y enfocados en actividades prioritarias.",
                "scheduling": "Nuestra característica de programación optimiza reuniones y citas, integrándose con calendarios automáticamente. Reduce conflictos de programación y asegura una gestión eficiente del tiempo.",
                "knowledge_retrieval": "Nuestra característica de recuperación de conocimiento recupera instantáneamente documentación y directrices de la empresa usando búsqueda de IA. Los empleados pueden encontrar rápidamente la información que necesitan sin búsqueda manual.",
                "intelligent_rule_engine": "Nuestro motor de reglas inteligente ejecuta reglas comerciales dinámicamente basado en condiciones, prioridades y entradas de datos. Permite la toma de decisiones automatizada y ejecución de procesos sin intervención humana.",
                "industries": "Servimos a múltiples industrias incluyendo:\n• Salud\n• Finanzas\n• Retail y Comercio Electrónico\n• Educación y EdTech\n• Manufactura\n• Logística y Cadena de Suministro\n• Tecnología y Startups de IA\n\nNuestras soluciones están personalizadas para los desafíos únicos de cada industria.",
                "healthcare": "En salud, proporcionamos soluciones de IA para automatización del cuidado del paciente, análisis de imágenes médicas, optimización de flujos de trabajo administrativos y análisis predictivo de salud.",
                "finance": "Para el sector financiero, ofrecemos detección de fraude, sistemas de trading automatizados, chatbots de servicio al cliente, herramientas de evaluación de riesgos y automatización de cumplimiento regulatorio.",
                "services": "Nuestros servicios incluyen:\n• Desarrollo de Soluciones de IA\n• Consultoría de Transformación Digital\n• Automatización de Flujos de Trabajo\n• Mejora de Experiencia del Empleado\n• Análisis de Datos e Información\n• Integración de IA Personalizada\n• Capacitación y Soporte",
                "contact": "Puedes contactarnos a través de:\n• Formulario de Contacto: /contact\n• Email: info@ai-solution.com\n• Teléfono: +1 (555) 123-4567\n\nNormalmente respondemos dentro de 4 días hábiles.",
                "support": "Para soporte, por favor visita nuestra página de contacto o llama a nuestro equipo de soporte. Estamos aquí para ayudarte a aprovechar al máximo tus soluciones de IA.",
                "events": "Organizamos regularmente eventos incluyendo talleres, cumbres y conferencias. Revisa nuestra página /events para próximos Talleres de Innovación en IA, Cumbres Corporativas de IA y encuentros específicos de la industria.",
                "workshop": "Ofrecemos talleres prácticos de IA cubriendo estrategias de innovación, mejores prácticas de implementación y casos de uso específicos de la industria. Visita nuestra página de eventos para ver próximos talleres.",
                "pricing": "Nuestros precios se personalizan según tus necesidades específicas, complejidad de la solución y requisitos de implementación. Contáctanos para una cotización y consulta personalizada.",
                "process": "Nuestro proceso típicamente involucra:\n1. Descubrimiento y Consulta\n2. Diseño de Solución\n3. Prototipado Rápido\n4. Implementación\n5. Capacitación y Soporte\n6. Optimización Continua",
                "vision": "Nuestra visión es dar forma al futuro de la experiencia digital del empleado habilitando organizaciones worldwide para trabajar más inteligentemente, más rápido y más eficientemente a través de la innovación impulsada por IA.",
                "mission": "Nuestra misión es diseñar y entregar soluciones impulsadas por IA que apoyen proactivamente a las personas en el trabajo, mejoren la productividad y aceleren la innovación en todas las industrias.",
                "values": "Nuestros valores fundamentales son:\n• Innovación - Impulsando continuamente los límites para entregar soluciones de IA inteligentes y con visión de futuro\n• Confianza y Seguridad - Construyendo soluciones seguras y confiables con transparencia en cada etapa\n• Personas Primero - Diseñando IA que empodera a las personas, mejora el trabajo y apoya la colaboración\n• Excelencia en IA - Aplicando experiencia profunda en IA para entregar impacto medible del mundo real",
                "location": "Nuestra sede está ubicada en Sunderland, Reino Unido. Estamos posicionados estratégicamente en el corazón del distrito de innovación de Sunderland.",
                "headquarters": "La sede de AI-Solution está en Sunderland, Reino Unido. Nuestro espacio de oficina moderno está diseñado para fomentar la colaboración y la innovación.",
                "office_hours": "Nuestro horario de oficina es:\n• Lunes - Viernes: 9:00 de la mañana - 6:00 de la tarde\n• Sábado: 10:00 de la mañana - 2:00 de la tarde\n• Domingo: Cerrado",
                "sunderland": "AI-Solution se enorgullece de estar basada en Sunderland, Reino Unido. Visítanos para ver cómo la innovación se encuentra con la excelencia en nuestro espacio de oficina moderno.",
                "default_responses": [
                    "No estoy seguro sobre esa pregunta específica, pero estaré feliz de contarte sobre nuestras soluciones de IA, servicios o empresa. ¿Qué te interesa más?",
                    "¡Esa es una pregunta interesante! Aunque pueda no tener información específica sobre eso, puedo ayudarte a conocer nuestros asistentes inteligentes, soluciones de automatización u ofertas específicas de la industria.",
                    "Puede que no tenga la respuesta a eso, pero definitivamente puedo ayudarte a entender cómo AI-Solution puede transformar tu lugar de trabajo digital. ¿Qué te gustaría explorar?",
                    "¡Gran pregunta! Permíteme dirigirte a lo que mejor conozco - nuestras soluciones de IA, servicios y cómo ayudamos a empresas como la tuya. ¿Qué área te interesa?"
                ]
            },
            "zh": {
                "no_message": "我没有收到消息。我该如何帮助您？",
                "greeting": "您好！我是AI-Solution的助手。今天我该如何帮助您？",
                "thanks": "不客气！还有什么我可以帮助您的吗？",
                "goodbye": "再见！欢迎您随时回来询问关于AI-Solution的问题。祝您有美好的一天！",
                "what_is_ai_solution": "AI-Solution是AI驱动的数字工作场所解决方案的领先提供商。我们专门创建智能系统，帮助企业自动化工作流程、增强员工体验并推动数字化转型。",
                "who_are_you": "我是AI-Solution的助手，在这里帮助您了解我们的AI驱动数字工作场所解决方案。请随时询问我关于我们的服务、解决方案或公司的任何问题。",
                "about_company": "AI-Solution通过AI驱动的解决方案创新数字员工体验的未来。我们通过智能自动化、智能助手和数据驱动的洞察帮助企业转变其数字工作场所。",
                "solutions": "我们提供全面的AI解决方案，包括：\n• 智能助手解决方案\n• 任务自动化\n• 虚拟工作助手\n• 预测分析\n• AI聊天机器人\n• 计算机视觉\n• 定制AI解决方案\n\n每个解决方案都根据您的特定行业需求量身定制。",
                "smart_assistant": "我们的智能助手解决方案使用AI主动支持员工的日常工作流程。这些工具减少手动工作、简化沟通并增强整体数字员工体验。",
                "task_automation": "我们的任务自动化解决方案帮助您使用智能AI代理自动化重复性工作流程和运营任务。这提高效率并让您的团队专注于高价值活动。",
                "virtual_work": "我们的虚拟工作助手通过AI驱动的虚拟助手简化任务、日程和查询。它旨在帮助远程和混合团队更有效地工作。",
                "virtual_work_summary": "虚拟工作助手是一个全面的AI驱动解决方案，帮助员工高效管理日常任务、安排会议和检索公司知识。它提高生产力、减少错误并自动化重复性任务，为战略性工作释放宝贵时间。",
                "task_automation_summary": "任务自动化助手旨在通过自动化各部门的常规业务流程来消除手动重复性工作。从审批和数据输入到工作流程编排，它使团队能够更快地运营、减少错误并专注于高价值计划。",
                "virtual_work_features": "虚拟工作助手包含这些关键功能：\n• 任务管理 - 自动化日常任务分配和跟踪以节省时间并提高效率\n• 日程安排 - 优化会议和约会，自动集成日历\n• 知识检索 - 使用AI搜索即时检索公司文档和指南",
                "task_automation_features": "任务自动化助手提供这些强大功能：\n• 工作流程自动化 - 自动化端到端工作流程，包括审批、升级和通知\n• 系统集成 - 与企业系统、CRM、ERP和内部工具无缝集成\n• 智能规则引擎 - 基于条件、优先级和数据输入动态执行业务规则",
                "workflow_automation": "我们的工作流程自动化功能处理端到端业务流程，包括审批、升级和通知。它简化复杂工作流程以减少手动干预并提高流程效率。",
                "system_integration": "我们的系统集成能力与企业系统、CRM、ERP和内部工具无缝连接。这确保数据流畅通并消除不同业务应用程序之间的孤岛。",
                "task_management": "我们的任务管理功能自动化日常任务分配和跟踪以节省时间并提高效率。它帮助团队保持组织性并专注于优先活动。",
                "scheduling": "我们的日程安排功能优化会议和约会，自动集成日历。它减少日程冲突并确保高效的时间管理。",
                "knowledge_retrieval": "我们的知识检索功能使用AI搜索即时检索公司文档和指南。员工可以快速找到他们需要的信息，无需手动搜索。",
                "intelligent_rule_engine": "我们的智能规则引擎基于条件、优先级和数据输入动态执行业务规则。它支持自动化决策制定和流程执行，无需人工干预。",
                "industries": "我们服务多个行业，包括：\n• 医疗保健\n• 金融\n• 零售和电子商务\n• 教育和教育科技\n• 制造业\n• 物流和供应链\n• 技术和AI初创公司\n\n我们的解决方案为每个行业的独特挑战量身定制。",
                "healthcare": "在医疗保健领域，我们为患者护理自动化、医学影像分析、管理工作流程优化和预测性健康分析提供AI解决方案。",
                "finance": "对于金融部门，我们提供欺诈检测、自动化交易系统、客户服务聊天机器人、风险评估工具和监管合规自动化。",
                "services": "我们的服务包括：\n• AI解决方案开发\n• 数字转型咨询\n• 工作流程自动化\n• 员工体验增强\n• 数据分析和洞察\n• 定制AI集成\n• 培训和支持",
                "contact": "您可以通过以下方式联系我们：\n• 联系表单：/contact\n• 邮箱：info@ai-solution.com\n• 电话：+1 (555) 123-4567\n\n我们通常在4个工作日内回复。",
                "support": "如需支持，请访问我们的联系页面或致电我们的支持团队。我们在这里帮助您充分利用您的AI解决方案。",
                "events": "我们定期举办活动，包括研讨会、峰会和会议。查看我们的/events页面了解即将举行的AI创新研讨会、企业AI峰会和行业特定聚会。",
                "workshop": "我们提供实践性AI研讨会，涵盖创新策略、实施最佳实践和行业特定用例。访问我们的活动页面查看即将举行的研讨会。",
                "pricing": "我们的定价根据您的特定需求、解决方案复杂性和实施要求进行定制。联系我们获取个性化报价和咨询。",
                "process": "我们的流程通常涉及：\n1. 发现和咨询\n2. 解决方案设计\n3. 快速原型制作\n4. 实施\n5. 培训和支持\n6. 持续优化",
                "vision": "我们的愿景是通过AI驱动的创新，使全球组织能够更智能、更快速、更高效地工作，从而塑造数字员工体验的未来。",
                "mission": "我们的使命是设计和提供AI驱动的解决方案，主动支持工作中的员工，提高生产力，并加速各行业的创新。",
                "values": "我们的核心价值观是：\n• 创新 - 持续突破界限，提供智能、前瞻性的AI解决方案\n• 信任与安全 - 在每个阶段都透明地构建安全、可靠的解决方案\n• 以人为本 - 设计能够赋能员工、增强工作并支持协作的AI\n• AI卓越 - 应用深厚的AI专业知识，提供可衡量的现实世界影响",
                "location": "我们的总部位于英国桑德兰。我们战略性地位于桑德兰创新区的中心。",
                "headquarters": "AI-Solution的总部位于英国桑德兰。我们的现代化办公空间旨在促进协作和创新。",
                "office_hours": "我们的办公时间是：\n• 周一 - 周五：上午9:00 - 下午6:00\n• 周六：上午10:00 - 下午2:00\n• 周日：关闭",
                "sunderland": "AI-Solution很自豪地位于英国桑德兰。访问我们，看看创新与卓越如何在我们的现代化办公空间相遇。",
                "default_responses": [
                    "我不确定那个具体问题，但我很乐意告诉您关于我们的AI解决方案、服务或公司。您最感兴趣的是什么？",
                    "那是个有趣的问题！虽然我可能没有关于那个的具体信息，但我可以帮助您了解我们的智能助手、自动化解决方案或行业特定产品。",
                    "我可能没有那个问题的答案，但我绝对可以帮助您了解AI-Solution如何转变您的数字工作场所。您想探索什么？",
                    "好问题！让我引导您到我最了解的内容 - 我们的AI解决方案、服务以及我们如何帮助像您这样的企业。您对哪个领域感兴趣？"
                ]
            }
        }
        
        
        if any(keyword in user_message for keyword in knowledge_base[language]["greetings"]):
            return responses[language]["greeting"]
        
        
        if any(keyword in user_message for keyword in knowledge_base[language]["thanks"]):
            return responses[language]["thanks"]
        
        
        if any(keyword in user_message for keyword in knowledge_base[language]["goodbye"]):
            return responses[language]["goodbye"]
        
        
        for topic, keywords in knowledge_base[language].items():
            if topic.startswith("greetings") or topic.startswith("thanks") or topic.startswith("goodbye"):
                continue
            if any(keyword in user_message for keyword in keywords):
                return responses[language].get(topic, responses[language]["default_responses"][0])
        
        
        default_responses = responses[language]["default_responses"]
        return default_responses[len(user_message) % len(default_responses)]
    
    def get_response(key, language):
        """Helper function to get response by key and language"""
        responses = {
            "en": {"no_message": "I didn't receive a message. How can I help you?"},
            "es": {"no_message": "No recibí un mensaje. ¿Cómo puedo ayudarte?"},
            "zh": {"no_message": "我没有收到消息。我该如何帮助您？"}
        }
        return responses.get(language, responses["en"]).get(key, "I didn't receive a message. How can I help you?")
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run()
