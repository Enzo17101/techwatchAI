from app.core.database import SessionLocal
from app.models.article import Article
from sqlalchemy import text

def test_connection():
    db = SessionLocal()
    try:
        print("🔌 Tentative de connexion à PostgreSQL...")

        # Test 1 : Ping simple SQL
        db.execute(text("SELECT 1"))
        print("✅ Connexion réussie !")

        # Test 2 : Lecture des articles créés par Java
        count = db.query(Article).count()
        print(f"📊 Nombre d'articles trouvés dans la table : {count}")

        if count > 0:
            first = db.query(Article).first()
            print(f"📝 Exemple : {first.title} (ID: {first.id})")
        else:
            print("⚠️ Table vide")

    except Exception as e:
        print(f"❌ Erreur : {e}")
    finally:
        db.close()

if __name__ == "__main__":
    test_connection()