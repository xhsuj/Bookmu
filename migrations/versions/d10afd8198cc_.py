"""empty message

Revision ID: d10afd8198cc
Revises: 1e3e83033c66
Create Date: 2021-08-11 16:03:40.016574

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'd10afd8198cc'
down_revision = '1e3e83033c66'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('artist',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('city', sa.String(), nullable=False),
    sa.Column('state', sa.String(), nullable=False),
    sa.Column('phone', sa.String(), nullable=False),
    sa.Column('facebook_link', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('venue',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('city', sa.String(), nullable=False),
    sa.Column('state', sa.String(), nullable=False),
    sa.Column('phone', sa.String(), nullable=False),
    sa.Column('address', sa.String(), nullable=False),
    sa.Column('facebook_link', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('genres',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('kind', sa.String(), nullable=False),
    sa.Column('venue_id', sa.Integer(), nullable=True),
    sa.Column('artist_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['artist_id'], ['artist.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['venue_id'], ['venue.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('shows',
    sa.Column('artist_id', sa.Integer(), nullable=False),
    sa.Column('venue_id', sa.Integer(), nullable=False),
    sa.Column('start_time', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['artist_id'], ['artist.id'], ),
    sa.ForeignKeyConstraint(['venue_id'], ['venue.id'], ),
    sa.PrimaryKeyConstraint('artist_id', 'venue_id')
    )
    op.drop_table('todos')
    op.drop_table('table0')
    op.drop_table('persons')
    op.drop_table('song_info')
    op.drop_table('table2')
    op.drop_table('songbase')
    op.drop_table('table3')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('table3',
    sa.Column('id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('completed', sa.BOOLEAN(), server_default=sa.text('false'), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='table3_pkey')
    )
    op.create_table('songbase',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('songName', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('artist', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('albumName', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('isseu_date', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='songbase_pkey'),
    sa.UniqueConstraint('albumName', name='songbase_albumName_key'),
    sa.UniqueConstraint('artist', name='songbase_artist_key'),
    sa.UniqueConstraint('isseu_date', name='songbase_isseu_date_key'),
    sa.UniqueConstraint('songName', name='songbase_songName_key')
    )
    op.create_table('table2',
    sa.Column('id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('sex', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='table2_pkey')
    )
    op.create_table('song_info',
    sa.Column('id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('album', sa.VARCHAR(), server_default=sa.text("'unknown'::character varying"), autoincrement=False, nullable=False),
    sa.Column('artist', sa.VARCHAR(), server_default=sa.text("'unknown'::character varying"), autoincrement=False, nullable=False),
    sa.Column('song_name', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('created_time', sa.DATE(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='song_info_pkey')
    )
    op.create_table('persons',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='persons_pkey')
    )
    op.create_table('table0',
    sa.Column('id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('description', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('comment', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('sex', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='table0_pkey')
    )
    op.create_table('todos',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('description', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='todos_pkey')
    )
    op.drop_table('shows')
    op.drop_table('genres')
    op.drop_table('venue')
    op.drop_table('artist')
    # ### end Alembic commands ###
