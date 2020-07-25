"""Reseed DB

Revision ID: 8d80e867d3dd
Revises: b557abac858b
Create Date: 2020-07-24 18:32:20.914310

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column
from sqlalchemy import String, Integer, Date, Unicode, Boolean

# revision identifiers, used by Alembic.
revision = '8d80e867d3dd'
down_revision = 'b557abac858b'
branch_labels = None
depends_on = None


def upgrade():
    op.execute('''TRUNCATE TABLE "gardens"; ''')
    op.execute('''TRUNCATE TABLE "plants" CASCADE; ''')

    plants_table = table('plants',
        column('id', Integer),
        column('plant_type', String),
        column('image', Unicode),
        column('lighting', String),
        column('water_frequency', Integer),
        column('harvest_time', Integer),
        column('root_depth', Integer),
        column('annual', String),
    )

    op.bulk_insert(plants_table,
      [
        {'id':1,'plant_type':'Better Boy Tomato','image':'https://skitterphoto.com/photos/skitterphoto-1901-default.jpg','lighting':'Full Sun','water_frequency':7,'harvest_time':70,'root_depth':24,'annual':"Perennial"},
        {'id':2,'plant_type':'Cherry Tomato','image':'https://cdn.pixabay.com/photo/2019/05/29/19/04/tomatoes-4238247_960_720.jpg','lighting':'Full Sun','water_frequency':3,'harvest_time':50,'root_depth':12,'annual':"Perennial"},
        {'id':3,'plant_type':'Roma Tomato','image':'https://live.staticflickr.com/2591/3816942238_e669d597f7_w.jpg','lighting':'Full Sun','water_frequency':3,'harvest_time':75,'root_depth':12,'annual':"Perennial"},
        {'id':4,'plant_type':'Jalapeno Peppers','image':'https://storage.needpix.com/rsynced_images/jalapeno-2053130_1280.jpg','lighting':'Full Sun','water_frequency':2,'harvest_time':90,'root_depth':12,'annual':"Annual"},
        {'id':5,'plant_type':'Dill','image':'https://storage.needpix.com/rsynced_images/dill-2826179_1280.jpg','lighting':'Full Sun','water_frequency':2,'harvest_time':70,'root_depth':12,'annual':"Perennial"},
        {'id':6,'plant_type':'Cucumber','image':'https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcTH6vaDH-HbpwfvwrutxxtJ-5PgpAFNfwXNiA&usqp=CAU','lighting':'Full Sun','water_frequency':1,'harvest_time':50,'root_depth':48,'annual':"Annual"},
        {'id':7,'plant_type':'Pumpkin','image':'https://static1.squarespace.com/static/5a485430e9bfdfa8207ede01/5a947dd98165f5c601e919d0/5d67ed18d3c92c0001a80f49/1571424584578/pumpkins.jpg?format=1500w','lighting':'Full Sun','water_frequency':1,'harvest_time':50,'root_depth':48,'annual':"Annual"},
        {'id':8,'plant_type':'Venus Fly Trap','image':'https://p0.pikist.com/photos/62/950/venus-fly-trap-plant-green-thumbnail.jpg','lighting':'Full Sun','water_frequency':3,'harvest_time':None,'root_depth':4,'annual':"Annual"},
        {'id':9,'plant_type':'Aloe','image':'https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcTuaaDL2UgvUhOfsKtBJt515UTYy0Ixs-B0Bw&usqp=CAU','lighting':'Full Sun','water_frequency':21,'harvest_time':1460,'root_depth':17,'annual':"Perennial"},
        {'id':10,'plant_type':'Bear Paw','image':'https://cdn.shopify.com/s/files/1/2391/9491/products/image_ff75aeba-99e0-4791-b21b-74580ff9303b_1024x1024.jpg?v=1571710608','lighting':'Full Sun','water_frequency':7,'harvest_time':None,'root_depth':4,'annual':"Annual"},
        {'id':11,'plant_type':'Bamboo','image':'https://cdn.pixabay.com/photo/2020/05/24/11/53/bamboo-5213909_960_720.jpg','lighting':'Indirect Sun','water_frequency':4,'harvest_time':None,'root_depth':36,'annual':"Perennial"},
        {'id':12,'plant_type':'Raspberry','image':'https://www.publicdomainpictures.net/pictures/10000/velka/1-1248158051Ix2h.jpg','lighting':'Full Sun','water_frequency':4,'harvest_time':456,'root_depth':20,'annual':"Perennial"},
        {'id':13,'plant_type':'Blackberry','image':'https://www.publicdomainpictures.net/pictures/10000/velka/1-1248160910fXMI.jpg','lighting':'Full Sun','water_frequency':4,'harvest_time':730,'root_depth':14,'annual':"Perennial"},
        {'id':14,'plant_type':'Strawberry','image':'https://www.picserver.org/pictures/strawberries01-lg.jpg','lighting':'Full Sun','water_frequency':4,'harvest_time':152,'root_depth':12,'annual':"Perennial"},
        {'id':15,'plant_type':'Avocado','image':'https://c1.peakpx.com/wallpaper/736/669/216/appetite-avacado-avo-avocado-wallpaper-preview.jpg','lighting':'Full Sun','water_frequency':7,'harvest_time':3285,'root_depth':12,'annual':"Perennial"},
        {'id':16,'plant_type':'Cilantro','image':'https://storage.needpix.com/rsynced_images/cilantro-1287301_1280.jpg','lighting':'Full Sun/Light Shade','water_frequency':3,'harvest_time':70,'root_depth':18,'annual':"Annual"},
        {'id':17,'plant_type':'Lemon','image':'https://p0.pikrepo.com/preview/784/509/two-lemons-and-1-slice-of-lemon.jpg','lighting':'Full Sun','water_frequency':4,'harvest_time':365,'root_depth':24,'annual':"Perennial"},
        {'id':18,'plant_type':'Lime','image':'https://i2.pickpik.com/photos/197/226/505/sliced-lime-fruit-lime-slice-preview.jpg','lighting':'Full Sun','water_frequency':4,'harvest_time':121,'root_depth':24,'annual':"Perennial"},
        {'id':19,'plant_type':'Grapes','image':'https://p0.pikist.com/photos/670/14/autumn-grapes-grape-vine-fruit-winegrowing-grapevine-blue-grapes-wine-harvest.jpg','lighting':'Full Sun','water_frequency':7,'harvest_time':1095,'root_depth':36,'annual':"Perennial"},
        {'id':20,'plant_type':'Asparagus','image':'https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcS2HpJaaQQPpaDrolZY-cg9owfb4z9oy2eZ-A&usqp=CAU','lighting':'Full Sun','water_frequency':21,'harvest_time':730,'root_depth':10,'annual':"Annual"},
        {'id':21,'plant_type':'Daffodil','image':'https://p0.pikist.com/photos/246/87/daffodils-spring-flowers-daffodil-bloom-nature-yellow-petals-garden.jpg','lighting':'Full Sun','water_frequency':7,'harvest_time':None,'root_depth':6,'annual':"Annual"},
        {'id':22,'plant_type':'Sunflower','image':'https://p0.pikist.com/photos/348/318/sunflower-yellow-flower-yellow-sun-flower-plant-nature-summer-field-of-sunflowers.jpg','lighting':'Full Sun','water_frequency':7,'harvest_time':None,'root_depth':24,'annual':"Annual"},
        {'id':23,'plant_type':'Bleeding Heart','image':'https://images.pexels.com/photos/414362/pexels-photo-414362.jpeg?cs=srgb&dl=beautiful-bleeding-heart-bloom-blooming-414362.jpg&fm=jpg','lighting':'Full/Partial Shade','water_frequency':7,'harvest_time':None,'root_depth':6,'annual':"Annual"},
        {'id':24,'plant_type':'Foxglove','image':'https://upload.wikimedia.org/wikipedia/commons/d/da/Purple_Foxglove_%28Digitalis_purpurea%29_2008_03.jpg','lighting':'Full/Partial Shade','water_frequency':7,'harvest_time':None,'root_depth':10,'annual':"Annual"},
      ]
    )


def downgrade():
    op.execute('''TRUNCATE TABLE "plants"; ''')
