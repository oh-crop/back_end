"""Seed DB

Revision ID: 752c338c6328
Revises: 8c089a511ab7
Create Date: 2020-07-21 12:02:06.021348

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column
from sqlalchemy import String, Integer, Date, Unicode, Boolean


# revision identifiers, used by Alembic.
revision = '752c338c6328'
down_revision = '8c089a511ab7'
branch_labels = None
depends_on = None


def upgrade():
    plants_table = table('plants',
        column('id', Integer),
        column('name', String),
        column('plant_type', String),
        column('image', Unicode),
        column('lighting', String),
        column('water_frequency', Integer),
        column('harvest_time', Integer),
        column('root_depth', Integer),
        column('annual', Boolean),
    )

    op.bulk_insert(plants_table,
      [
        {'id':1,'name':'Andrew','plant_type':'Better Boy Tomato','image':'https://skitterphoto.com/photos/skitterphoto-1901-default.jpg','lighting':'Full Sun','water_frequency':7,'harvest_time':70,'root _depth':24,'annual':False},
        {'id':2,'name':'Jimothy','plant_type':'Cherry Tomato','image':'https://cdn.pixabay.com/photo/2019/05/29/19/04/tomatoes-4238247_960_720.jpg','lighting':'Full Sun','water_frequency':3,'harvest_time':50,'root _depth':12,'annual':False},
        {'id':3,'name':'Hans','plant_type':'Roma Tomato','image':'https://live.staticflickr.com/2591/3816942238_e669d597f7_w.jpg','lighting':'Full Sun','water_frequency':3,'harvest_time':75,'root _depth':12,'annual':False},
        {'id':4,'name':'Diego','plant_type':'Jalapeno Peppers','image':'https://storage.needpix.com/rsynced_images/jalapeno-2053130_1280.jpg','lighting':'Full Sun','water_frequency':2,'harvest_time':90,'root _depth':12,'annual':True},
        {'id':5,'name':'Rachel','plant_type':'Dill','image':'https://storage.needpix.com/rsynced_images/dill-2826179_1280.jpg','lighting':'Full Sun','water_frequency':2,'harvest_time':70,'root _depth':12,'annual':True},
        {'id':6,'name':'Ted','plant_type':'Cucumber','image':'https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcTH6vaDH-HbpwfvwrutxxtJ-5PgpAFNfwXNiA&usqp=CAU','lighting':'Full Sun','water_frequency':1,'harvest_time':50,'root _depth':48,'annual':True},
        {'id':7,'name':'Ronald','plant_type':'Pumpkin','image':'https://static1.squarespace.com/static/5a485430e9bfdfa8207ede01/5a947dd98165f5c601e919d0/5d67ed18d3c92c0001a80f49/1571424584578/pumpkins.jpg?format=1500w','lighting':'Full Sun','water_frequency':1,'harvest_time':50,'root _depth':48,'annual':True},
        {'id':8,'name':'Venus','plant_type':'Venus Fly Trap','image':'https://p0.pikist.com/photos/62/950/venus-fly-trap-plant-green-thumbnail.jpg','lighting':'Full Sun','water_frequency':3,'harvest_time':None,'root _depth':4,'annual':False},
        {'id':9,'name':'Tina','plant_type':'Aloe','image':'https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcTuaaDL2UgvUhOfsKtBJt515UTYy0Ixs-B0Bw&usqp=CAU','lighting':'Full Sun','water_frequency':21,'harvest_time':1460,'root _depth':17,'annual':False},
        {'id':10,'name':'Kenai','plant_type':'Bear Paw','image':'https://cdn.shopify.com/s/files/1/2391/9491/products/image_ff75aeba-99e0-4791-b21b-74580ff9303b_1024x1024.jpg?v=1571710608','lighting':'Full Sun','water_frequency':7,'harvest_time':None,'root _depth':4,'annual':False},
        {'id':11,'name':'Ken','plant_type':'Bamboo','image':'https://cdn.pixabay.com/photo/2020/05/24/11/53/bamboo-5213909_960_720.jpg','lighting':'Indirect Sun','water_frequency':4,'harvest_time':None,'root _depth':36,'annual':False},
        {'id':12,'name':'Mary','plant_type':'Raspberry','image':'https://www.publicdomainpictures.net/pictures/10000/velka/1-1248158051Ix2h.jpg','lighting':'Full Sun','water_frequency':4,'harvest_time':456,'root _depth':20,'annual':False},
        {'id':13,'name':'Jane','plant_type':'Blackberry','image':'https://www.publicdomainpictures.net/pictures/10000/velka/1-1248160910fXMI.jpg','lighting':'Full Sun','water_frequency':4,'harvest_time':730,'root _depth':14,'annual':False},
        {'id':14,'name':'Randy','plant_type':'Strawberry','image':'https://www.picserver.org/pictures/strawberries01-lg.jpg','lighting':'Full Sun','water_frequency':4,'harvest_time':152,'root _depth':12,'annual':False},
        {'id':15,'name':'Howdi','plant_type':'Avocado','image':'https://c1.peakpx.com/wallpaper/736/669/216/appetite-avacado-avo-avocado-wallpaper-preview.jpg','lighting':'Full Sun','water_frequency':7,'harvest_time':3285,'root _depth':12,'annual':False},
        {'id':16,'name':'Russel','plant_type':'Cilantro','image':'https://storage.needpix.com/rsynced_images/cilantro-1287301_1280.jpg','lighting':'Full Sun/Light Shade','water_frequency':3,'harvest_time':70,'root _depth':18,'annual':True},
        {'id':17,'name':'Todd','plant_type':'Lemon','image':'https://p0.pikrepo.com/preview/784/509/two-lemons-and-1-slice-of-lemon.jpg','lighting':'Full Sun','water_frequency':4,'harvest_time':365,'root _depth':24,'annual':False},
        {'id':18,'name':'Leslie','plant_type':'Lime','image':'https://i2.pickpik.com/photos/197/226/505/sliced-lime-fruit-lime-slice-preview.jpg','lighting':'Full Sun','water_frequency':4,'harvest_time':121,'root _depth':24,'annual':False},
        {'id':19,'name':'Henri','plant_type':'Grapes','image':'https://p0.pikist.com/photos/670/14/autumn-grapes-grape-vine-fruit-winegrowing-grapevine-blue-grapes-wine-harvest.jpg','lighting':'Full Sun','water_frequency':7,'harvest_time':1095,'root _depth':36,'annual':False},
        {'id':20,'name':'Jennifer','plant_type':'Asparagus','image':'https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcS2HpJaaQQPpaDrolZY-cg9owfb4z9oy2eZ-A&usqp=CAU','lighting':'Full Sun','water_frequency':21,'harvest_time':730,'root _depth':10,'annual':False},
        {'id':21,'name':'Sunshine','plant_type':'Daffodil','image':'https://p0.pikist.com/photos/246/87/daffodils-spring-flowers-daffodil-bloom-nature-yellow-petals-garden.jpg','lighting':'Full Sun','water_frequency':7,'harvest_time':None,'root _depth':6,'annual':False},
        {'id':22,'name':'Hades','plant_type':'Sunflower','image':'https://p0.pikist.com/photos/348/318/sunflower-yellow-flower-yellow-sun-flower-plant-nature-summer-field-of-sunflowers.jpg','lighting':'Full Sun','water_frequency':7,'harvest_time':None,'root _depth':24,'annual':False},
        {'id':23,'name':'Mort','plant_type':'Bleeding Heart','image':'https://images.pexels.com/photos/414362/pexels-photo-414362.jpeg?cs=srgb&dl=beautiful-bleeding-heart-bloom-blooming-414362.jpg&fm=jpg','lighting':'Full/Partial Shade','water_frequency':7,'harvest_time':None,'root _depth':6,'annual':False},
        {'id':24,'name':'Judy','plant_type':'Foxglove','image':'https://upload.wikimedia.org/wikipedia/commons/d/da/Purple_Foxglove_%28Digitalis_purpurea%29_2008_03.jpg','lighting':'Full/Partial Shade','water_frequency':7,'harvest_time':None,'root _depth':10,'annual':False},
      ]
    )


def downgrade():
    op.execute('''DELETE * FROM "plants"; ''')
