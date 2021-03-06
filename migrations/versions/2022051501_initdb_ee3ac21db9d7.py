"""initdb

Revision ID: ee3ac21db9d7
Revises: 
Create Date: 2022-05-15 15:01:36.721617

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils


# revision identifiers, used by Alembic.
revision = 'ee3ac21db9d7'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('site',
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('code', sa.String(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('status', sa.Enum('Active', 'Planned', 'Deployed', 'Offline', name='sitestatus'), nullable=False),
    sa.Column('priority', sa.Enum('P1', 'P2', 'P3', 'P4', name='sitepriority'), nullable=True),
    sa.Column('classfication', sa.Enum('office', 'datacenter', 'pop', 'remote', name='siteclassfication'), nullable=True),
    sa.Column('asn', sa.String(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_site_code'), 'site', ['code'], unique=True)
    op.create_index(op.f('ix_site_name'), 'site', ['name'], unique=True)
    op.create_table('circuit',
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('local_ip', sa.String(), nullable=True),
    sa.Column('gateway', sa.String(), nullable=True),
    sa.Column('status', sa.Enum('Active', 'Planned', 'Deployed', 'Offline', name='circuitstatus'), nullable=True),
    sa.Column('terminal_a', sa.String(), nullable=False),
    sa.Column('terminal_z', sa.String(), nullable=False),
    sa.Column('site_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['site_id'], ['site.id'], ondelete='cascade'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('terminal_a'),
    sa.UniqueConstraint('terminal_z')
    )
    op.create_index(op.f('ix_circuit_gateway'), 'circuit', ['gateway'], unique=False)
    op.create_index(op.f('ix_circuit_local_ip'), 'circuit', ['local_ip'], unique=False)
    op.create_index(op.f('ix_circuit_name'), 'circuit', ['name'], unique=True)
    op.create_table('dcim_circuits',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('local_ip', sa.String(), nullable=True),
    sa.Column('gateway', sa.String(), nullable=True),
    sa.Column('terminal_a', sa.String(), nullable=False),
    sa.Column('terminal_z', sa.String(), nullable=False),
    sa.Column('site_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['site_id'], ['site.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('terminal_a'),
    sa.UniqueConstraint('terminal_z')
    )
    op.create_index(op.f('ix_dcim_circuits_gateway'), 'dcim_circuits', ['gateway'], unique=False)
    op.create_index(op.f('ix_dcim_circuits_local_ip'), 'dcim_circuits', ['local_ip'], unique=False)
    op.create_index(op.f('ix_dcim_circuits_name'), 'dcim_circuits', ['name'], unique=True)
    op.create_table('host',
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('hostname', sa.String(), nullable=False),
    sa.Column('management_ip', sa.String(), nullable=True),
    sa.Column('serial', sa.String(), nullable=False),
    sa.Column('status', sa.Enum('Active', 'Planned', 'Deployed', 'Offline', name='hoststatus'), nullable=True),
    sa.Column('site_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['site_id'], ['site.id'], ondelete='cascade'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('serial')
    )
    op.create_index(op.f('ix_host_hostname'), 'host', ['hostname'], unique=False)
    op.create_index(op.f('ix_host_management_ip'), 'host', ['management_ip'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_host_management_ip'), table_name='host')
    op.drop_index(op.f('ix_host_hostname'), table_name='host')
    op.drop_table('host')
    op.drop_index(op.f('ix_dcim_circuits_name'), table_name='dcim_circuits')
    op.drop_index(op.f('ix_dcim_circuits_local_ip'), table_name='dcim_circuits')
    op.drop_index(op.f('ix_dcim_circuits_gateway'), table_name='dcim_circuits')
    op.drop_table('dcim_circuits')
    op.drop_index(op.f('ix_circuit_name'), table_name='circuit')
    op.drop_index(op.f('ix_circuit_local_ip'), table_name='circuit')
    op.drop_index(op.f('ix_circuit_gateway'), table_name='circuit')
    op.drop_table('circuit')
    op.drop_index(op.f('ix_site_name'), table_name='site')
    op.drop_index(op.f('ix_site_code'), table_name='site')
    op.drop_table('site')
    # ### end Alembic commands ###
