from datetime import datetime, timedelta, timezone
from random import choice, randint, sample
from app import create_app, db
from models import Review

app = create_app()

with app.app_context():
    
    names = [
        "Alice Johnson", "Bob Smith", "Clara Davis", "Daniel Lee", "Eva Green",
        "Frank Miller", "Grace Kim", "Henry Thompson", "Isla Brown", "Jack Wilson",
        "Karen Moore", "Liam Anderson", "Mia Scott", "Noah Turner", "Olivia White",
        "Peter Hall", "Quinn Lewis", "Ruby Young", "Samuel King", "Tina Adams"
    ]

    job_titles = [
        "Product Manager", "Software Engineer", "HR Specialist", "Marketing Lead",
        "Data Analyst", "Operations Manager", "UX Designer", "Sales Executive", "Head of Software Engineering", "Head of Business Intelligence", "IT Manager", "IT Executive", "IT Director"
    ]

    companies = [
        "TechCorp", "Innova Solutions", "GlobalSoft", "NextGen AI", "BrightFuture Ltd",
        "Alpha Systems", "SmartWorks", "FutureTech", "Mello", "Pixeon", "Cybertrix", "Blobe"
    ]

    industries = [
        "Technology", "Finance", "Healthcare", "Education & EdTech", "Logistics & Supply Chain", "Retail & E-commerce", "Manufacturing"
    ]

    
    positive_feedback_base = [
        "The AI tools have transformed our workflow efficiency tremendously.",
        "We are very satisfied with the solutions provided by AI-Solution.",
        "Exceptional service and intuitive AI products!",
        "Our team has seen great productivity gains since using these tools.",
        "Highly recommend AI-Solution for any business looking to leverage AI.",
        "The platform is user-friendly and the support team is very responsive."
    ]

    mixed_feedback_base = [
        "The product is good, but the onboarding process could be smoother.",
        "Some features are excellent, though a few are still buggy.",
        "Overall satisfied, but we experienced occasional downtime.",
        "AI tools are helpful, though integration with existing software was tricky."
    ]

    negative_feedback_base = [
        "We faced multiple issues with the setup and support was slow.",
        "The software did not meet our expectations and caused delays.",
        "Not satisfied with the AI solutions for our workflow needs."
    ]

    
    def vary_feedback(base_list):
        varied = []
        for text in base_list:
            
            variations = [
                text,
                text.replace("AI", "the AI platform"),
                text + " Overall, quite satisfied.",
                text.replace("tools", "solutions"),
            ]
            varied.extend(variations)
        return varied

    positive_feedback = vary_feedback(positive_feedback_base)
    mixed_feedback = vary_feedback(mixed_feedback_base)
    negative_feedback = vary_feedback(negative_feedback_base)

    
    used_feedback = set()  
    for i in range(20):
        name = names[i]
        job_title = choice(job_titles)
        company = choice(companies)
        industry = choice(industries)

        
        rating_type = choice(["positive"]*12 + ["mixed"]*5 + ["negative"]*3)

        if rating_type == "positive":
            rating = randint(4, 5)
            pool = positive_feedback
        elif rating_type == "mixed":
            rating = randint(3, 4)
            pool = mixed_feedback
        else:
            rating = randint(1, 2)
            pool = negative_feedback

        
        feedback = choice([f for f in pool if f not in used_feedback])
        used_feedback.add(feedback)

        
        past_days = randint(30, 1000)  
        created_at = datetime.now(timezone.utc) - timedelta(days=past_days)

        review = Review(
            name=name,
            job_title=job_title,
            company=company,
            industry=industry,
            rating=rating,
            feedback=feedback,
            created_at=created_at
        )

        db.session.add(review)

    db.session.commit()
    print("20 realistic reviews inserted successfully!")
