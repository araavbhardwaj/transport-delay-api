import random
from datetime import datetime, timedelta
from database import SessionLocal, engine
import models

# Ensure tables exist
models.Base.metadata.create_all(bind=engine)

def seed_database():
    db = SessionLocal()
    
    # Check if data already exists to avoid duplicates
    if db.query(models.Incident).count() > 10:
        print("Database already contains data. Skipping seed.")
        db.close()
        return

    routes = ["LeedsBus 1", "LeedsBus 6", "LeedsBus 56", "LeedsBus 27", "Northern Rail: Harrogate Line"]
    locations = ["Headingley", "Hyde Park", "Leeds City Centre", "Kirkstall", "Burley"]
    descriptions = ["Heavy traffic", "Temporary traffic lights", "Vehicle breakdown", "Driver shortage", "Adverse weather"]

    print("Seeding database with 250 realistic transport incidents...")
    
    
    for _ in range(250):

        random_days_ago = random.randint(0, 30)
        random_hours_ago = random.randint(0, 23)
        past_date = datetime.utcnow() - timedelta(days=random_days_ago, hours=random_hours_ago)

        incident = models.Incident(
            location=random.choice(locations),
            route=random.choice(routes),
            delay_minutes=random.randint(5, 60), # Delays between 5 and 60 mins
            description=random.choice(descriptions),
            timestamp=past_date
        )
        db.add(incident)
    
    db.commit()
    db.close()
    print("Successfully seeded the database!")

if __name__ == "__main__":
    seed_database()