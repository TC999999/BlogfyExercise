from models import db, User, Post, Tag, PostTag
from app import app

db.drop_all()
db.create_all()

PostTag.query.delete()
Post.query.delete()
Tag.query.delete()
User.query.delete()

# Add Users
f1 = User(
    first_name="Ross",
    last_name="Geller",
    image_url="https://upload.wikimedia.org/wikipedia/en/6/6f/David_Schwimmer_as_Ross_Geller.jpg",
)
f2 = User(
    first_name="Rachel",
    last_name="Green",
    image_url="https://upload.wikimedia.org/wikipedia/en/e/ec/Jennifer_Aniston_as_Rachel_Green.jpg",
)
f3 = User(
    first_name="Phoebe",
    last_name="Buffay",
    image_url="https://upload.wikimedia.org/wikipedia/en/f/f6/Friendsphoebe.jpg",
)
f4 = User(first_name="Gunther", last_name="Centralperk")

# Add Posts
p1 = Post(
    title="My Sandwich",
    content="Someone at work at my sandwich. MY SANDWICH!!!",
    usr=f1,
)
p2 = Post(
    title="This isn't a marriage",
    content="This is the world's worst hangover",
    usr=f2,
)
p3 = Post(
    title="Thumbs",
    content="I found a severed thumb in my Pepsi today",
    usr=f3,
)
p4 = Post(
    title="My Sister",
    content="If you didn't eat fast, you didn;t eat!",
    usr=f1,
)

db.session.add_all([f1, f2, f3, f4, p1, p2, p3, p4])
db.session.commit()

# Add Tags
ta = Tag(name="Angry", pst_tg=[PostTag(post_id=p1.id), PostTag(post_id=p2.id)])
tn = Tag(name="Neutral", pst_tg=[PostTag(post_id=p3.id)])

db.session.add_all([ta, tn])
db.session.commit()
